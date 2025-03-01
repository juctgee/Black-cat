from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.db.models import Count

from .models import Menu # สมมุติว่า models อยู่ในไฟล์ models.py


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

def home(req):
    # ดึงข้อมูลเมนูพร้อมคำนวณจำนวนรีวิว จากนั้นจัดเรียงจากมากไปน้อย
    best_selling_menus = Menu.objects.annotate(num_reviews=Count('reviews')).order_by('-num_reviews')
    context = {
        'best_selling_menus': best_selling_menus,
    }
    return render(req, 'index.html', context)

def menu(req):
    # ดึงข้อมูลเมนูทั้งหมดมาแสดง
    menus = Menu.objects.all()
    context = {
        'menus': menus,
    }
    return render(req, 'menu.html', context)

@login_required
def members(req):
    context = {
        'username': req.user.username,
    }
    return render(req, 'members.html', context)

def register(req):
    return render(req, 'register.html')

def logout_view(req):  # เปลี่ยนชื่อฟังก์ชัน logout เพื่อไม่ให้ชนกับการนำเข้าจาก django.contrib.auth
    return redirect('login')
