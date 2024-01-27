import csv
import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Load ingredients from CSV or JSON file'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help='Path to the CSV or JSON file'
        )

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        if file_path.endswith('.json'):
            self.load_from_json(file_path)
        elif file_path.endswith('.csv'):
            self.load_from_csv(file_path)
        else:
            self.stdout.write(self.style.ERROR('Unsupported file format'))

    def load_from_json(self, file_path):
        total_loaded = 0  # Initialize the total count to 0

        with open(file_path, 'r', encoding='utf-8') as json_file:
            ingredients_data = json.load(json_file)

        for ingredient_data in ingredients_data:
            _, created = Ingredient.objects.get_or_create(
                name=ingredient_data['name'],
                measurement_unit=ingredient_data['measurement_unit']
            )
            if created:
                total_loaded += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully loaded ingredients from CSV. | '
                f'Total loaded: {total_loaded} | '
                f'Total ingredients in db: {Ingredient.objects.count()}'
            )
        )

    def load_from_csv(self, file_path):
        total_loaded = 0  # Initialize the total count to 0

        with open(file_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)

            for name, measurement_unit in csv_reader:
                _, created = Ingredient.objects.get_or_create(
                    name=name,
                    measurement_unit=measurement_unit
                )
                if created:
                    total_loaded += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully loaded ingredients from CSV. | '
                f'Total loaded: {total_loaded} | '
                f'Total ingredients in db: {Ingredient.objects.count()}'
            )
        )
