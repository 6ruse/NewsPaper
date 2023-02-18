from django_filters import FilterSet, ModelChoiceFilter, DateTimeFilter
from .models import Post, Category
from django.forms import DateTimeInput

# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    category = ModelChoiceFilter(
        field_name='categorypost__category',
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Все'

    )
    added_after = DateTimeFilter(
        field_name='date_time_create',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
       model = Post
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
       fields = {
           'post_title': ['icontains'],
       }