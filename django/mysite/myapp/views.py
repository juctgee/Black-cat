from django.shortcuts import redirect, render

from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout


from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
# Create your views here.

def home(req):
    return render(req, 'index.html')

def menu(req):
    return render(req, 'menu.html')

@login_required
def members(req):
    context = {
        'username': req.user.username,
    }
    return render(req, 'members.html', context)

def register(req):
    return render(req, 'register.html')

def logout(req):
    return redirect('login')

from django.shortcuts import render
from .models import MenuItem

def menu_list(request):
    menus = MenuItem.objects.all()
    return render(request, "menu.html", {"menus": menus})
