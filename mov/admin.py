from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_staff')

admin.site.register(Type)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('area',)

@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'date_uploaded')

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('series', 'season_number')

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ("season", "episode_number")

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'date_uploaded')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('writer', 'series', 'episode', 'movie', 'date')
