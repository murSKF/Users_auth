from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.core.mail import EmailMultiAlternatives

from news.models import Post, Category

class Command(BaseCommand):
    help = 'Weekly articles digest'

    def handle(self, *args, **options):
        week_ago = timezone.now() - timedelta(days=7)

        articles = Post.objects.filter(
            type='AR',
            created_at__gte=week_ago
        )

        for category in Category.objects.all():
            category_articles = articles.filter(categories=category)

            if not category_articles.exists():
                continue

            for user in category.subscribers.all():
                subject = f'Новые статьи категории "{category.name}"'

                text = (
                    f'Здравствуй, {user.username}!\n\n'
                    f'Новые статьи за неделю:\n'
                )

                html = f'<h2>Новые статьи в категории "{category.name}"</h2>'

                for article in category_articles:
                    text += f'-{article.title}\n'
                    text += f'<p><b>{article.title}</b><br>{article.text[:50]}...</p>'

                msg = EmailMultiAlternatives(
                    subject=subject,
                    body=text,
                    to=[user.email]
                )
                msg.attach_alternative(html, 'text/html')
                msg.send()