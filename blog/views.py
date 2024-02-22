from django.shortcuts import render
from .models import Post
from django.views.generic import ListView,DetailView
# Create your views here.

class BlogListView(ListView): #Regresa una lista del objeto
    model = Post
    template_name = 'home.html'
    context_object_name = 'all_posts_blog'


class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'