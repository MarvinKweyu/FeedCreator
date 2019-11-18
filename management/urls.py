from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name='management'

urlpatterns = [
    # let sofia log in
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('myposts/', views.ManagePostListView.as_view(), name='manage_post_list'),
    # path(),
]