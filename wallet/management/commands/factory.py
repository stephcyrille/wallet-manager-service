from django.core.management.base import BaseCommand
from .wallet import generate_wallet
from .blockchain import generate_blockchain


class Command(BaseCommand):
    help = 'Setting base wallet configuration'

    def add_arguments(self, parser):
        parser.add_argument('-d', '--data', type=str, help='Help to say which type of data we will init')

    def handle(self, *args, **kwargs):
        data = kwargs['data']

        if "wallet" == data:
            generate_wallet()

        elif "blockchain" == data:
            generate_blockchain()

        else:
            print("You need to say the data that you want to create")
