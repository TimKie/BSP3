from django.core.management.base import BaseCommand
from GoodnessGroceries.models import CashierTicketProducts, Users, StaticProducts
import os
import csv
from push_notifications.models import APNSDevice, GCMDevice
import os.path
from os import path



class Command(BaseCommand):
    help = 'Fetch cashier tickets from URL, import to database and send push notifications to available devices'

    def handle(self, *args, **kwargs):
        # TODO: configuration of the CSV file
        date_column = 0
        time_column = 1
        participant_column = 11
        product_ref_column = 5
        product_column = 6
        quantity_column = 7
        price_column = 8
        store_column = 3
                        
        directory = '/home/admin/tickets'
        directory_done = '/home/admin/tickets_fetched'
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            # checking if it is a file
            if os.path.isfile(f) and os.path.splitext(f)[1]=='.csv':
                file = open(f, 'r', encoding="latin-1") 
                cr = csv.reader(file, delimiter=';')
                print(cr)
                header = next(cr)
                if header != None:
                    for row in cr:
                        print(row)
                        try:
                            participant = Users.objects.only('participant_id').get(participant_id='2200000'+row[participant_column])
                        except Users.DoesNotExist:
                            continue
                        try:
                            product_ean = StaticProducts.objects.only('code').get(code=row[product_ref_column])
                        except StaticProducts.DoesNotExist:
                            continue
                        timestamp = row[date_column][0:4]+'-'+row[date_column][4:6]+'-'+row[date_column][6:8]+' '+row[time_column][0:2]+':'+row[time_column][3:5]+':'+row[time_column][6:8]
                        #product_ean = row[product_ref_column]
                        ticket = CashierTicketProducts.objects.create(
                            participant=participant, timestamp=timestamp, product_ean=product_ean)

                productsToReview = {}
                for cashier_ticket in CashierTicketProducts.objects.filter(reviewed=False).distinct('participant', 'product_ean'):
                    if not cashier_ticket.participant.participant_id in productsToReview:
                        productsToReview[cashier_ticket.participant.participant_id] = []
                    productsToReview[cashier_ticket.participant.participant_id].append(
                        cashier_ticket.product_ean)

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
                        # TODO
                        pass
                file.close()
                os.rename(os.path.join(directory, filename), os.path.join(directory_done, filename))
            else:
                print(os.path.splitext(f))
                os.rename(os.path.join(directory, filename), os.path.join(directory_done, filename))
                
