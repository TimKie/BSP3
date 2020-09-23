from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='GreenBot-home'),
    path('about/', views.about, name='GreenBot-about'),
    path('statistics/', views.ChartView.as_view(), name='GreenBot-statistics')
]