from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import FileExtensionValidator
from django.utils import timezone

import django.utils.timezone
import uuid

# Create your models here.

class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=99)
    first_name = models.CharField(max_length=99, blank=True, null=True)
    last_name = models.CharField(max_length=99, blank=True, null=True)
    email = models.EmailField(max_length=299, unique=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    
class Type(models.Model):
    area = models.CharField(max_length=19)

    def __str__(self):
        return self.area

class Category(models.Model):
    typ = models.ForeignKey(Type, on_delete=models.CASCADE)
    area = models.CharField(max_length=99)

    def __str__(self):
        return self.area

class Series(models.Model):
    owner = models.ForeignKey(User, models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=49)
    description = models.TextField()
    genre = models.CharField(max_length=99)
    stars = models.CharField(max_length=999, blank=True, null=True)
    language = models.CharField(max_length=49)
    cover_picture = models.ImageField(upload_to='images/')
    trailer = models.FileField(upload_to='videos/trailers/',
                               validators=[FileExtensionValidator(allowed_extensions=['mov','avi','mp4','webm','mkv','vbmv'])])
    release_year = models.CharField(max_length=4, default=2023)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-date_uploaded']

    def __str__(self):
        return self.title

class Season(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    season_number = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-series']

    def __str__(self):
        return f'{self.series.title} - S{self.season_number}'

class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    episode_number = models.IntegerField()
    title = models.CharField(max_length=49, blank=True, null=True)
    description = models.TextField()
    duration = models.CharField(max_length=8, default='00:00:00')
    movie = models.FileField(upload_to='videos/movies/',
                               validators=[FileExtensionValidator(allowed_extensions=['mov','avi','mp4','webm','mkv','vbmv'])]) 
    release_date = models.DateField(default=django.utils.timezone.now,)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-date_uploaded']

    def __str__(self):
        return f'{self.season.series} - S{self.season.season_number}E{self.episode_number}'

class Movie(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=49)
    description = models.TextField()
    genre = models.CharField(max_length=99)
    duration = models.CharField(max_length=8, default='00:00:00')
    stars = models.CharField(max_length=999, blank=True, null=True)
    language = models.CharField(max_length=49)
    cover_picture = models.ImageField(upload_to='images/')
    trailer = models.FileField(upload_to='videos/trailers/',
                               validators=[FileExtensionValidator(allowed_extensions=['mov','avi','mp4','webm','mkv','vbmv'])])
    movie = models.FileField(upload_to='videos/movies/',
                               validators=[FileExtensionValidator(allowed_extensions=['mov','avi','mp4','webm','mkv','vbmv'])]) 
    release_date = models.DateField(default=django.utils.timezone.now,)
    release_year = models.CharField(max_length=4, default=2023)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-date_uploaded']

    def __str__(self):
        return self.title

class Review(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    series = models.ForeignKey(Series, on_delete=models.CASCADE, blank=True, null=True)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, blank=True, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='replies')

    class Meta:
        ordering=['-date']

    def __str__(self):
        return str(self.writer) + ' Review'

    @property
    def children(self):
        return Review.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
    