from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = 'Create tokens for all users in the system'

    def handle(self, *args, **options):
        User = get_user_model()
        users = User.objects.all()
        
        created_count = 0
        for user in users:
            token, created = Token.objects.get_or_create(user=user)
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created token for user: {user.username}')
                )
            else:
                self.stdout.write(f'Token for user {user.username} already exists')

        self.stdout.write(
            self.style.SUCCESS(f'Total new tokens created: {created_count}')
        )
