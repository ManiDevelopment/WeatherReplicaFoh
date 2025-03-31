from django.core.management.base import BaseCommand
from MySourceReplica.models import City

class Command(BaseCommand):
    help = 'Adds a few test cities for dev stuff'

    def handle(self, *args, **kwargs):
        cities = ['London', 'Tokyo', 'Paris', 'Guildford']
        for name in cities:
            City.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS("Sample cities added ✅"))
