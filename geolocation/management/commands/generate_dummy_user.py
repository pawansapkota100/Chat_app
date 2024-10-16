from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

User = get_user_model()

class Command(BaseCommand):
    help = "Generate a specified number of users"

    def add_arguments(self, parser):
        parser.add_argument("users_number", type=int, help="number of users")

    def handle(self, *args, **kwargs):
        users_number = kwargs["users_number"]  # Get the number of users from command line arguments

        faker = Faker()
        for _ in range(users_number):  # Use range to iterate the specified number of times
            email = faker.email()
            password = faker.password()
            User.objects.create_user(email=email, password=password)  # Use create_user for proper password handling

        self.stdout.write(self.style.SUCCESS(f'{users_number} users created successfully!'))
