from django.urls import path
# Импортируем созданное нами представление
from .views import (PostList, PostDetail, NewsCreate, NewsUpdate, NewsDelete, PostSearch,
                    ArticlesDelete, ArticlesUpdate, ArticlesCreate)


urlpatterns = [
   # path('/category/', CategoryList.as_view()),
   # path('/category/<int:pk>', CategoryDetail.as_view()),
   path('', PostList.as_view(), name='news'),
   path('<int:pk>', PostDetail.as_view(), name='newsOne'),
   path('create/', NewsCreate.as_view(), name='postEdit'),
   path('<int:pk>/update/', NewsUpdate.as_view(), name='postEdit'),
   path('<int:pk>/delete/', NewsDelete.as_view(), name='newsDelete'),
   path('search/', PostSearch.as_view(), name='news'),

   path('articles/create/', ArticlesCreate.as_view(), name='articlesEdit'),
   path('articles/update/', ArticlesUpdate.as_view(), name='articlesEdit'),
   path('articles/delete/', ArticlesDelete.as_view(), name='articlesDelete'),
]