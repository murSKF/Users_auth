from django.core.management.base import BaseCommand
from news.models import Post, Category

class Command(BaseCommand):
    help = 'Удаляет все посты из указанной категории (с подтверждением)'

    def add_arguments(self, parser):
        parser.add_argument('category_id', type=int, help='ID категории')

    def handle(self, *args, **options):
        category_id = options['category_id']

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR('Категория не найдена'))
            return
        
        posts = Post.objects.filter(categories=category)

        count = posts.count()

        if count == 0:
            self.stdout.write(self.style.WARNING('В этой категории нет постов'))
            return
        
        # Подтверждение
        confirm = input(
            f'Удалить {count} пост(ов) из категории "{category.name}"? (yes/no): '
        )

        if confirm.lower() == 'yes':
            posts.delete()
            self.stdout.write(self.style.SUCCESS('Посты удалены'))
        else:
            self.stdout.write(self.style.WARNING('Удаление отменено'))