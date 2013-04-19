from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required

from .views import *

urlpatterns = patterns('drive.views',
    url(r'^$', login_required(RecentView.as_view()), name='recent'),
    url(r'^category/(?P<name>\w+)/$', login_required(CategoryView.as_view()), name='category'),
    url(r'^add/$', login_required(AddView.as_view()), name='add'),
    url(r'^edit/(?P<pk>\d+)/$', login_required(EditView.as_view()), name='edit'),
    url(r'^delete/(?P<pk>\d+)/$', login_required(DeleteView.as_view()), name='delete'),
    url(r'^file/(?P<pk>\d+)/$', login_required(FileView.as_view()), name='file'),
    url(r'^all/$', login_required(AllView.as_view()), name='all'),
    url(r'^changelog/$', ChangelogView.as_view(), name='changelog'),
    url(r'^search/$', login_required(SearchView.as_view()), name='search'),
)
