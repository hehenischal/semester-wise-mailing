from django.urls import path
from . import views

urlpatterns = [
    path('track/<uuid:token>/', views.track, name='track'),
    #example uuid token:    
]