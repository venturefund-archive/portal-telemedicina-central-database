from django.core.management.base import BaseCommand
from patients.factories import VaccineStatusFactory


class Command(BaseCommand):
    help = "A command to populate database"

    def handle(self, *args, **options):
        print("Start Seeding...")

        [VaccineStatusFactory() for _ in range(5000)]
