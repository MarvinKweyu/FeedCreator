from django.urls import path
from . import views

urlpatterns = [
    path(' ', views.ManagePostListView.as_view(), name='manage_post_list'),
]