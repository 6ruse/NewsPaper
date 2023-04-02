from django.core.management.base import BaseCommand, CommandError
from news.models import Category, Post

class Command(BaseCommand):
    help = 'Удаление новостей указанной категории'
    missing_args_message = 'Недостаточно аргументов'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        self.stdout.readable()
        self.stdout.write('Действительно удалить новости выбранной категрии ? y/n')
        answer = input()
        if answer == 'y':
            cat = Category.objects.get(nm_category=options['category'])
            Post.objects.filter(category=cat).delete()
            self.stdout.write(self.style.SUCCESS('Удаление выполнено!'))
            return

        self.stdout.write(self.style.ERROR('Удаление не выполнялось'))