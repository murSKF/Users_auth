from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_notification_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        'from@example.com',
        recipient_list
    )


@shared_task
def weekly_digest():
    from .models import Post
    from django.utils import timezone
    from datetime import timedelta

    week_ago = timezone.now() - timedelta(days=7)

    posts = Post.objects.filter(created_at__gte=week_ago)