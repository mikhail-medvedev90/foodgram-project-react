import csv

from django.core.management.base import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    help = 'Load data from a CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help='Path to the CSV file'
        )

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        total_loaded = 0

        with open(file_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)

            for name, slug, color in csv_reader:
                _, created = Tag.objects.get_or_create(
                    name=name,
                    slug=slug,
                    color=color
                )

                if created:
                    total_loaded += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully loaded ingredients from CSV. | '
                f'Total loaded: {total_loaded} | '
                f'Total ingredients in db: {Tag.objects.count()}'
            )
        )
