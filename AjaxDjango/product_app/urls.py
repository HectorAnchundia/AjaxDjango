"""
URL patterns for the product_app application.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/test-connection/', views.test_connection, name='test_connection'),
    path('api/insert/', views.insert_data, name='insert_data'),
    path('api/delete/', views.delete_data, name='delete_data'),
]