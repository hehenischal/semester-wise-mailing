from django.urls import path
from . import views

urlpatterns = [
    path('batches/', views.batches, name='batches'),
    path('batches/list/', views.batch_list, name='batch_list'),
    # path('batches/<int:pk>/', views.batch_detail, name='batch_detail'),
    path('batches/create/', views.batch_create, name='batch_create'),
    path('batches/<int:pk>/edit/', views.batch_update, name='batch_update'),
    path('batches/<int:pk>/delete/', views.batch_delete, name='batch_delete'),
]
