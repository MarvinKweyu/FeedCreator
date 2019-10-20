from django.shortcuts import render,get_object_or_404
from .models import Post,Comment
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from django.views.generic import ListView
from .forms import EmailPostForm,CommentForm, SearchForm
from django.core.mail import send_mail # allow mail sending
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector,SearchQuery, SearchRank
# Create your views here.


def post_list(request,tag_slug=None):
    """Get a list of posts"""
    object_list = Post.published.all() # get all published posts

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag]) # filter by the ones that have a given tag
        
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page') # to indicate the current page number
    try:
        posts = paginator.page(page) #obtain objects of page
    except PageNotAnInteger:
        # if page is not an integer,deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range,deliver the last page of results
        posts = paginator.page(paginator.num_pages)
     
    # return the page number and number of objects 
    return render(request,'blog/post/list.html', {'page':page, 'posts':posts, 'tag':tag})   


def post_detail(request, year, post):
    """ Display details of a single post"""

    post = get_object_or_404(Post, slug=post,
                                    status='published',
                                    publish__year=year,
                                    # publish__month=month,
                                    # publish__day=day
                                    )

    # list active comments for post.Note use of comments from related_name in comment model
    """ 
    Note:
    The related name for the foreign key in comment model is 'comments'
    Hence, we can say retrieve the post of this comment using comment.post
    We can also say to this post, get its comments using post.comments
    """
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # new comment posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # create comment object but don't save yet
            new_comment = comment_form.save(commit=False)
            # assign current post to comment
            new_comment.post = post
            # save to database
            new_comment.save()
    else:
        comment_form = CommentForm() # ender form with validation errors
    
    # list of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True) #retrieve list of IDS of tags of this post
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id) #exclude this post we are watching
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    return render(request, 'blog/post/detail.html', {'post': post,
                                                      'comments':comments, 
                                                      'comment_form':comment_form,
                                                      'similar_posts':similar_posts
                                                      })

# ToDo find out why I can't add month and year to the get_absolute_url method


class PostListView(ListView):
    queryset = Post.published.all() # alternatively model = Post
    context_object_name = 'posts' # default is object_list if this variable is unspecified
    paginate_by = 3
    template_name = 'blog/post/list.html' # default usu blog/post_list.html


def post_share(request,post_id):
    """Allow a post to be shared via mail"""
    # retrieve post by id
    post = get_object_or_404(Post,id=post_id, status='published')
    sent = False
   
    if request.method == 'POST':
        # form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form fields passed validation
            cd = form.cleaned_data #* a dictionary type object
            
            # send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']}({cd['email']}) recommends you reading '{post.title}'"
            message= f"Read '{post.title}' at {post_url}\n\n{cd['name']}\'s comments:{cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com',[cd['to']])

            sent=True
    else:
        form = EmailPostForm() # display the from again to correct errors
    return render(request,'blog/post/share.html',{'post':post, 'form': form,'sent':sent })
    

def post_search(request):
    """Allow text matching search. """
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET: # check if result is submitted by looking for query
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # results = Post.objects.annotate(search=SearchVector('title','body'),).filter(search=query)
            # a search is more relevant if the search term is in the title
            """ 
            Search weights are D,C,B and A corresponding to 0.1,0.2,0.4 and 1.0
            """
            search_vector = SearchVector('title', weight='A') + SearchVector('body',weight='B')
            search_query = SearchQuery(query)
            # filter results to display only the ones ranking higher than 0.3
            results = Post.objects.annotate(search=search_vector,rank=SearchRank(search_vector,search_query)
                                            ).filter(rank__gte=0.3).order_by('-rank')

    return render(request,'blog/post/search.html', {'form':form, 'query':query, 'results':results})