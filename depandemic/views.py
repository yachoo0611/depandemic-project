from django.shortcuts import render
from django.http import HttpResponse
from .models import Post


def index(request):
    #twieter 
    #최근 데이터 조회 -최근일 기준 100건까지
    posts = Post.objects.all().order_by('created_date')[:100]
    tweet_posts = Post.objects.all().order_by('created_date')[:1] #트위터 가장 최근글

    return render(request, 'depandemic/index.html', {'form': 'form', 'posts': posts, 'tweet_posts':tweet_posts})


    #return render(request, 'depandemic/index.html')
