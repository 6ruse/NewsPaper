from django.contrib import admin
from django.urls import path, include
# from django.conf.urls.i18n import i18n_patterns
# from django.views.decorators.cache import cache_page
from rest_framework import routers
from news import views

router = routers.DefaultRouter()
router.register(r'news', views.NewsViewset, 'news')
router.register(r'articles', views.ArticlesViewset, 'articles')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('i18n/', include('django.conf.urls.i18n')), # подключаем встроенные эндопинты для работы с локализацией
    path('admin/', admin.site.urls),
    # path('category/', include('news.urls')),
    path('news/', include('news.urls')),
    # path('', include('news.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),  # Добавили эту строчку
    # path('', include('basic.urls')),
]
