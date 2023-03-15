from django.urls import path
from django.views.decorators.cache import cache_page
# Импортируем созданное нами представление
from .views import (PostList, PostDetail, NewsCreate, NewsUpdate, NewsDelete, PostSearch, ArticlesDelete,
                    ArticlesUpdate, ArticlesCreate, subscriptions, CategoryList, subscribe, ArticlesDetail)


urlpatterns = [
   # path('category/', CategoryList.as_view()),
   # path('category/<int:pk>', CategoryDetail.as_view()),
   path('categories/<int:pk>', cache_page(300)(CategoryList.as_view()), name='categories_news'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
   path('', cache_page(60)(PostList.as_view()), name='news'),
   path('<int:pk>', cache_page(300)(PostDetail.as_view()), name='newsOne'),
   path('create/', NewsCreate.as_view(), name='postEdit'),
   path('<int:pk>/update/', NewsUpdate.as_view(), name='postEdit'),
   path('<int:pk>/delete/', NewsDelete.as_view(), name='newsDelete'),
   path('search/', PostSearch.as_view(), name='news'),

   path('articles/create/', ArticlesCreate.as_view(), name='articlesEdit'),
   path('articles/update/', ArticlesUpdate.as_view(), name='articlesEdit'),
   path('articles/delete/', ArticlesDelete.as_view(), name='articlesDelete'),
   path('subscriptions/', subscriptions, name='subscriptions'),

   path('articles/<int:pk>', ArticlesDetail.as_view(), name='newsOne'),
]