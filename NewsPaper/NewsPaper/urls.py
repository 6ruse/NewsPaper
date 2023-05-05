from django.contrib import admin
from django.urls import path, include
# from django.conf.urls.i18n import i18n_patterns
# from django.views.decorators.cache import cache_page

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')), # подключаем встроенные эндопинты для работы с локализацией
    path('admin/', admin.site.urls),
    # path('category/', include('news.urls')),
    path('news/', include('news.urls')),
    # path('', include('news.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),  # Добавили эту строчку
    # path('', include('basic.urls')),
]
