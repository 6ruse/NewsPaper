from django.urls import path
# Импортируем созданное нами представление
from .views import CategoryList, CategoryDetail, PostList, PostDetail


urlpatterns = [
   # path('/category/', CategoryList.as_view()),
   # path('/category/<int:pk>', CategoryDetail.as_view()),
   path('', PostList.as_view()),
   path('<int:pk>', PostDetail.as_view()),
]