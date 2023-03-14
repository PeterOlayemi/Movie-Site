from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView, name='home'),
    path('<category>/', views.CategoryView, name='category'),
    
    path('account/login/', views.LoginView, name='login'),
    path('account/register/', views.RegisterView, name='register'),
    
    path('search/movie/', views.SearchMovieView, name='moviesearch'),
    path('movie/<title>/<int:pk>/', views.MovDetailView, name='movdetail'),
    path('search/series/', views.SearchSeriesView, name='seriesearch'),
    path('series/<title>/<int:pk>/', views.SeriesDetailView, name='seriesdetail'),
    path('<title>/season<season_number>/<int:pk>/', views.SeasonView, name='season'),
    path('<title>/season<season_number>/episode<episode_number>/<int:pk>/', views.EpisodeView, name='episode'),
    
    path('review/reply/<int:pk>/', views.ReplyReviewView, name='reply'),
    path('review/delete/<int:pk>/', views.ReviewDelView, name='delreview'),
    

]
