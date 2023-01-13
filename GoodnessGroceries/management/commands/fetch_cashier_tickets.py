from django.core.management.base import BaseCommand
from GoodnessGroceries.models import CashierTicketProducts, Users, StaticProducts
import os
import csv
from push_notifications.models import APNSDevice, GCMDevice
import os.path
from os import path
from datetime import datetime


class Command(BaseCommand):
    help = 'Fetch cashier tickets from URL, import to database and send push notifications to available devices'

    def handle(self, *args, **kwargs):
        # TODO: configuration of the CSV file
        date_column = 0
        hour_column = 1
        minute_column = 2
        participant_column = 12
        product_ref_column = 6
        quantity_column = 7
        price_column = 9
        store_column = 4
        ticket_number_column = 3
                        
        directory = '/home/admin/tickets'
        directory_done = '/home/admin/tickets_fetched'
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            # checking if it is a file
            if os.path.isfile(f) and os.path.splitext(f)[1]=='.csv':
                file = open(f, 'r', encoding="latin-1") 
                cr = csv.reader(file, delimiter=';')
                header = next(cr)
                if header != None:
                    for row in cr:
                        print(row)
                        try:
                            participant = Users.objects.only('participant_id').get(participant_id__contains=row[participant_column])
                        except Users.DoesNotExist:
                            continue
                        try:
                            product_ean = StaticProducts.objects.only('code').get(code=row[product_ref_column]).code
                        except StaticProducts.DoesNotExist:
                            continue
                        timestamp = row[date_column][0:4]+'-'+row[date_column][4:6]+'-'+row[date_column][6:8]+' '+row[hour_column]+':'+row[minute_column]+':00'
                        datestamp = row[date_column][0:4]+'-'+row[date_column][4:6]+'-'+row[date_column][6:8]
                        if participant.status == 'valid' and participant.phase2_date.strftime('%Y-%m-%d') <= (datetime.now()).strftime('%Y-%m-%d') and participant.phase1_date.strftime('%Y-%m-%d') <= datestamp:
                            if CashierTicketProducts.objects.filter(participant=participant,product_ean=product_ean).count() <2 and CashierTicketProducts.objects.filter(participant=participant,product_ean=product_ean,timestamp=timestamp).first() == None:
                                ticket = CashierTicketProducts.objects.create(participant=participant, timestamp=timestamp, product_ean=product_ean)
                productsToReview = {}
                for cashier_ticket in CashierTicketProducts.objects.filter(reviewed=False, notified=False).distinct('participant', 'product_ean'):
                    if not cashier_ticket.participant.participant_id in productsToReview:
                        productsToReview[cashier_ticket.participant.participant_id] = []
                    print(cashier_ticket.timestamp.strftime('%Y-%m-%d'))
                    if participant.phase2_date.strftime('%Y-%m-%d') <= cashier_ticket.timestamp.strftime('%Y-%m-%d'):
                        productsToReview[cashier_ticket.participant.participant_id].append(cashier_ticket.product_ean)
                        cashier_ticket.notified=True
                        cashier_ticket.save()
                for participant, products in productsToReview.items():
                    participant = Users.objects.get(participant_id=participant)

                    if participant.platform == 'ios':
                        for device in APNSDevice.objects.filter(name=participant.participant_id):
                            device.send_message("", extra={
                                'aps': {
                                    'mutable-content': 1,
                                    'alert': {
                                        'title': 'NOTIFICATION_REVIEW_PRODUCTS_TITLE',
                                        'body': 'NOTIFICATION_REVIEW_PRODUCTS_BODY'
                                    },
                                    'sound': 'default',
                                    'badge': len(products)
                                },
                                'products': list(map(lambda x: str(x), products))
                            })
                        print(list(map(lambda x: str(x), products)))
                        
                    elif participant.platform == 'android':
                        for device in GCMDevice.objects.filter(name=participant.participant_id):
                            try:    
                                device.send_message(None, extra={
                                    'data': {
                                        'mutable-content': 1,
                                        'alert': {
                                            'title': 'NOTIFICATION_REVIEW_PRODUCTS_TITLE',
                                            'body': 'NOTIFICATION_REVIEW_PRODUCTS_BODY'
                                        },
                                        'sound': 'default',
                                        'badge': len(products),
                                        'products': list(map(lambda x: str(x), products))
                                    }
                                })
                                print(list(map(lambda x: str(x), products)))
                            except:
                                pass
                file.close()
                os.rename(os.path.join(directory, filename), os.path.join(directory_done, datetime.now().strftime('%Y%m%d%H%M%S') + filename))
            else:
                print(os.path.splitext(f))
                os.rename(os.path.join(directory, filename), os.path.join(directory_done, filename))
                
