from django.shortcuts import render_to_response
from django.template import RequestContext

from blog.models import Post

def index(request):
    posts = Post.objects.order_by('-date')[:5]
    return render_to_response('blog/index.html',
                              {'posts' : posts},
                              context_instance = RequestContext(request))
