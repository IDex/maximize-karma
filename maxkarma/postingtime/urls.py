from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('subreddit/<str:subreddit>', views.get_subreddit, name='get_subreddit')
]
