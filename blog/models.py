from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime

from taggit.managers import TaggableManager # allow tags

# Create your models here.


class PublishedManager(models.Manager):
    """Iteract with the Published posts directly
    """
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')
    

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published'),
    )
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,unique_for_date='publish') #URL SEO friendly
    # a user can have multiple posts
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True) # auto_now_add saves date automatically while creating
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')

    # give different manager
    objects = models.Manager() # the default manager
    published = PublishedManager() # custom model manager

    tags = TaggableManager()

   
    class Meta:
        # sort latest posts first when query to database is done hence -ve
        ordering = ('-publish',)

    def __str__(self):
        """human readable representation of object"""
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                        args=[self.publish.year,
                        # self.publish.month,
                        # self.publish.day,
                        self.slug])


class Comment(models.Model):
    """Allow users to comment on posts
    Creates a blog_comment table in database
     """
    
    # foreign key: a post can have multiple comments from the same person
    # * Related name refers to attribute we use for the relationship btn model
    # without related name, Django uses name of class i.e comment followed by _set i.e *comment_set
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True) # allow manual deactivation of inappropriate comments

    class Meta:
        ordering = ('created',) # sort by chronological order by default

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
