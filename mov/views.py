from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import *
from .forms import *

# Create your views here.

@login_required
def ReviewDelView(request, pk):
    obj = Review.objects.get(id=pk)
    if request.method == 'POST':
        obj.delete()
        if obj.series:
            return redirect(reverse('seriesdetail', args=[obj.series.title, obj.series.pk]))
        if obj.episode:
            return redirect(reverse('episode', args=[obj.episode.season.series.title, obj.episode.season.season_number, obj.episode.episode_number, obj.episode.pk]))
        if obj.movie:
            return redirect(reverse('movdetail', args=[obj.movie.title, obj.movie.pk]))
    context={'obj':obj, 'type':'review'}
    return render(request, 'del.html', context)

@login_required
def ReplyReviewView(request, pk):
    obj = Review.objects.get(id=pk)
    cat = Category.objects.all()
    form = ReviewForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            if request.user.is_authenticated:
                data = form.save(commit=False)
                data.writer = request.user
                if obj.series:
                    data.series = obj.series
                if obj.episode:
                    data.episode = obj.episode
                if obj.movie:
                    data.movie = obj.movie
                data.parent = obj
                data.save()
                if obj.series:
                    return redirect(reverse('seriesdetail', args=[obj.series.title, obj.series.pk]))
                if obj.episode:
                    return redirect(reverse('episode', args=[obj.episode.season.series.title, obj.episode.season.season_number, obj.episode.episode_number, obj.episode.pk]))
                if obj.movie:
                    return redirect(reverse('movdetail', args=[obj.movie.title, obj.movie.pk]))
            else:
                return redirect('login')
    context = {'obj':obj, 'form':form, 'cat':cat}
    return render(request, 'reply.html', context)

def EpisodeView(request, title, season_number, episode_number, pk):
    obj = Episode.objects.get(id=pk)
    cat = Category.objects.all()
    data = Review.objects.filter(episode=obj).order_by('-date')
    data_c = Review.objects.filter(episode=obj).count()
    form = ReviewForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            if request.user.is_authenticated:
                post = form.save(commit=False)
                post.writer = request.user
                post.episode = obj
                post.save()
                return redirect(reverse('episode', args=[obj.season.series.title, obj.season.season_number, obj.episode_number, obj.pk]))
            else:
                return redirect('login')
    context = {'obj':obj, 'data':data, 'data_c':data_c, 'form':form, 'cat':cat}
    return render(request, 'episode.html', context)

def SeasonView(request, title, season_number, pk):
    obj = Season.objects.get(id=pk)
    data = Episode.objects.filter(season=obj).order_by('-date_uploaded')
    data_c = Episode.objects.filter(season=obj).count()
    cat = Category.objects.all()
    context = {'obj':obj, 'data':data, 'data_c':data_c, 'cat':cat}
    return render(request, 'season.html', context)

def SeriesDetailView(request, title, pk):
    obj = Series.objects.get(id=pk)
    cat = Category.objects.all()
    son = Season.objects.filter(series=obj).order_by('-date')
    son_c = Season.objects.filter(series=obj).count()
    data = Review.objects.filter(series=obj).order_by('-date')
    data_c = Review.objects.filter(series=obj).count()
    form = ReviewForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            if request.user.is_authenticated:
                post = form.save(commit=False)
                post.writer = request.user
                post.series = obj
                post.save()
                return redirect(reverse('seriesdetail', args=[obj.title, obj.pk]))
            else:
                return redirect('login')
    context = {'obj':obj, 'son':son, 'son_c':son_c, 'data':data, 'data_c':data_c, 'form':form, 'cat':cat}
    return render(request, 'seriesdetail.html', context)

def MovDetailView(request, title, pk):
    obj = Movie.objects.get(id=pk)
    cat = Category.objects.all()
    data = Review.objects.filter(movie=obj).order_by('-date')
    data_c = Review.objects.filter(movie=obj).count()
    form = ReviewForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            if request.user.is_authenticated:
                post = form.save(commit=False)
                post.writer = request.user
                post.movie = obj
                post.save()
                return redirect(reverse('movdetail', args=[obj.title, obj.pk]))
            else:
                return redirect('login')
    context = {'obj':obj, 'data':data, 'data_c':data_c, 'form':form, 'cat':cat}
    return render(request, 'movdetail.html', context)

def CategoryView(request, category):
    data = Series.objects.filter(category__typ__area='Series', category__area=category).order_by('-date_uploaded')
    paginator = Paginator(data, 10)
    page = request.GET.get('page')
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    obj = Movie.objects.filter(category__typ__area='Movie', category__area=category).order_by('-date_uploaded')
    paginator = Paginator(obj, 10)
    page = request.GET.get('page')
    try:
        obj = paginator.page(page)
    except PageNotAnInteger:
        obj = paginator.page(1)
    except EmptyPage:
        obj = paginator.page(paginator.num_pages)
    cat = Category.objects.all()
    categ = Category.objects.get(area=category)
    
    cou = Series.objects.filter(category__area=category).all().count()
    nt = Movie.objects.filter(category__area=category).all().count()
    count = cou + nt
    
    context={'obj':obj, 'data':data, 'count':count, 'cat':cat, 'categ':categ}
    return render(request, 'category.html', context)

def SearchSeriesView(request):
    q = request.POST.get('q') if request.POST.get('q') != None else ''
    obj = Series.objects.filter( Q(category__area__icontains=q) | Q(genre__icontains=q) | Q(title__icontains=q) | Q(language__icontains=q) | Q(release_year__icontains=q)).order_by('-date_uploaded')
    obj_c = Series.objects.filter( Q(category__area__icontains=q) | Q(genre__icontains=q) | Q(title__icontains=q) | Q(language__icontains=q) | Q(release_year__icontains=q)).order_by('-date_uploaded').count()
    cat = Category.objects.all()
    context={'obj':obj, 'obj_c':obj_c, 'cat':cat}
    return render(request, 'seriesearch.html', context)

def SearchMovieView(request):
    q = request.POST.get('q') if request.POST.get('q') != None else ''
    obj = Movie.objects.filter( Q(category__area__icontains=q) | Q(genre__icontains=q) | Q(title__icontains=q) | Q(language__icontains=q) | Q(release_year__icontains=q)).order_by('-date_uploaded')
    obj_c = Movie.objects.filter( Q(category__area__icontains=q) | Q(genre__icontains=q) | Q(title__icontains=q) | Q(language__icontains=q) | Q(release_year__icontains=q)).order_by('-date_uploaded').count()
    cat = Category.objects.all()
    context={'obj':obj, 'obj_c':obj_c, 'cat':cat}
    return render(request, 'movsearch.html', context)

def HomeView(request):
    obj = Movie.objects.all().order_by('-date_uploaded')[:3]
    data = Series.objects.all().order_by('-date_uploaded')[:2]
    cat = Category.objects.all()
    context={'obj':obj, 'data':data, 'cat':cat}
    return render(request, 'home.html', context)

def RegisterView(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, 'registration/register.html', {'form':form})

def LoginView(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                msg= 'Invalid Email or Password'
        else:
            msg = 'Invalid Email or Password'
    return render(request, 'registration/login.html', {'form': form, 'msg': msg})
