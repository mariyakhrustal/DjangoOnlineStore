from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from catalog.models import Product, Category


class Command(BaseCommand):
    help = "Delete old data and load test data from fixture"

    def handle(self, *args, **options):
        self.stdout.write("Удаление старых данных...")
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write("Загрузка категорий из фикстуры...")
        try:
            call_command("loaddata", "category_fixture.json", format="json")
        except Exception as e:
            raise CommandError(f"Не удалось загрузить категории: {e}")

        self.stdout.write("Загрузка продуктов из фикстуры...")
        try:
            call_command("loaddata", "product_fixture.json", format="json")
        except Exception as e:
            raise CommandError(f"Не удалось загрузить продукты: {e}")

        self.stdout.write(self.style.SUCCESS("Данные успешно загружены из фикстур!"))
