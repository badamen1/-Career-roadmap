from django.core.management.base import BaseCommand
from roadmap.models import Intereses
import json

# Command to load Intereses from a JSON file

class Command(BaseCommand):
    help = 'Carga intereses desde un archivo JSON'

    def handle(self, *args, **kwargs):
        json_file_path = 'roadmap/management/commands/intereses.json'

        # Load data from the JSON file
        with open(json_file_path, 'r') as file:
            intereses_data = json.load(file)
        
        for interes in intereses_data:
            exist = Intereses.objects.filter(name=interes['name']).first()
            if not exist:
                Intereses.objects.create(
                    name=interes['name'],
                    description=interes['description'],
                    color=interes['color']
                )
                self.stdout.write(self.style.SUCCESS(f'Interés "{interes["name"]}" agregado.'))
            else:
                self.stdout.write(self.style.WARNING(f'El interés "{interes["name"]}" ya existe.'))