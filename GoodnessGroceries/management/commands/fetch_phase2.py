from django.core.management.base import BaseCommand
from GoodnessGroceries.models import Users
from push_notifications.models import APNSDevice
from datetime import datetime

class Command(BaseCommand):
    help = 'Send notif when Phase 2 start.'

    def handle(self, *args, **kwargs):
        for user in Users.objects.filter(status='valid'):
            if user.phase2_date:
                if user.phase2_date.strftime('%Y-%m-%d') == (datetime.now()).strftime('%Y-%m-%d'):
                    if user.platform == 'ios':
                        for device in APNSDevice.objects.filter(name=user.participant_id):
                            device.send_message("", extra={
                                'aps': {
                                    'mutable-content': 1,
                                    'alert': {
                                        'title': 'NOTIFICATION_ACCOUNT_PHASE2_TITLE',
                                        'body': 'NOTIFICATION_ACCOUNT_PHASE2_BODY'
                                    },
                                    'sound': 'default',
                                    'badge': 1
                                }
                            })
                    elif user.platform == 'android':
                       for device in GCMDevice.objects.filter(name=user.participant_id):
                            try:    
                                device.send_message("", extra={
                                    'aps': {
                                        'mutable-content': 1,
                                        'alert': {
                                            'title': 'NOTIFICATION_ACCOUNT_PHASE2_TITLE',
                                            'body': 'NOTIFICATION_ACCOUNT_PHASE2_BODY'
                                        },
                                        'sound': 'default',
                                        'badge': 1
                                    }
                                })
                            except:
                                pass
                
