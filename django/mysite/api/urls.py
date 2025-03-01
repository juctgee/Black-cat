from django.urls import path
from .views import *
urlpatterns = [
    path('menu_list/', menu_list, name='menu_list'),
    path('total_sales/', total_sales, name='total_sales'),
    path('new_members/', new_members, name='new_members'),
    path('monthly_sales/', monthly_sales, name='monthly_sales'),
    path('upcoming_events/', upcoming_events, name='upcoming_events'),
     path('member_list/', member_list, name='member_list'),
]
