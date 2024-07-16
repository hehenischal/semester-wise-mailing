from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views 
from . import utils as util

urlpatterns = [
    path('', views.home, name='index'),
    path('base/', views.base, name='base'),
    path('create/mailing/', views.create_mailing, name='create_mailing'),
    path('confirm-mailing/<str:token>/', util.confirm_mailing, name='confirm_mailing'),
] 
