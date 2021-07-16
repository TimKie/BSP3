from django.core.management.base import BaseCommand
from GoodnessGroceries.models import CashierTicketProducts, Users
import os
from csv import reader


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        participant_column = 0
        timestamp_column = 1
        product_column = 2

        path = os.getcwd() + "/Dropbox/share/json files/tim input/cashier_tickets_combined.csv"

        with open(path, 'r') as file:
            csv_reader = reader(file)
            header = next(csv_reader)
            if header != None:
                for row in csv_reader:
                    participant = Users.objects.only(
                        'participant_id').get(participant_id=row[participant_column])
                    timestamp = row[timestamp_column]
                    product_ean = row[product_column]

                    ticket = CashierTicketProducts.objects.create(
                        participant=participant, timestamp=timestamp, product_ean=product_ean)
