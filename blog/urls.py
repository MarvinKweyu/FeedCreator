from django.urls import path
from .import views
from .feeds import LatestPostFeed


app_name = 'blog' # make it posible to call url from another app by reference

urlpatterns = [
    path('',views.post_list,name='post_list'),
    # path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/',views.post_share, name='post_share'),
    path('<int:year>/<slug:post>/',views.post_detail, name='post_detail'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('feed/', LatestPostFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
    # allow owner to manage posts

]
