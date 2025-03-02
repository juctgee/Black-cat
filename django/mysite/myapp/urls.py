from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import SignUpView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # URL สำหรับระบบ authentication ของ Django
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/sign_up/', SignUpView.as_view(), name='sign_up'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

    # URL หลัก
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('members/', views.user_dashboard, name='members'),
    path('buy/<int:menu_id>/', views.buy, name='buy'),
    path('reviews/<int:menu_id>/', views.review, name='review'),
    path('buy/<int:menu_id>/process_order/', views.process_order, name='process_order'),
    path('my_menu/', views.my_menu, name='my_menu'),
    
    # URL สำหรับ Custom Admin Dashboard และการจัดการโปรโมชั่น
    path('back_office/', views.custom_admin_dashboard, name='custom_admin'),
    path('back_office/promotion/add/', views.admin_add_promotion, name='admin_add_promotion'),
    path('back_office/promotion/edit/<int:promo_id>/', views.admin_edit_promotion, name='admin_edit_promotion'),
    path('back_office/promotion/delete/<int:promo_id>/', views.admin_delete_promotion, name='admin_delete_promotion'),
    
    # URL สำหรับการจัดการเมนูในหน้า admin
    path('back_office/menu/edit/<int:menu_id>/', views.admin_edit_menu, name='admin_edit_menu'),
    path('back_office/menu/delete/<int:menu_id>/', views.admin_delete_menu, name='admin_delete_menu'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
