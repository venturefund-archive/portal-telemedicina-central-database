from django.core.management.base import BaseCommand
from django.utils import timezone
from vaccines.models import ImmunizationRecommendation

class Command(BaseCommand):
    help = 'Update overdue immunization recommendations'

    def handle(self, *args, **options):
        overdue_recommendations = ImmunizationRecommendation.objects.filter(
            due_date__lt=timezone.now(),
            forecast_status__in=['due', 'immune']
        )
        
        updated_count = overdue_recommendations.update(forecast_status='overdue')
        
        self.stdout.write(self.style.SUCCESS(f'Updated {updated_count} recommendations to overdue status'))
