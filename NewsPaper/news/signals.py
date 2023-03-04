from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import CategoryPost


@receiver(m2m_changed, sender=CategoryPost)
def post_created(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()

        emails = []

        for cat in categories.all():
            subscribers = cat.subscribers.all()
            emails += [s.emails for s in subscribers]

        subject = f'Новая новость в категории'

        text_content = (
            f'Название: {instance.post_title}\n'
            f'Ссылка на новость: http://127.0.0.1{instance.get_absolute_url()}'
        )
        html_content = (
            f'Название: {instance.post_title}\n'
            f'Ссылка на новость: http://127.0.0.1{instance.get_absolute_url()}'
        )
        print('emails start')
        print(emails)
        print('emails end')
        for email in emails:
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()