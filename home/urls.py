from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views 

urlpatterns = [
    path('', views.home, name='index'),
    path('base/', views.base, name='base'),
    path('create/mailing/', views.create_mailing, name='create_mailing'),
    path('confirm-mailing/<str:token>/', views.confirm_mailing, name='confirm_mailing'),
    path('update/<int:pk>/', views.update_mailing, name='update_mailing'),
    path('view/<int:pk>/', views.view_mailing, name='view_mailing'),
] 
