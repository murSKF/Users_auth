from django.urls import path
from .views import (
    NewsListView,
    NewsDetailView,
    NewsSearchView,
    NewsCreateView,
    NewsUpdateView,
    NewsDeleteView,
    become_author,
    ArticleListView,
    ArticleCreateView,
    ArticleDeleteView,
    ArticleUpdateView,
    ArticleDetailView,
    SubscribeCategoryView,
    CategoryPostListView,
)


urlpatterns = [
    path('', NewsListView.as_view(), name='news_list'),
    path('search/', NewsSearchView.as_view(), name='news_search'),
    path('<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('create/', NewsCreateView.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsUpdateView.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),

    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('articles/create/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('become_author/', become_author, name='become_author'),

    path('category/<int:pk>/subscribe/', SubscribeCategoryView.as_view(), name='subscribe_category'),
    path('category/<int:pk>/', CategoryPostListView.as_view(), name='category_posts'),
]