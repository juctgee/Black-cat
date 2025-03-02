from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.db.models import Count, Avg, Q

from .models import Menu, Promotion, Order, Member, Review

# สร้าง SignUpView ที่เมื่อสมัครสมาชิกแล้วจะสร้าง Member instance ด้วย
class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('members')  # เปลี่ยนไปหน้าสมาชิกหลังสมัครเสร็จ

    def form_valid(self, form):
        # บันทึกข้อมูล User ก่อน
        response = super().form_valid(form)
        # สร้าง Member instance ด้วย username จาก User ที่สมัคร
        Member.objects.create(
            username=self.object.username,
            password=self.object.password,  # ควรเก็บ password hashed แล้ว
            points=0
        )
        return response

def home(req):
    best_selling_menus = Menu.objects.annotate(num_reviews=Count('reviews')).order_by('-num_reviews')
    context = {
        'best_selling_menus': best_selling_menus,
    }
    return render(req, 'index.html', context)

def menu(request):
    menus = Menu.objects.annotate(avg_rating=Avg('reviews__rating')).prefetch_related('promotions')
    storewide_promos = Promotion.objects.filter(applicable_menus__isnull=True)
    for m in menus:
        m.all_promos = list(m.promotions.all()) + list(storewide_promos)
    context = {
        'menus': menus,
    }
    return render(request, 'menu.html', context)

@login_required
def members(req):
    context = {
        'username': req.user.username,
    }
    return render(req, 'members.html', context)

def register(req):
    return render(req, 'register.html')

@login_required
def review(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    reviews = menu.reviews.all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    if request.method == "POST":
        rating = int(request.POST.get("rating"))
        comment = request.POST.get("comment", "")

        Review.objects.create(
            menu=menu,
            rating=rating,
            comment=comment
        )
        return redirect('review', menu_id=menu.id)

    context = {
        'menu': menu,
        'reviews': reviews,
        'avg_rating': avg_rating,
    }
    return render(request, 'review.html', context)

def buy(request, menu_id):
    menu_item = get_object_or_404(Menu, pk=menu_id)
    return render(request, 'buy.html', {'menu': menu_item})

@login_required
def process_order(request, menu_id):
    if request.method == 'POST':
        menu_item = get_object_or_404(Menu, pk=menu_id)
        quantity = int(request.POST.get('quantity', 1))
        selected_promo = request.POST.get('selected_promo', None)

        from decimal import Decimal
        try:
            base_price = Decimal(menu_item.price)
        except Exception:
            base_price = Decimal("0.00")

        discount_percentage = Decimal(selected_promo) if selected_promo and selected_promo != "0" else Decimal("0")
        discount_amount = base_price * (discount_percentage / 100)
        final_price = base_price - discount_amount

        # ค้นหา Member instance จาก request.user.username
        member_instance = get_object_or_404(Member, username=request.user.username)

        # สร้าง Order ใหม่
        order = Order.objects.create(
            member=member_instance,
            menu=menu_item,
            quantity=quantity,
            total_price=final_price,
        )
        return redirect('my_menu')
    return redirect('buy', menu_id=menu_id)
@login_required
def my_menu(request):
    # ค้นหา Member instance จาก username ของผู้ใช้ที่ล็อกอินอยู่
    member_instance = get_object_or_404(Member, username=request.user.username)
    # ดึงรายการ Order ที่สั่งซื้อโดย Member นี้
    orders = Order.objects.filter(member=member_instance).order_by('-order_date')
    context = {
        'orders': orders,
    }
    return render(request, 'my_menu.html', context)

def logout_view(req):
    return redirect('login')
