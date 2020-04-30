from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home_view(request,*args, **kwargs):
    return HttpResponse("<h1>Hello world</h1>")

def tweet_detail_view(request, tweet_id, *args, **kwargs):
    return HttpResponse(f"<h1>Tweet {tweet_id}</h1>")