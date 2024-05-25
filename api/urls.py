"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import  path, re_path
from .views import category_list, category_detail, article_list, article_detail, comment_operations, reply_operations, user_info,create_reply
from .views import ( main_spa, CustomTokenObtainPairView, comment_list, update_profile, create_comment, 
        user_favorite_category_list, user_favorite_category_detail, category_list, user_favorite_categories_with_articles)

urlpatterns = [
        
    path('categories/', category_list, name='category-list'),
    path('categories/<int:pk>/', category_detail, name='category-detail'),

    path('api/articles/', article_list, name='article-list'),

    path('api/articles/<int:pk>/', article_detail, name='article-detail'),



    path('api/comment_list/<int:pk>/', comment_list, name='comment_list'),
    path('api/comments/create/<int:article_pk>/', create_comment, name='create_comment'),
    path('api/comments/<int:pk>/', comment_operations, name='comment_operations'),


    path('api/reply/create/<int:comment_pk>/', create_reply, name='create_reply'),

    path('api/replies/<int:pk>/', reply_operations, name='reply_operations'),

    path('user-info/', user_info, name='user_info'),
    
    path('update-profile/',update_profile, name='update_profile' ),

   

    path('user_favorite_categories/', user_favorite_category_list, name='user-favorite-categories-list'),



    path('user_favorite_categories/<int:category_id>/', user_favorite_category_detail, name='user-favorite-category-detail'),

    path('categories/', category_list, name='category-list'),

    path('user_favorite_categories_with_articles/',user_favorite_categories_with_articles, name='user_favorite_categories_with_articles'), 
    path('', main_spa),

]



