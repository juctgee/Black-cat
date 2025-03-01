from django.urls import path
from . import views
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

from .views import SignUpView
from django.contrib.auth.views import LogoutView


urlpatterns = [
   path('accounts/', include('django.contrib.auth.urls')),
   path('accounts/sign_up/', SignUpView.as_view(), name='sign_up'),
   path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
   path('', views.home, name='home'),
   path('menu/', views.menu, name='menu'),
   path('members/', views.members, name='members'),
   path('buy/<int:menu_id>/', views.buy, name='buy'),
   path('reviews/<int:menu_id>/', views.review, name='review'),
   path('buy/<int:menu_id>/process_order/', views.process_order, name='process_order'),
   path('my_menu/', views.my_menu, name='my_menu'),  # คุณต้องสร้าง view my_menu ด้วย

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)