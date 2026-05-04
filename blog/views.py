from django.http import Http404
from django.shortcuts import render
from .models import Post

# Create your views here.
def index(request):
    pass


def post_list(request):
    posts = Post.published.all()
    context = {
        'posts': posts,
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, id):
    try:
        post = Post.published.get(id=id)
    except:
        raise Http404("Post does not exist")
    context = {
        'post': post,
    }
    return render(request, 'blog/post_detail.html', context)