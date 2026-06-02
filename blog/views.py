from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from scripts.regsetup import description
from django.db.models import Q
from django.contrib.postgres.search import TrigramSimilarity
from .forms import TicketForm
from .models import *
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    last_post = Post.published.all().order_by('-publish')[0]
    return render(request, "blog/index.html", {"last_post": last_post})

# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/list.html'


def post_list(request, category=None):
    if category is not None:
        posts = Post.published.filter(category=category)
    else:
        posts = Post.published.all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    print(posts, type(posts))
    context = {
        'posts': posts,
        'category': category
    }
    return render(request, "blog/list.html", context)


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk, status=Post.Status.PUBLISHED)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }
    return render(request, 'blog/detail.html', context)

# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'blog/detail.html'

def ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket_obj = Ticket.objects.create()
            cd = form.cleaned_data
            ticket_obj.message = cd['message']
            ticket_obj.name = cd['name']
            ticket_obj.email = cd['email']
            ticket_obj.phone = cd['phone']
            ticket_obj.subject = cd['subject']
            ticket_obj.save()
            return redirect("blog:index")
    else:
        form = TicketForm()
    return render(request, 'forms/ticket.html', {'form': form})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {'post': post, 'comment': comment, 'form': form}
    return render(request, 'forms/comment.html', context)


@login_required
def create_post(request):
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(image_file=form.cleaned_data['image1'], post=post)
            Image.objects.create(image_file=form.cleaned_data['image2'], post=post)
            return redirect('blog:profile')
    else:
        form = CreatePostForm()
    return render(request, 'forms/create_post.html', {'form': form})


def post_search(request):
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results1 = (Post.objects.annotate(similarity=TrigramSimilarity('title', query))
                .filter(similarity__gt=0.1))
            results2 = (Post.objects.annotate(similarity=TrigramSimilarity('description', query))
                .filter(similarity__gt=0.1))
            results3 = (Post.objects.annotate(similarity=TrigramSimilarity('images__title', query))
                .filter(similarity__gt=0.1))
            results = (results1 | results2 | results3).order_by('-similarity').distinct()
    context = {'results': results, 'query': query}
    return render(request, 'blog/search.html', context)


@login_required
def profile(request):
    user = request.user
    posts = Post.objects.filter(author=user)
    return render(request, 'blog/profile.html', {'posts': posts})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        post.delete()
        return redirect('blog:profile')
    else:
        return render(request, 'forms/delete_post.html', {'post': post})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(image_file=form.cleaned_data['image1'], post=post)
            Image.objects.create(image_file=form.cleaned_data['image2'], post=post)
            return redirect('blog:profile')
    else:
        form = CreatePostForm(instance=post)
    return render(request, 'forms/create_post.html', {'form': form, 'post': post})

@login_required
def delete_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    image.delete()
    return redirect('blog:profile')


# def user_login(request):
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return redirect('blog:profile')
#                 else:
#                     return HttpResponse('Your account is disabled.')
#             else:
#                 return HttpResponse('You are not logged in')
#     else:
#         form = LoginForm()
#     return render(request, 'forms/login.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect('blog:index')
