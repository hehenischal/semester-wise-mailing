from django.urls import path
from . import views

urlpatterns = [
    path('track/<uuid:token>/', views.track, name='track'),
    #example uuid token: 123e4567-e89b-12d3-a456-426614174000
]