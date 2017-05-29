from django.conf.urls import include
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^blogs/$', views.BlogListView.as_view(), name='blogs'),
    url(r'^blogger/(?P<pk>\d+)$', views.BlogListbyAuthorView.as_view(), name='blogs-by-author'),
    url(r'^blog/(?P<pk>\d+)$', views.BlogDetailView.as_view(), name='blog-detail'),
    url(r'^blog/post/(?P<pk>\d+)$', views.PostDetailView.as_view(), name='post-detail'),
    url(r'^bloggers/$', views.BloggerListView.as_view(), name='bloggers'),
    url(r'^blog/post/comment/(?P<pk>\d+)/$', views.PostCommentCreate.as_view(), name='post_comment'),
    url(r'^blog/post/(?P<pk>\d+)/$', views.PostCreate.as_view(), name='post_add'),
    url(r'^blog_add/$', views.BlogCreate.as_view(), name='blog_add'),
    url('^signup/$', views.signup, name='signup'),
    url(r'^search/', include('haystack.urls')),
    url(r'^search/', views.redirectSearch, name='search'),
]
