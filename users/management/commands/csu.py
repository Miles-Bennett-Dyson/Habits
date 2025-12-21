from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Создание суперпользователя'

    def handle(self, *args, **options):
        try:
            user = User.objects.create(email='super@user.com', username = 'Admin')
            user.is_staff = True
            user.is_active = True
            user.is_superuser = True
            user.set_password('admin')
            user.save()
            self.stdout.write(self.style.SUCCESS('Супер-пользователь создан. \n email = super@user.com \n password =  admin '))
        except Exception as e:
            self.stdout.write(
                self.style.DANGER(f'Ошибка создания супер-пользователя: {e}'))
