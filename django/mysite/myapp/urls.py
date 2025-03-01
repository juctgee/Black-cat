from django.urls import path
from . import views
from django.urls import include

from .views import SignUpView
from django.contrib.auth.views import LogoutView


urlpatterns = [
   path('accounts/', include('django.contrib.auth.urls')),
   path('accounts/sign_up/', SignUpView.as_view(), name='sign_up'),
   path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
   path('', views.home, name='home'),
   path('menu/', views.menu, name='menu'),
   path('members/', views.members, name='members'),
]
