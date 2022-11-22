from django.db import models
from django.template.defaultfilters import slugify
import uuid
from django_quill.fields import QuillField
from django.urls import reverse
from  embed_video.fields  import  EmbedVideoField
from django.contrib.auth import get_user_model

CustomUser=get_user_model()

# Create your models here.
# la class de base
class BaseModel(models.Model):
    uid=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    created=models.DateField(auto_now_add=True,blank=True,null=True,verbose_name='Create date')
    updated=models.DateTimeField(auto_now=True,verbose_name='Update date')

    class Meta:
        abstract=True

# blog
class Categorie(BaseModel):
    nom_categorie = models.CharField(max_length=100, verbose_name='Non categorie')
    slug = models.SlugField(max_length=200, verbose_name='Slug')

    class Meta:
        verbose_name = "Categorie"

    def __str__(self) -> str:
        return self.nom_categorie

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom_categorie)

        super().save(*args, **kwargs)

class Article(BaseModel):
    CHOIX_CATEGORIE=(
        ('Developpement','Developpement'),
        ('Linux', 'Linux'),
        ('Windows Server', 'Windows Server'),
    )

    titre = models.CharField(max_length=1000, verbose_name='Titre')
    slug = models.SlugField(max_length=200, verbose_name='Slug')
    body = models.TextField(blank=True, null=True, verbose_name="Resume")
    description=QuillField(blank=True,null=True,verbose_name='Description')
    image = models.ImageField(upload_to='articles_images', blank=True, null=True, name="image", verbose_name='Image')
    bg = models.ImageField(upload_to='articles_images', blank=True, null=True)
    auteur = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Auteur')
    categorie1=models.CharField(choices=CHOIX_CATEGORIE,default="Developpement",max_length=200,blank=True,null=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='fk_categorie',
                                  verbose_name='Categorie')
    statut = models.BooleanField(default=False, verbose_name="Statut")

    class Meta:
        ordering = ['-created']
        verbose_name = "Article"

    def __str__(self) -> str:
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)

        super().save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse("mes_articles")

    def get_absolute_url(self):
        return reverse('detail_article', kwargs={'pk': self.pk})

class Commentaire(BaseModel):
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='fk_blog_comment')
    name = models.CharField(max_length=80,null=True, blank=True,)
    email = models.EmailField()
    body = models.TextField()
    cauthor = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        ordering = ['-created']
        verbose_name = "Commentaire"

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
