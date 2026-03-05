from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed
from django.core.mail import EmailMultiAlternatives
from .models import Post
from .tasks import send_notification_email

@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        subject = f'Новая статья: {instance.title}'
        message = instance.text[:50]

        send_notification_email.delay(
            subject,
            message,
            ['test@mail.com']
        )
@receiver(post_save, sender=User)
@receiver(m2m_changed, sender=Post.categories.through)
def add_user_to_common(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='common')
        instance.groups.add(group)

def notify_subscribers(sender, instance, action, **kwargs):
    if action != 'post_add':
        return
    
    for category in instance.categories.all():
        for user in category.subscribers.all():
            subject = instance.title

            text_content = (
                f"Здравствуй, {user.username}. "
                f"Новая статья в твоем любимом разделе! "
            )

            html_context = (
                f"<h2>{instance.title}</h2>"
                f"<p>{instance.text[:50]}...</p>"
            )

            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                to=[user.email],
            )
            msg.attach_alternative(html_context, "text/html")
            msg.send()


    