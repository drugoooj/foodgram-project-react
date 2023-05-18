import csv
import os

from django.conf import settings
from django.core.management import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка из csv файла'

    def handle(self, *args, **kwargs):
        with open(
            os.path.join(settings.BASE_DIR, "ingredients.csv"),
            'r',
            encoding='utf-8'
        ) as file:
            reader = csv.DictReader(file, delimiter=",")
            for row in reader:
                Ingredient.objects.bulk_create(
                    name=row[0],
                    measurement_unit=row[1]
                )
        self.stdout.write(self.style.SUCCESS('Все ингридиенты загружены!'))
