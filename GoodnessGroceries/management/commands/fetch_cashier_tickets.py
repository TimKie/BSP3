from django.core.management.base import BaseCommand
from GoodnessGroceries.models import CashierTicketProducts, Users
import os
import csv
from push_notifications.models import APNSDevice, GCMDevice
import requests

class Command(BaseCommand):
    help = 'Fetch cashier tickets from URL, import to database and send push notifications to available devices'

    def handle(self, *args, **kwargs):
        # TODO: configuration of the CSV file
        participant_column = 0
        timestamp_column = 1
        product_column = 2
        file_url = 'https://drive.google.com/uc?export=download&id=1q5eyMVddf5o6KcFfxmQSsycOs2GfIbnl'

        with requests.Session() as s:
            download = s.get(file_url)

            decoded_content = download.content.decode('utf-8')

            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            header = next(cr)
            if header != None:
                for row in cr:
                    try:
                        participant = Users.objects.only(
                            'participant_id').get(participant_id=row[participant_column])
                    except Users.DoesNotExist:
                        continue

                    timestamp = row[timestamp_column]
                    product_ean = row[product_column]

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
            elif participant.platform == 'android':
                # TODO
                pass
