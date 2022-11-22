from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('articles', blog, name='articles'),
    path('blog/(?P<pk>[0-9]+)/$', detail_article, name='detail_article'),
    # path('blog/<auteur>/',auteur_article,name='auteur_article'),
    path('article/recherche', search_article, name='search_article'),
    path('recherche/', search, name='search'),
    path('comment/', postComment, name='comment'),
    path('categorie/(?P<pk>[0-9]+)/$', select_article_categorie, name='select_article_categorie'),
    path('contact/',contact , name='contact'),

    # la class ArticleCategorie
    path(r'api/ArticleCategories/', ArticleCategorieList.as_view(), name='ArticleCategories/'),
    path(r'api/(?P<pk>[0-9]+)/$', ArticleCategorieListDetail.as_view(), name='ArticleCategoriedetails/'),

    # la class Article
    path(r'api/Articles/', ArticleList.as_view(), name='Article/'),
    path(r'api/(?P<pk>[0-9]+)/$', ArticleListDetail.as_view(), name='Articledetails/'),

    # la class Commentaire
    path(r'api/Commentaires/', CommentaireList.as_view(), name='Commentaires/'),
    path(r'api/(?P<pk>[0-9]+)/$', CommentaireListDetail.as_view(), name='Commentairedetails/'),

]
