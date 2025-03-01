from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncMonth


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