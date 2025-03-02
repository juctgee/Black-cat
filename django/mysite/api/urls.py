from django.urls import path # type: ignore
from .views import *
from . import views

urlpatterns = [
    path('menu_list/', menu_list, name='menu_list'),
    path('total_sales/', total_sales, name='total_sales'),
    path('new_members/', new_members, name='new_members'),
    path('monthly_sales/', monthly_sales, name='monthly_sales'),
    path('upcoming_events/', upcoming_events, name='upcoming_events'),
    path('member_list/', member_list, name='member_list'),
    path('order_list/', order_list, name='order_list'),
    path('order_by_date/', order_by_date, name='order_by_date'),
    path('best_selling_menus/', best_selling_menus, name='best_selling_menus'),  # เพิ่มตรงนี้
    path('orders_by_date/', order_by_date, name='orders-by-date'),
    path('promotion_list/', views.promotion_list, name='promotion_list'),
    path('promotion/', views.add_promotion, name='add_promotion'),
    path('promotion/<int:promo_id>/', views.delete_promotion, name='delete_promotion'),
]
