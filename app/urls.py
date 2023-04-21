
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name = 'index'),
    path('post/<slug:slug>', views.post_page, name='post_page')

]