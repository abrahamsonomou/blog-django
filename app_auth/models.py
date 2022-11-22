from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django_countries.fields import CountryField


# Create your models here.
class UserProfileManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Desolé, veuillez saisir un email')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username)

        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email, username, password)

        user.is_staff = True
        user.is_active = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    CHOIX_GRADE = {
        ('licence', 'Licence'),
        ('master', 'Master'),
        ('doctorat', 'Doctorat'),
        ('bts', 'BTS'),
        ('autre', 'Autre'),
    }
    username = models.CharField(max_length=50, default='Anonymous', unique=True)
    email = models.EmailField(max_length=254, unique=True, blank=True, null=True)
    photo = models.ImageField(upload_to='users_avatar', blank=True, null=True)
    resume = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    contry = CountryField(blank=True, null=True, max_length=200, name="contry", verbose_name="Contry")
    grade = models.TextField(blank=True, null=True, name="grade", verbose_name="Grade", choices=CHOIX_GRADE)
    specialite = models.CharField(blank=True, null=True, name="specialite", verbose_name="specialite", max_length=200, )
    twitter = models.CharField(blank=True, null=True, name='twitter', verbose_name="Twitter", max_length=200)
    facebook = models.CharField(blank=True, null=True, name='facebook', verbose_name="Facebook", max_length=200)
    instagram = models.CharField(blank=True, null=True, name='instagram', verbose_name="Instagram", max_length=200)
    linkdin = models.CharField(blank=True, null=True, name='linkdin', verbose_name="Linkdin", max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True, blank=True, null=True)
    is_staff = models.BooleanField(default=False, blank=True, null=True)

    # USERNAME_FIELD='email'
    # REQUIRED_FIELDS=['username']

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS=['username']

    objects = UserProfileManager()

    class Meta:
        verbose_name = "Profil"

    def __str__(self) -> str:
        return self.username