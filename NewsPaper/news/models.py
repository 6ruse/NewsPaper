from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse

class Author(models.Model):
    autor = models.OneToOneField(User, on_delete=models.CASCADE)
    raiting = models.FloatField(default=0)

    def update_rating(self):
        postRaiting = self.post_set.aggregate(postRaiting=Sum('post_raiting'))
        pRaiting = 0
        pRaiting += postRaiting.get('postRaiting')

        commentRaiting = self.autor.comment_set.aggregate(commentRaiting=Sum('comment_raiting'))
        cRaiting = 0
        cRaiting += commentRaiting.get('commentRaiting')
        self.raiting = (pRaiting * 3) + cRaiting
        self.save()

class Category(models.Model):
  nm_category = models.CharField(max_length=150, unique=True)
  def __str__(self):
    return self.nm_category.title()

class Post(models.Model):
    autor = models.ForeignKey(Author, on_delete=models.CASCADE)

    in_article = 'A'
    in_news = 'N'

    post_type = [
        (in_article, 'Статья'),
        (in_news, 'Новость')
    ]

    post_type = models.CharField(max_length=2, choices=post_type, default=in_article)
    date_time_create = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='CategoryPost')
    post_title = models.CharField(max_length=255)
    post_text = models.TextField()
    post_raiting = models.FloatField(default=0)

    def __str__(self):
        return self.post_title.title()

    def like(self):
        self.post_raiting += 1
        self.save()

    def dislike(self):
        if self.post_raiting > 0:
            self.post_raiting -= 1
        self.save()

    def preview(self):
        return self.post_text[0:123] + '...'

    def get_absolute_url(self):
        return reverse('newsOne', args=[str(self.id)])

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    # def get_context_data(self, **kwargs):
    #     # С помощью super() мы обращаемся к родительским классам
    #     # и вызываем у них метод get_context_data с теми же аргументами,
    #     # что и были переданы нам.
    #     # В ответе мы должны получить словарь.
    #     context = super().get_context_data(**kwargs)
    #     # К словарю добавим текущую дату в ключ 'time_now'.
    #     context['time_now'] = datetime.utcnow()
    #     # Добавим ещё одну пустую переменную,
    #     # чтобы на её примере рассмотреть работу ещё одного фильтра.
    #     context['next_sale'] = None
    #     return context

class CategoryPost(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    date_time_create = models.DateTimeField(auto_now_add=True)
    comment_raiting = models.FloatField(default=0)

    def like(self):
        self.comment_raiting += 1
        self.save()

    def dislike(self):
        if self.comment_raiting > 0:
            self.comment_raiting -= 1
        self.save()
