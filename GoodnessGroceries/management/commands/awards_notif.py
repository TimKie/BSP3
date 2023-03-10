from django.core.management.base import BaseCommand
from GoodnessGroceries.models import Users
from push_notifications.models import APNSDevice
from datetime import datetime

class Command(BaseCommand):
    help = 'Send notif for Awards.'

    def handle(self, *args, **kwargs):
        for user in Users.objects.filter(status='valid'):
            if user.participant_id == "2200000000006":
                    if user.platform == 'ios':
                        for device in APNSDevice.objects.filter(name=user.participant_id):
                             try:   
                                device.send_message("", extra={
                                    'aps': {
                                        'mutable-content': 1,
                                        'alert': {
                                            'title': 'Gagnez 150€',
                                            'body': 'Donnez votre feedback'
                                        },
                                        'sound': 'default',
                                        'badge': 1
                                    }
                                })
                             except:
                                pass
                                
                    elif user.platform == 'android':
                       for device in GCMDevice.objects.filter(name=user.participant_id):
                            try:    
                                device.send_message(None, extra={
                                    'data': {
                                        'mutable-content': 1,
                                        'alert': {
                                            'title': 'Gagnez 150€',
                                            'body': 'Donnez votre feedback'
                                        },
                                        'sound': 'default',
                                        'badge': 1
                                    }
                                })
                            except:
                                pass
