from django.shortcuts import render
from app.forms import CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from app.models import Comment, Post

# Create your views here.

def index(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'app/index.html', context)

def post_page(request, slug):
    post = Post.objects.get(slug = slug)

    comments = Comment.objects.filter(post = post)

    # comments form
    form = CommentForm()
    
    
    if request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid:
            # geting commit false will help us to add values to the object before saving it to the database
            comment = comment_form.save(commit=False)
            postid = request.POST.get('post_id')
            post = Post.objects.get(id = postid )
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('post_page', kwargs={'slug':slug}))

    # view counts
    if post.view_count is None:
        post.view_count = 1
    else:
        post.view_count += 1
    
    post.save()
    context = {'post': post, 'form': form, 'comments': comments}
    return render(request, 'app/post.html', context)