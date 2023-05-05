from django.contrib import admin
from .models import Category, Post
from modeltranslation.admin import TranslationAdmin # импортируем модель амдинки (вспоминаем модуль про переопределение стандартных админ-инструментов)

class CategoryAdmin(TranslationAdmin):
    model = Category

class PostAdmin(TranslationAdmin):
    model = Post


def delete_post_category(modeladmin, request, queryset): # все аргументы уже должны быть вам знакомы, самые нужные из них это
    # request — объект хранящий информацию о запросе и queryset — грубо говоря набор объектов, которых мы выделили галочками.
    for cat in queryset:
        cat = Category.objects.get(nm_category=cat)
        Post.objects.filter(category=cat).delete()
    delete_post_category.short_description = 'Удалить товары выбранной категории'

# создаём новый класс для представления товаров в админке
class CategoryAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('nm_category',) # генерируем список имён всех полей для более красивого отображения
    list_filter = ('nm_category',)
    search_fields = ('nm_category', 'category__nm_category')
    actions = [delete_post_category]  # добавляем действия в список

# class PostAdmin(admin.ModelAdmin):
#     list_display = ('autor', 'post_type', 'date_time_create', 'post_title', 'post_raiting', 'preview') # генерируем список имён всех полей для более красивого отображения

admin.site.register(Category, CategoryAdmin)
# admin.site.register(Category)
admin.site.register(Post, PostAdmin)
