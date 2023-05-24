import csv
import os

from django.conf import settings
from django.core.management import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка из csv файла'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, "ingredients.csv")
        ingredients_to_create = []
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=",")
                for row in reader:
                    name, measurement_unit = row.values()
                    ingredient = Ingredient(
                        name=name,
                        measurement_unit=measurement_unit
                    )
                    ingredients_to_create.append(ingredient)
            Ingredient.objects.bulk_create(ingredients_to_create)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(
                f"Файл '{file_path}' не найден.")
            )
        except csv.Error as e:
            self.stdout.write(self.style.ERROR(
                f"Ошибка при чтении CSV файла: {str(e)}")
            )
        else:
            self.stdout.write(self.style.SUCCESS('Все ингридиенты загружены!'))
