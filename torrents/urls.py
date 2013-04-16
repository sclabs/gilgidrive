from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required

from .views import *

urlpatterns = patterns('torrents.views',
    url(r'^$', login_required(RecentView.as_view()), name='recent'),
    url(r'^category/(?P<name>\w+)/$', login_required(CategoryView.as_view()), name='category'),
    url(r'^add/$', login_required(AddView.as_view()), name='add'),
    url(r'^edit/(?P<pk>\d+)/$', login_required(EditView.as_view()), name='edit'),
    url(r'^torrent/(?P<pk>\d+)/$', login_required(TorrentView.as_view()), name='torrent'),
    url(r'^all/$', login_required(AllView.as_view()), name='all'),
    url(r'^changelog/$', ChangelogView.as_view(), name='changelog'),
)
