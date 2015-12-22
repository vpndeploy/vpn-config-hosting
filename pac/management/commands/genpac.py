from django.core.management.base import BaseCommand, CommandError
from pac.models import PacGenerator

class Command(BaseCommand):
    help = 'Generate Pac file'

    def add_arguments(self, parser):
        parser.add_argument('mode')
        parser.add_argument('server', nargs="+")
        parser.add_argument('out')

    def handle(self, *args, **options):
        with open(options['out'], 'w') as fp:
            fp.write(PacGenerator.generate(options['mode'], options['server']))
