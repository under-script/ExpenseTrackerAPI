from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Reset the sequence of a specified model in the database'

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='The name of the model to reset the sequence for')

    def handle(self, *args, **kwargs):
        model_name = kwargs['model_name']

        # Get the model from the model name
        try:
            model = apps.get_model('api', model_name)
        except LookupError:
            self.stdout.write(self.style.ERROR(f"Model '{model_name}' not found in 'api' app"))
            return

        # Delete all existing records
        model.objects.all().delete()

        # Get the current database engine
        db_engine = connection.vendor

        with connection.cursor() as cursor:
            if db_engine == 'sqlite':
                # For SQLite
                cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{model._meta.db_table}';")

        self.stdout.write(self.style.SUCCESS(f'Successfully reset the sequence for {model_name}'))
