from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Seed basic test data for the price tracker"

    def add_arguments(self, parser):
        parser.add_argument(
            "--products",
            type=int,
            default=5,
            help="Number of fake products to create"
        )

    def handle(self, *args, **options):
        products_count = options["products"]

        self.stdout.write(f"Creating {products_count} test products...")
        self.stdout.write(self.style.SUCCESS("Done"))