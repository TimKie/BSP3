from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='GoodnessGroceries-home'),
    path('about/', views.about, name='GoodnessGroceries-about'),
    path('most_expensive_products/', views.MostExpensiveProducts.as_view(), name='GoodnessGroceries-most_expensive_products'),
    path('product_overview/', views.product_overview, name='GoodnessGroceries-product_overview'),
    path('most_sold_products/', views.MostSoldProducts.as_view(), name='GoodnessGroceries-most_sold_products'),
    path('most_popular_indicators/', views.MostPopularIndicators.as_view(), name='GoodnessGroceries-most_popular_indicators'),
    path('most_popular_product_types/', views.MostPopularProductTypes.as_view(), name='GoodnessGroceries-most_popular_product_types')
]