"""
Allow users to subsribe to content i.e get regular updates on post
 """

from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post


class LatestPostFeed(Feed):
    title = "My blog"
    link = '/blog/'
    description = 'New posts for my blog.'

    def items(self):
        """Get the last 5 published posts """
        return Post.published.all()[:5]
    
    #* below methods receive each an object returned by items 
    # and return the title and description
    def item_title(self,item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)
