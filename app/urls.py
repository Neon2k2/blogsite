
from . import views
from django.urls import path

urlpatterns = [
    path('post/<slug:slug>', views.post_page, name='post_page')

]