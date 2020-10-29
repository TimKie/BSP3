from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='GoodnessGroceries-home'),
    path('about/', views.about, name='GoodnessGroceries-about'),
    path('most_expensive_products/', views.MostExpensiveProducts.as_view(), name='GoodnessGroceries-most_expensive_products'),
    path('product_overview/', views.product_overview, name='GoodnessGroceries-product_overview'),
    path('most_sold_products/', views.MostSoldProducts.as_view(), name='GoodnessGroceries-most_sold_products'),
    path('most_popular_indicators/', views.MostPopularIndicators.as_view(), name='GoodnessGroceries-most_popular_indicators'),
    path('most_popular_product_types/', views.MostPopularProductTypes.as_view(), name='GoodnessGroceries-most_popular_product_types'),
    path('api-auth/', include('rest_framework.urls')),
    path('products_api_view/', views.ProductsAPIView.as_view(), name='GoodnessGroceries-ProductsAPIView'),
    path('monitoring_data_api_view/', views.MonitoringDataAPIView.as_view(), name='GoodnessGroceries-MonitoringDataAPIView'),
    path('product_reviews_api_view/', views.ProductsReviewAPIView.as_view(), name='GoodnessGroceries-ProductsReviewAPIView'),
    path('users_api_view/', views.UsersAPIView.as_view(), name='GoodnessGroceries-UsersAPIView')
]
