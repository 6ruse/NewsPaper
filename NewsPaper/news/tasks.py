from celery import shared_task
import time
from django.core.mail import EmailMultiAlternatives
from .models import Category, Post

@shared_task
def send_subscribers(url_news, post_title, emails):
    subject = f'Новая новость в категории'

    text_content = (
        f'Название: {post_title}\n'
        f'Ссылка на новость: http://127.0.0.1{url_news}'
    )
    html_content = (
        f'Название: {post_title}\n'
        f'Ссылка на новость: http://127.0.0.1{url_news}'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    print('send_subscribers is work')

@shared_task
def weekly_posts():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(created_at__gte=last_week)
    categories = set(posts.values_list('category__nm_category', flat=True))
    subscribers = set(Category.objects.filter(name__id=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': '',
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()