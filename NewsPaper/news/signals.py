# from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import CategoryPost
from .tasks import send_subscribers


@receiver(m2m_changed, sender=CategoryPost)
def post_created(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()

        emails = []

        for cat in categories.all():
            subscribers = cat.subscribers.all()
            emails += [s.email for s in subscribers.user]

        send_subscribers.delay(instance.get_absolute_url(), instance.post_title, emails)

    # if kwargs['action'] == 'post_add':
    #     categories = instance.category.all()
    #
    #     emails = []
    #
    #     for cat in categories.all():
    #         subscribers = cat.subscribers.all()
    #         emails += [s.email for s in subscribers.user]
    #
    #     subject = f'Новая новость в категории'
    #
    #     text_content = (
    #         f'Название: {instance.post_title}\n'
    #         f'Ссылка на новость: http://127.0.0.1{instance.get_absolute_url()}'
    #     )
    #     html_content = (
    #         f'Название: {instance.post_title}\n'
    #         f'Ссылка на новость: http://127.0.0.1{instance.get_absolute_url()}'
    #     )
    #     for email in emails:
    #         msg = EmailMultiAlternatives(subject, text_content, None, [email])
    #         msg.attach_alternative(html_content, "text/html")
    #         msg.send()