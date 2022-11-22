from dataclasses import fields
from rest_framework.serializers import ModelSerializer
from .models import *


# serialisation de la classe ArticleCategorie
class CategorieSerializer(ModelSerializer):
    class Meta:
        model = Categorie
        fields = ['nom_categorie', ]

    # serialisation de la classe Article


class ArticleSerializer(ModelSerializer):
    # image = serializers.ImageField(
    #     max_length=None, allow_empty_file=False, allow_null=True, required=False)

    class Meta:
        model = Article
        # fields=['titre','resume','description','auteur','categorie','image','statut']
        fields = ['titre', 'resume', 'auteur', 'categorie', 'image', 'statut']


# serialisation de la classe Commentaire
class CommentaireSerializer(ModelSerializer):
    class Meta:
        model = Commentaire
        fields = ['article', 'auteur', 'content']
