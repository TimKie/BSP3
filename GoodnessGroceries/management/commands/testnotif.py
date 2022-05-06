
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.views.generic import View
import io
import os
from glob import glob
import pandas as pd
from .filters import *
from .serializers import CashierTicketProductsSerializer, ProductReviewsSerializer, UsersSerializer, UsersStatusSerializer
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .models import *
from .functions import handle_product_reviews
from datetime import datetime
from datetime import timedelta
from push_notifications.models import APNSDevice, 

user = Users.objects.get(participant_id='4444444444444')

if user.platform == 'android':
  for device in GCMDevice.objects.filter(name=user.participant_id):
    device.send_message("", extra={
        'aps': {
            'mutable-content': 1,
            'alert': {
                'title': 'NOTIFICATION_ACCOUNT_AUTHENTICATED_TITLE',
                'body': 'NOTIFICATION_ACCOUNT_AUTHENTICATED_BODY'
            },
            'sound': 'default',
            'badge': 1
        }
    })
