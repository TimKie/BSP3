from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='GoodnessGroceries-home'),
    path('about/', views.about, name='GoodnessGroceries-about'),
    path('product_overview/', views.product_overview, name='GoodnessGroceries-product_overview'),
    path('user_overview/', views.user_overview, name='GoodnessGroceries-user_overview'),
    path('user_overview/<int:participant_id>/', views.user_overview_filtered, name='GoodnessGroceries-user_overview_filtered'),
    path('update_status_of_users/<int:participant_id>/', views.update_status_of_user, name='GoodnessGroceries-update_status_of_users'),
    path('product_reviews_overview/', views.product_reviews_overview, name='GoodnessGroceries-product_reviews_overview'),
    path('product_reviews_overview/<int:participant_id>/', views.product_reviews_overview_filtered, name='GoodnessGroceries-product_reviews_overview_filtered'),

    # Statistics URLs
    path('most_popular_indicators/', views.MostPopularIndicators.as_view(), name='GoodnessGroceries-most_popular_indicators'),
    path('most_popular_product_types/', views.MostPopularProductTypes.as_view(), name='GoodnessGroceries-most_popular_product_types'),

    # API URLs
    path('api-auth/', include('rest_framework.urls')),
    path('get_bought_products/<int:participant_id>/', views.GetBoughtProducts.as_view(), name='GoodnessGroceries-GetBoughtProducts'),
    path('post_monitoring_data/', views.PostMonitoringData.as_view(), name='GoodnessGroceries-PostMonitoringData'),
    path('post_product_review/', views.PostProductsReview.as_view(), name='GoodnessGroceries-PostProductsReview'),
    path('fetch_user_status/<int:participant_id>/', views.FetchUserStatus.as_view(), name='GoodnessGroceries-FetchUserStatus'),
    path('request_user_access/', views.RequestUserAccess.as_view(), name='GoodnessGroceries-RequestUserAccess'),

    # Import - Export
    path('import_export/', views.ImportExportView, name='GoodnessGroceries-import_export'),

    # Dynamic Files Download
    path('download_cashier_ticket_products/', views.CashierTicketsProductsDownload.as_view(), name='GoodnessGroceries-download_cashier_ticket_products'),
    path('download_product_reviews/', views.ProductReviewsDownload.as_view(), name='GoodnessGroceries-download_product_reviews'),
    path('download_monitoring_data/', views.MonitoringDataDownload.as_view(), name='GoodnessGroceries-download_monitoring_data'),
    path('download_users/', views.UsersDownload.as_view(), name='GoodnessGroceries-download_users'),

    # Static Files Download
    path('download_static_products/', views.StaticProductsDownload.as_view(), name='GoodnessGroceries-download_static_products'),
    path('download_static_indicators/', views.StaticIndicatorsDownload.as_view(), name='GoodnessGroceries-download_static_indicators'),
    path('download_static_indicator_categories/', views.StaticIndicatorCategoriesDownload.as_view(), name='GoodnessGroceries-download_static_indicator_categories'),

    # Static Files Upload
    path('upload_static_products/', views.static_products_upload, name='GoodnessGroceries-upload_static_products'),
    path('upload_static_indicators/', views.static_indicators_upload, name='GoodnessGroceries-upload_static_indicators'),
    path('upload_static_indicator_categories/', views.static_indicator_categories_upload, name='GoodnessGroceries-upload_static_indicator_categories')
]
