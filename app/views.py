from django.shortcuts import render, redirect, get_object_or_404
from app.forms import CommentForm, NewUserForm, SubscribeForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db.models import Count
from app.models import Comment, Post, Profile, Tag, WebsiteMeta
from django.db.models import Max, F


# Create your views here.


def index(request):

    posts = Post.objects.all()
    # for top posts in homepage
    top_posts = Post.objects.all().order_by('-view_count')[0:3]
    # for recent posts in homepage
    recent_posts = Post.objects.all().order_by('-last_updated')[0:3]

    featured_blog = Post.objects.filter(isfeatured=True)

    subscribe_form = SubscribeForm()
    subscribe_successful = None
    website_info = None

    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]

    if featured_blog:
        featured_blog = featured_blog[0]

    if request.POST:
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
            request.session['subscribed'] = True
            subscribe_successful = 'Subscribed Successfully'
            # resetting the form
            subscribe_form = SubscribeForm()

    context = {'posts': posts, 'top_posts': top_posts, 'recent_posts': recent_posts,
               'subscribe_form': subscribe_form, 'subscribe_successful': subscribe_successful, 'featured_blog': featured_blog, 'website_info': website_info}
    return render(request, 'app/index.html', context)


def post_page(request, slug):
    post = Post.objects.get(slug=slug)

    comments = Comment.objects.filter(post=post, parent=None)
    form = CommentForm()

    author = post.author
    print(author)

    # bookmark logic
    bookmarked = False
    if post.bookmarks.filter(id=request.user.id).exists():
        bookmarked = True

    is_bookmarked = bookmarked

    # likes logic
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = True

    number_of_likes = post.number_of_likes()

    is_liked = liked

    recent_posts = Post.objects.all().order_by('-last_updated')[0:3]
    related_posts = Post.objects.filter(
        tags__in=post.tags.all()[:1]).order_by('-last_updated')[:3]
    top_posts = Post.objects.filter(
        tags__in=post.tags.all()).order_by('-view_count')[:3]

    # annotate maximum view_count for each tag
    tags_with_max_views = Tag.objects.annotate(
        max_view_count=Max('post__view_count')
    )

    # filter tags based on maximum view_count annotation
    tags = tags_with_max_views.filter(
        post__view_count__gte=F('max_view_count')
    )[:3]

    if request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid:
            parent_obj = None
            if request.POST.get('parent'):
                # save reply
                parent = request.POST.get('parent')
                parent_obj = Comment.objects.get(id=parent)
                if parent_obj:
                    comment_reply = comment_form.save(commit=False)
                    comment_reply.parent = parent_obj
                    comment_reply.post = post
                    comment_reply.save()
                    return HttpResponseRedirect(reverse('post_page', kwargs={'slug': slug}))
            else:
                comment = comment_form.save(commit=False)
                postid = request.POST.get('post_id')
                post = Post.objects.get(id=postid)
                comment.post = post
                comment.save()

                # update the total number of comments
                post.total_comment = Comment.objects.filter(post=post).count()
                post.save()

                return HttpResponseRedirect(reverse('post_page', kwargs={'slug': slug}))

    total_comment = Comment.objects.filter(post=post).count()

    if post.view_count is None:
        post.view_count = 1
    else:
        post.view_count = post.view_count + 1
    post.save()

    context = {'post': post, 'form': form, 'author': author,
               'comments': comments, 'is_bookmarked': is_bookmarked, 'is_liked': is_liked, 'number_of_likes': number_of_likes, 'total_comment': total_comment, 'recent_posts': recent_posts, 'related_posts': related_posts, 'top_posts': top_posts, 'tags': tags}
    return render(request, 'app/post.html', context)


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    top_posts = Post.objects.filter(
        tags__in=[tag.id]).order_by('-view_count')[0:2]
    recent_posts = Post.objects.filter(
        tags__in=[tag.id]).order_by('-last_updated')[0:3]

    tags = Tag.objects.all()

    context = {'tag': tag, 'top_posts': top_posts,
               'recent_posts': recent_posts, 'tags': tags}

    return render(request, 'app/tag.html', context)


def author_page(request, slug):
    profile = Profile.objects.get(slug=slug)
    top_posts = Post.objects.filter(
        author=profile.user).order_by('-view_count')[0:2]
    recent_posts = Post.objects.filter(
        author=profile.user).order_by('-last_updated')[0:2]
    top_authors = User.objects.annotate(number=Count('post')).exclude(
        id=profile.user.id).order_by('-number')[:5]
    context = {'profile': profile, 'top_posts': top_posts,
               'recent_posts': recent_posts, 'top_authors': top_authors}
    try:
        Post.objects.filter(author=profile.user).exists()
    except Post.DoesNotExist:
        top_authors = User.objects.annotate(number=Count('post')).exclude(
            id=profile.user.id).order_by('-number')[:6]
        context['top_authors'] = top_authors
        context['no_posts'] = True
    return render(request, 'app/author.html', context)


def search_posts(request):
    search_query = ''
    if request.GET.get('q'):
        # It checks if the request object has a query parameter 'q' (which is usually added to the URL when a user searches for something). If it exists, it sets the value of search_query to the query parameter value.
        search_query = request.GET.get('q')
    posts = Post.objects.filter(title__icontains=search_query)
    context = {'posts': posts, 'search_query': search_query}

    return render(request, 'app/search.html', context)


def about(request):
    website_info = None
    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]

    context = {'website_info': website_info}
    return render(request, 'app/about.html', context)


def owner(request):

    context = {}
    return render(request, 'app/owner.html', context)


def register_user(request):

    form = NewUserForm()
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    context = {'form': form}

    return render(request, 'registration/registration.html', context)


def bookmark_post(request, slug):

    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.bookmarks.filter(id=request.user.id).exists():
        post.bookmarks.remove(request.user)
    else:
        post.bookmarks.add(request.user)
    return HttpResponseRedirect(reverse('post_page', args=[str(slug)]))


def like_post(request, slug):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post_page', args=[str(slug)]))


def all_bookmarked_posts(request):
    all_bookmarked_posts = Post.objects.filter(bookmarks=request.user)

    context = {'all_bookmarked_posts': all_bookmarked_posts}

    return render(request, 'app/all_bookmarked_posts.html', context)
