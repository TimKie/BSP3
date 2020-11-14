from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='GoodnessGroceries-home'),
    path('about/', views.about, name='GoodnessGroceries-about'),
    path('product_overview/', views.product_overview, name='GoodnessGroceries-product_overview'),

    # Statistics URLs
    path('most_expensive_products/', views.MostExpensiveProducts.as_view(), name='GoodnessGroceries-most_expensive_products'),
    path('most_sold_products/', views.MostSoldProducts.as_view(), name='GoodnessGroceries-most_sold_products'),
    path('most_popular_indicators/', views.MostPopularIndicators.as_view(), name='GoodnessGroceries-most_popular_indicators'),
    path('most_popular_product_types/', views.MostPopularProductTypes.as_view(), name='GoodnessGroceries-most_popular_product_types'),

    # API URLs
    path('api-auth/', include('rest_framework.urls')),
    path('get_bought_products/<int:participant_id>/', views.GetBoughtProducts.as_view(), name='GoodnessGroceries-GetBoughtProducts'),
    path('post_monitoring_data/', views.PostMonitoringData.as_view(), name='GoodnessGroceries-PostMonitoringData'),
    path('post_product_review/', views.PostProductsReview.as_view(), name='GoodnessGroceries-PostProductsReview'),
    path('fetch_user_status/<int:participant_id>/', views.FetchUserStatus.as_view(), name='GoodnessGroceries-FetchUserStatus'),
    path('request_user_access/', views.RequestUserAccess.as_view(), name='GoodnessGroceries-RequestUserAccess'),

    # Download URL
    path('products_data/', views.CSVFileView.as_view(), name='GoodnessGroceries-csv_download'),

    # Upload Static Files URLs
    path('upload_static_products/', views.static_products_upload, name='GoodnessGroceries-upload_static_products'),
    path('upload_static_indicators/', views.static_indicators_upload, name='GoodnessGroceries-upload_static_indicators'),
    path('upload_static_indicator_categories/', views.static_indicator_categories_upload, name='GoodnessGroceries-upload_static_indicator_categories')
]
