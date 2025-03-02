from rest_framework.decorators import api_view # type: ignore
from rest_framework.response import Response # type: ignore
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncMonth
from myapp.models import Order, Promotion
from django.db.models import Count
from datetime import datetime


from myapp.models import Menu, Order, Member, Event

@api_view(['GET'])
def member_list(request):
    members = list(Member.objects.all().values())
    return Response(members)

@api_view(['GET'])
def menu_list(request):
    menus = list(Menu.objects.all().values())
    return Response(menus)

@api_view(['GET'])
def total_sales(request):
    """
    ดึงข้อมูลยอดขายทั้งหมด (สมมติว่า Order มีฟิลด์ total_price)
    """
    total = Order.objects.aggregate(Sum('total_price'))['total_price__sum']
    if total is None:
        total = 0
    return Response({"total_sales": float(total)})

@api_view(['GET'])
def new_members(request):
    """
    ดูจำนวนสมาชิกที่สมัครเข้ามาใหม่ในช่วง 7 วันล่าสุด
    โดยใช้เวลาปัจจุบัน (local time) แล้วนับถอยหลังไป 7 วัน
    """
    now = timezone.localtime()  # ใช้ local time แทน timezone.now()
    last_7_days = now - timedelta(days=7)
    count_new_members = Member.objects.filter(created_at__gte=last_7_days).count()
    return Response({
        "new_members_past_7_days": count_new_members
    })

@api_view(['GET'])
def monthly_sales(request):
    # คำนวณยอดขายรายเดือน
    sales = (
        Order.objects
        .annotate(month=TruncMonth('order_date'))
        .values('month')
        .annotate(total_sales=Sum('total_price'))
        .order_by('month')
    )
    result = [
        {"month": item['month'].strftime("%B %Y"), "sales": float(item['total_sales'] or 0)}
        for item in sales
    ]
    return Response(result)

@api_view(['GET'])
def upcoming_events(request):
    # ดึงกิจกรรมที่ยังไม่ผ่าน (ตัวอย่าง: event_date อยู่ในอนาคต)
    now = timezone.now()
    events = list(Event.objects.filter(event_date__gte=now).values())
    return Response(events)

@api_view(['GET'])
def order_list(request):
    orders = Order.objects.all().values(
        'id', 'member__username', 'menu__name', 'quantity', 'total_price', 'order_date'
    )
    return Response(list(orders))

@api_view(['GET'])
def order_by_date(request):
    if 'start_date' not in request.query_params or 'end_date' not in request.query_params:
        return Response({"error": "Missing start_date and end_date parameters"}, status=400)
    
    start_date = request.query_params['start_date']
    end_date = request.query_params['end_date']

    orders = Order.objects.filter(
        order_date__date__gte=start_date,
        order_date__date__lte=end_date
    ).values(
        'id', 'member__username', 'menu__name', 'quantity', 'total_price', 'order_date'
    )
    return Response(list(orders))

@api_view(['GET'])
def best_selling_menus(request):
    # คำนวณจำนวนรีวิวสำหรับแต่ละเมนูและจัดเรียงจากมากไปน้อย
    best_selling = Menu.objects.annotate(num_reviews=Count('reviews')).order_by('-num_reviews')
    # สร้าง list ของ dictionary โดยเลือก field ที่ต้องการแสดง
    data = list(best_selling.values('id', 'name', 'price', 'category', 'image', 'num_reviews'))
    return Response(data)

@api_view(['GET'])
def promotion_list(request):
    """
    ดึงรายการโปรโมชั่นทั้งหมด
    """
    promotions = Promotion.objects.all().values()
    return Response(list(promotions))

@api_view(['POST'])
def add_promotion(request):
    """
    เพิ่มโปรโมชั่นใหม่
    """
    data = request.data
    try:
        promo = Promotion.objects.create(
            title=data.get("title"),
            description=data.get("description"),
            discount=data.get("discount"),
            start_date=datetime.strptime(data.get("start_date"), "%Y-%m-%d").date(),
            end_date=datetime.strptime(data.get("end_date"), "%Y-%m-%d").date()
        )
        return Response({"id": promo.id, "message": "Promotion created successfully"})
    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(['DELETE'])
def delete_promotion(request, promo_id):
    """
    ลบโปรโมชั่นตาม id
    """
    try:
        promo = Promotion.objects.get(id=promo_id)
        promo.delete()
        return Response({"message": "Promotion deleted successfully"})
    except Promotion.DoesNotExist:
        return Response({"error": "Promotion not found"}, status=404)