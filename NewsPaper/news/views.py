from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Category, Post
from .filters import PostFilter
from .forms import (CategoryForm, NewsForm, ArticlesForm)
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
class CategoryList(ListView):
    model = Post
    template_name = 'category.html'
    context_object_name = 'category_news_list'
    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category)
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscruber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Подписка оформлена'

    return render(request, 'subscribe.html', {'category': category, 'message': message})
class CategoryDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Category
    # Используем другой шаблон — product.html
    template_name = 'categoryOne.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'categoryOne'

class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'post_title'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    context_object_name = 'news'  # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    ordering = ['-date_time_create']  #Новости должны выводиться в порядке от более свежей к старой.

    paginate_by = 2  # вот так мы можем указать количество записей на странице

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

class PostSearch(PostList):
    template_name = 'newsSearch.html'

class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'newsOne.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'newsOne'

def create_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/category/')

    return render(request, 'categoryEdit.html', {'form': form})

# def create_news(request):
#     form = NewsForm()
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/news/')
#
#     return render(request, 'postEdit.html', {'form': form})

class NewsCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    raise_exception = True
    form_class = NewsForm
    model = Post
    template_name = 'postEdit.html'

class NewsUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = NewsForm
    model = Post
    template_name = 'postEdit.html'

class NewsDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'postDelete.html'
    success_url = reverse_lazy('news')

class ArticlesCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = ArticlesForm
    model = Post
    template_name = 'articlesEdit.html'

class ArticlesUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = ArticlesForm
    model = Post
    template_name = 'articlesEdit.html'

class ArticlesDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'articlesDelete.html'
    success_url = reverse_lazy('news')

@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            category.subscribers.add(request.user)
        elif action == 'unsubscribe':
            if category.subscribers.filter(id=request.user.id).exists():
                category.subscribers.remove(request.user)

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Category.objects.filter(
                id=OuterRef('pk'),
                subscribers=request.user,
            )
        )
    ).order_by('nm_category')

    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )