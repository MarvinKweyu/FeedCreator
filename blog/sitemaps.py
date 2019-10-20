from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9 # max usu 1.Indicates relevance in our website

    def items(self):
        return Post.published.all() # what should be included in this sitemap

    def lastmod(self,obj):
        """Receive each object retured from items() and 
        return the last time the object was modified. """
        return obj.updated