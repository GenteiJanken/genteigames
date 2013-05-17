from django.conf.urls import url, patterns, include

urlpatterns = patterns('blog.views',
    url(r'^$', 'index'),
)
