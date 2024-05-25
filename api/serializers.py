# serializers.py
from rest_framework import serializers
from .models import Category, Article, Comment, Reply, UserFavoriteCategory
from users.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'category', 'author', 'created_at']



class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['id', 'comment', 'user', 'text', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    replies = ReplySerializer(many=True, read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'article', 'user', 'text', 'created_at', 'replies']


class UserFavoriteCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = UserFavoriteCategory
        fields = ['id', 'category', 'added_at']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_of_birth', 'profile_image', 'favorite_categories']
