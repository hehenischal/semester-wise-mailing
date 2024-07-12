from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('404/', views.error_404, name='error_404'),
    path('base/', views.base, name='base'),
]
