
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name = 'index'),
    path('post/<slug:slug>', views.post_page, name='post_page'),
    path('tag/<slug:slug>', views.tag_page, name='tag_page'),
    path('author/<slug:slug>', views.author_page, name='author_page'),
]