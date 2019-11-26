from django.shortcuts import render
from django.views.generic import ListView, DetailView
from blog.models import Post
# CRUD
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
# groups
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.


class OwnerMixin(object):
    """ Get object s belonging to current user"""
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(author=self.request.user)


class OwnerEditMixin(object):

    """ When form is submitted , set current user as owner of object"""
    def form_valid(self,form):
        """used by CRUD"""
        form.instance.author = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)


class OwnerPostMixin(OwnerMixin, LoginRequiredMixin):
    model = Post
    # fields to  include in CRUD
    fields = ['title', 'slug','featured_image', 'body', 'publish', 'status']
    success_url = reverse_lazy('management:manage_post_list')
    template_name = 'blog/manage/post/form.html'


class OwnerPostEditMixin(OwnerPostMixin, OwnerEditMixin):
    fields = ['title', 'slug','featured_image', 'body', 'publish', 'status']
    success_url = reverse_lazy('management:manage_post_list')
    template_name = 'blog/manage/post/form.html'


class ManagePostListView(OwnerPostMixin, ListView):
    """List Posts from user.
    Show list of publications
    """
    template_name = 'blog/manage/post/list.html'


class PostCreateView(PermissionRequiredMixin, OwnerPostEditMixin, CreateView):
    """Create a new post"""
    permission_required = 'post.add_post'


class PostEditView(OwnerPostEditMixin, UpdateView):
    """Update a current post"""
    permission_required = 'post.change_post'


class PostDeleteView(PermissionRequiredMixin, OwnerPostMixin, DeleteView):
    """Delete a course"""
    template_name = 'blog/manage/post/delete.html'
    success_url = reverse_lazy('management:manage_post_list')
    permission_required = 'post.delete_post'
    # context_instance = RequestContext(request)
