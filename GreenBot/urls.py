from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='GreenBot-home'),
    path('about/', views.about, name='GreenBot-about'),
    path('most_expensive_products/', views.MostExpensiveProducts.as_view(), name='GreenBot-most_expensive_products'),
    path('product_overview/', views.product_overview, name='GreenBot-product_overview'),
    path('most_sold_products/', views.MostSoldProducts.as_view(), name='GreenBot-most_sold_products')
]