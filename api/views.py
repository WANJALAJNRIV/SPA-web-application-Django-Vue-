from django.http import HttpResponse, HttpRequest, JsonResponse

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
import json
from django.http import Http404
from rest_framework import status, permissions

from .models import Category, Article, Comment, Reply, UserFavoriteCategory
from .serializers import (
    CategorySerializer,
    ArticleSerializer,
    CommentSerializer,
    ReplySerializer,
    UserSerializer,
    UserFavoriteCategorySerializer,
    CategorySerializer
)


@login_required
def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    user = request.user
    serializer = UserSerializer(user)
    response_data = serializer.data
    return Response(response_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Profile updated successfully'})
    else:
        print(serializer.errors)
        return Response(serializer.errors, status=400)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_favorite_categories_with_articles(request):
    try:
        user_id = request.user.id

        # Get user's favorite categories
        favorite_categories = UserFavoriteCategory.objects.filter(user=user_id)
        favorite_categories_serializer = UserFavoriteCategorySerializer(favorite_categories, many=True)

        # Group articles by category
        grouped_articles = group_articles_by_category(user_id)

        return JsonResponse({
            'userFavoriteCategories': favorite_categories_serializer.data,
            'groupedArticles': grouped_articles,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def group_articles_by_category(user_id):
    # Get user's favorite categories
    favorite_categories = UserFavoriteCategory.objects.filter(user=user_id)

    grouped_articles = []
    for category in favorite_categories:
        # Get articles for each favorite category
        articles = Article.objects.filter(category=category.category)
        articles_serializer = ArticleSerializer(articles, many=True)

        grouped_articles.append({
            'categoryId': category.category.id,
            'categoryName': category.category.name,
            'articles': articles_serializer.data,
        })

    return grouped_articles


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        print(categories)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_favorites=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def article_list(request):
    articles = Article.objects.all()  #filter(category__user_favorites=request.user)
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    serializer = ArticleSerializer(article)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def comment_list(request, pk):
    comments = Comment.objects.filter(article_id=pk)
    serializer = CommentSerializer(comments, many=True)
    comments_with_replies = []
    for comment_data in serializer.data:
        comment_id = comment_data['id']
        replies = Comment.objects.filter(id=comment_id)
        reply_serializer = CommentSerializer(replies, many=True)
        comment_data['replies'] = reply_serializer.data
        comments_with_replies.append(comment_data)
    return Response(comments_with_replies)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_operations(request, pk):

    if request.method == 'PUT':
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_reply(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.method == 'POST':
        serializer = ReplySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, comment=comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            print('You sure ')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def reply_operations(request, pk):
    reply = get_object_or_404(Reply, pk=pk)

    if request.method == 'POST':
        print(request.data)
        serializer = ReplySerializer(data=request.data)
        if serializer.is_valid():
            comment_id = request.data['comment']
            comment = get_object_or_404(Comment,id=comment_id)
            print(comment)

            serializer.save(user=request.user, comment=comment)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        serializer = ReplySerializer(reply, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        reply.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    # Customize if needed
    pass



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_favorite_category_list(request):
    if request.method == 'GET':
        favorite_categories = UserFavoriteCategory.objects.filter(user=request.user)
        serializer = UserFavoriteCategorySerializer(favorite_categories, many=True)
        print(serializer.data)
        return Response(serializer.data)

    elif request.method == 'POST':
        category_id = request.data.get('category_id')
        if category_id is not None:
            category = get_object_or_404(Category, id=category_id)
            user_favorite_category = UserFavoriteCategory.objects.create(user=request.user, category=category)
            serializer = UserFavoriteCategorySerializer(user_favorite_category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        print("Category ID is required.")
        return Response({"error": "Category ID is required."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def user_favorite_category_detail(request, category_id):
    try:
        favorite_category = UserFavoriteCategory.objects.get(user=request.user, category__id=category_id)
    except UserFavoriteCategory.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        serializer = UserFavoriteCategorySerializer(favorite_category)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserFavoriteCategorySerializer(favorite_category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        favorite_category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


