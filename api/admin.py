from django.contrib import admin
from .models import Category, Article, Comment, Reply, UserFavoriteCategory

admin.site.register(Category)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(UserFavoriteCategory)
