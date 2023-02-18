from django import forms
from .models import Category, Post
from django.core.exceptions import ValidationError

class CategoryForm(forms.ModelForm):
   class Meta:
       model = Category
       fields = [
           'nm_category',
       ]

class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = [
           'autor',
           'category',
           'post_title',
           'post_text',
       ]

   def clean(self):
    cleaned_data = super().clean()
    post_text = cleaned_data.get("post_text")
    if post_text is not None and len(post_text) < 20:
        raise ValidationError({
            "post_text": "Описание не может быть менее 20 символов."
        })

    name = cleaned_data.get("post_title")
    if name == post_text:
        raise ValidationError(
            "Описание не должно быть идентично названию."
        )

    return cleaned_data

class NewsForm(PostForm):
    def form_valid(self, form):
        news = form.save(commit=False)
        news.category = 'N'
        return super().form_valid(form)

class ArticlesForm(PostForm):
    def form_valid(self, form):
        news = form.save(commit=False)
        news.category = 'A'
        return super().form_valid(form)