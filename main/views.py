from django.http import HttpResponseRedirect
from django.shortcuts import redirect,render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from .serializers import *
from .models import *
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAdminUser
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger
)

# Create your views here.
def index(request):

    recent_windows1=Article.objects.filter(categorie1='Windows Server').filter(statut=True).order_by('-updated')[:2]
    recent_windows2=Article.objects.filter(categorie1='Windows Server').filter(statut=True).order_by('-updated')[2:5]
    recent_windows3=Article.objects.filter(categorie1='Windows Server').filter(statut=True).order_by('-updated')[6:10]

    recent_linux1=Article.objects.filter(categorie1='Linux').filter(statut=True).order_by('-updated')[:3]
    recent_linux2=Article.objects.filter(categorie1='Linux').filter(statut=True).order_by('-updated')[3:5]

    recent_dev1=Article.objects.filter(categorie1='Developpement').filter(statut=True).order_by('-updated')[:9]

    recent_articles=Article.objects.filter(statut=True).order_by('-updated')[:3]
    categories=Categorie.objects.all()

    context = {
        'categories': categories,
        'recent_dev1':recent_dev1,
        'recent_linux1':recent_linux1,
        'recent_linux2':recent_linux2,
        'recent_windows1':recent_windows1,
        'recent_windows2':recent_windows2,
        'recent_windows3':recent_windows3,
        'recent_articles': recent_articles,
        }

    return render(request, "blog/index.html", context)

def blog(request):
    recent_article = Article.objects.filter(statut=True).order_by('-updated')[:3]
    list_articles = Article.objects.all().filter(statut=True)

    nb_article_dev=Article.objects.filter(categorie1='Developpement').filter(statut=True).count()
    nb_article_linux=Article.objects.filter(categorie1='Linux').filter(statut=True).count()
    nb_article_windows=Article.objects.filter(categorie1='Windows Server').filter(statut=True).count()

    paginator = Paginator(list_articles, 5)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    categories = Categorie.objects.all()

    context = {
        'categories': categories,
        'articles': articles,
        'page': page,
        'recent_article': recent_article,
        'nb_windows':nb_article_windows,
        'nb_linux':nb_article_linux,
        'nb_dev':nb_article_dev,
    }
    return render(request, "blog/articles.html", context)


def detail_article(request, pk: int):
    try:
        article = Article.objects.get(pk=pk)
        categorie = article.categorie
        article_en_relation = Article.objects.filter(categorie=categorie)[:3]

        nb_article_dev = Article.objects.filter(categorie1='Developpement').filter(statut=True).count()
        nb_article_linux = Article.objects.filter(categorie1='Linux').filter(statut=True).count()
        nb_article_windows = Article.objects.filter(categorie1='Windows Server').filter(statut=True).count()

        comments=Commentaire.objects.filter(article=article)

        categories = Categorie.objects.all()

        context = {
            'categories': categories,
            'article_en_relation': article_en_relation,
            'article': article,
            'nb_windows':nb_article_windows,
            'nb_linux':nb_article_linux,
            'nb_dev':nb_article_dev,
            'comments':comments,
        }
    except Article.DoesNotExist:
        raise ('This article doesnot exist')
    return render(request, 'blog/detail_article.html', context)

@csrf_exempt
def postComment(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'POST':
        article_id = request.POST.get('pk')
        body = request.POST.get('comment')
        article = Article.objects.get(pk=article_id)
        email = request.POST.get('email')
        name = request.POST.get('name')
        cauthor = request.user

        # print(article_id,body,email,name,cauthor)
        if article_id:
            Commentaire.objects.create(
                article=article,name=name,email=email,body=body,cauthor=cauthor
            )
        return redirect(request.build_absolute_uri(article.get_absolute_url()))

def search_article(request):
    query = request.POST.get('article')
    recent_article = Article.objects.filter(statut=True).order_by('-updated')[:5]
    list_articles = Article.objects.filter(Q(titre__icontains=query) | Q(body__icontains=query))

    nb_article_dev = Article.objects.filter(categorie1='Developpement').filter(statut=True).count()
    nb_article_linux = Article.objects.filter(categorie1='Linux').filter(statut=True).count()
    nb_article_windows = Article.objects.filter(categorie1='Windows Server').filter(statut=True).count()

    paginator = Paginator(list_articles, 12)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    categories=Categorie.objects.all()

    context = {
        'categories': categories,
        'articles': articles,
        'page': page,
        'recent_article': recent_article,
        'nb_windows': nb_article_windows,
        'nb_linux': nb_article_linux,
        'nb_dev': nb_article_dev,
        'q':query,
    }

    return render(request, 'blog/search_article.html', context)

def search(request):
    query = request.POST.get('q')
    recent_article = Article.objects.filter(statut=True).order_by('-updated')[:5]
    list_articles = Article.objects.filter(Q(titre__icontains=query) | Q(body__icontains=query))

    nb_article_dev = Article.objects.filter(categorie1='Developpement').filter(statut=True).count()
    nb_article_linux = Article.objects.filter(categorie1='Linux').filter(statut=True).count()
    nb_article_windows = Article.objects.filter(categorie1='Windows Server').filter(statut=True).count()

    paginator = Paginator(list_articles, 12)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    categories=Categorie.objects.all()

    context = {
        'categories': categories,
        'articles': articles,
        'page': page,
        'recent_article': recent_article,
        'nb_windows': nb_article_windows,
        'nb_linux': nb_article_linux,
        'nb_dev': nb_article_dev,
        'q':query,
    }

    return render(request, 'blog/search.html', context)


def select_article_categorie(request, pk: int):
    try:
        categorie = Categorie.objects.get(pk=pk)
        recent_article = Article.objects.filter(statut=True).order_by('-updated')[:5]
        list_articles = Article.objects.all().filter(statut=True).filter(categorie=categorie)

        nb_article_dev = Article.objects.filter(categorie1='Developpement').filter(statut=True).count()
        nb_article_linux = Article.objects.filter(categorie1='Linux').filter(statut=True).count()
        nb_article_windows = Article.objects.filter(categorie1='Windows Server').filter(statut=True).count()

        paginator = Paginator(list_articles, 5)
        page = request.GET.get('page')
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        categories = Categorie.objects.all()

        context = {
            'categories': categories,
            'categorie': categorie,
            'articles': articles,
            'page': page,
            'recent_article': recent_article,
            'nb_windows': nb_article_windows,
            'nb_linux': nb_article_linux,
            'nb_dev': nb_article_dev,
        }
    except Article.DoesNotExist:
        raise ('This categorie doesnot exist')
    return render(request, "blog/select_article_categorie.html", context)

def contact(request):
    return render(request, 'pages/contact.html')


# la class ArticleCategorie
class ArticleCategorieList(generics.ListCreateAPIView):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [IsAdminUser]

class ArticleCategorieListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [IsAdminUser]

# la class Article
class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAdminUser]


class ArticleListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAdminUser]


# la class Commentaire
class CommentaireList(generics.ListCreateAPIView):
    queryset = Commentaire.objects.all()
    serializer_class = CommentaireSerializer
    permission_classes = [IsAdminUser]

class CommentaireListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Commentaire.objects.all()
    serializer_class = CommentaireSerializer
    permission_classes = [IsAdminUser]

