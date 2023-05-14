from .models import *
from rest_framework import serializers


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
       model = Post
       fields = ['id', 'category', 'post_title', 'autor', 'post_text', 'post_raiting']
