from django.core.management.base import BaseCommand
from GoodnessGroceries.models import CashierTicketProducts, Users
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
        participant_column = 2
        product_ref_column = 3
        product_column = 4
        quantity_column = 5
        price_column = 6
        store_column = 7
                        
        file_url = '/home/pall_user/tickets.csv'
        if path.exists(file_url):
            #with requests.Session() as s:
            #download = s.get(file_url)
            file = open(filename, 'r')
            content = file.read()
            file.close()
            os.rename('/home/pall_user/tickets.csv', '/home/pall_user/tickets_fetched.csv')
            decoded_content = content.content.decode('utf-8')

            cr = csv.reader(decoded_content.splitlines(), delimiter=';')
            header = next(cr)
            if header != None:
                for row in cr:
                    print(row)
                    try:
                        participant = Users.objects.only(
                            'participant_id').get(participant_id='220000'+row[participant_column])
                    except Users.DoesNotExist:
                        continue
                    timestamp = row[date_column][0:4]+'-'+row[date_column][4:6]+'-'+row[date_column][6:8]+' '+row[time_column][0:2]+':'+row[time_column][3:5]+':'+row[time_column][6:8]
                    product_ean = row[product_ref_column]
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
