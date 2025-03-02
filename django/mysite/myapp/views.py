from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.db.models import Count, Avg
from django.http import HttpResponseForbidden

from .models import Review, Menu, Promotion, Order, Member
from .forms import PromotionForm, MenuForm # แบบฟอร์มสำหรับโปรโมชั่น (สำหรับส่วนโปรโมชั่น)

# สร้าง SignUpView ที่เมื่อสมัครสมาชิกแล้วจะสร้าง Member instance ด้วย
class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    # หลังสมัครเสร็จจะ redirect ไปที่ user_dashboard
    success_url = reverse_lazy('user_dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        # สร้าง Member instance สำหรับ user ที่สมัคร (password ที่เก็บเป็น hashed แล้ว)
        Member.objects.create(
            username=self.object.username,
            password=self.object.password,
            points=0
        )
        return response

def home(request):
    # ดึงเมนูที่ขายดีโดยอิงจากจำนวนรีวิว
    best_selling_menus = Menu.objects.annotate(num_reviews=Count('reviews')).order_by('-num_reviews')
    context = {
        'best_selling_menus': best_selling_menus,
    }
    return render(request, 'index.html', context)

def menu(request):
    # ดึงเมนูพร้อมค่าเฉลี่ยรีวิวและโปรโมชั่นที่เกี่ยวข้อง
    menus = Menu.objects.annotate(avg_rating=Avg('reviews__rating')).prefetch_related('promotions')
    # โปรโมชั่นที่ใช้ได้ทั้งร้าน (applicable_menus ว่าง)
    storewide_promos = Promotion.objects.filter(applicable_menus__isnull=True)
    for m in menus:
        # รวมโปรโมชั่นที่ผูกกับเมนูและโปรโมชั่นสำหรับทั้งร้าน
        m.all_promos = list(m.promotions.all()) + list(storewide_promos)
    context = {
        'menus': menus,
    }
    return render(request, 'menu.html', context)

@login_required
def user_dashboard(request):
    """
    หลัง login ให้ตรวจสอบสิทธิ์ผู้ใช้:
    - หากเป็น admin (staff หรือ superuser) ให้ redirect ไปที่ custom admin dashboard
    - หากเป็นผู้ใช้ทั่วไป ให้ render หน้า my_menu.html
    """
    if request.user.is_staff or request.user.is_superuser:
        return redirect('custom_admin')
    else:
        return render(request, 'my_menu.html')

@login_required
def custom_admin_dashboard(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("Access Denied")
    
    promotions = Promotion.objects.all()
    menus = Menu.objects.all()
    members = Member.objects.all()  # ดึงรายชื่อสมาชิกทั้งหมด
    context = {
        'promotions': promotions,
        'menus': menus,
        'members': members,
    }
    return render(request, 'admin/dashboard.html', context)

def register(request):
    return render(request, 'register.html')

@login_required
def review(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    reviews = menu.reviews.all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    if request.method == "POST":
        rating = int(request.POST.get("rating"))
        comment = request.POST.get("comment", "")
        member = Member.objects.get(username=request.user.username)
        Review.objects.create(
            member=member,
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

        member_instance = get_object_or_404(Member, username=request.user.username)
        Order.objects.create(
            member=member_instance,
            menu=menu_item,
            quantity=quantity,
            total_price=final_price,
        )
        return redirect('my_menu')
    return redirect('buy', menu_id=menu_id)

@login_required
def my_menu(request):
    member_instance = get_object_or_404(Member, username=request.user.username)
    orders = Order.objects.filter(member=member_instance).order_by('-order_date')
    context = {
        'orders': orders,
    }
    return render(request, 'my_menu.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

# --- View สำหรับการจัดการเมนูในหน้า admin (เพิ่ม แก้ไข ลบ) ---

@login_required
def admin_edit_menu(request, menu_id):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("Access Denied")
    
    menu_item = get_object_or_404(Menu, id=menu_id)
    
    if request.method == "POST":
        form = MenuForm(request.POST, request.FILES, instance=menu_item)
        if form.is_valid():
            form.save()
            return redirect('custom_admin')
    else:
        # สร้างแบบฟอร์มที่แสดงข้อมูลเดิมของเมนู โดยไม่ดึงข้อมูลของฟิลด์ review
        form = MenuForm(instance=menu_item)
    
    context = {
        'form': form,
        'menu': menu_item,
    }
    return render(request, 'admin/edit_menu.html', context)

@login_required
def admin_delete_menu(request, menu_id):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("Access Denied")
    menu_item = get_object_or_404(Menu, id=menu_id)
    if request.method == "POST":
        menu_item.delete()
        return redirect('custom_admin')
    context = {
        'menu': menu_item,
    }
    return render(request, 'admin/confirm_delete_menu.html', context)

# --- View สำหรับการจัดการโปรโมชั่น (มีอยู่แล้วในตัวอย่างก่อนหน้า) ---

@login_required
def admin_add_promotion(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("Access Denied")
    
    if request.method == "POST":
        form = PromotionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('custom_admin')
    else:
        form = PromotionForm()
    
    return render(request, 'admin/add_promotion.html', {'form': form})

@login_required
def admin_edit_promotion(request, promo_id):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("Access Denied")
    
    promo = get_object_or_404(Promotion, id=promo_id)
    if request.method == "POST":
        form = PromotionForm(request.POST, request.FILES, instance=promo)
        if form.is_valid():
            form.save()
            return redirect('custom_admin')
    else:
        form = PromotionForm(instance=promo)
    
    return render(request, 'admin/edit_promotion.html', {'form': form, 'promo': promo})

@login_required
def admin_delete_promotion(request, promo_id):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("Access Denied")
    
    promo = get_object_or_404(Promotion, id=promo_id)
    if request.method == "POST":
        promo.delete()
        return redirect('custom_admin')
    
    return render(request, 'admin/confirm_delete_promotion.html', {'promo': promo})
