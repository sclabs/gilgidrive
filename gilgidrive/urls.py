from django.conf.urls import patterns, include, url
from django.contrib import admin
from .settings import DEBUG, MEDIA_ROOT, STATIC_ROOT

admin.autodiscover()

urlpatterns = patterns('',
    # drive app
    url(r'^', include('drive.urls')),

    # auth-related URLs
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/loggedout/'}, name='logout'),
    url(r'^switchuser/$', 'django.contrib.auth.views.logout_then_login', name='switchuser'),
    url(r'^loggedout/$', 'gilgidrive.views.loggedout'),
    url(r'^changepassword/$', 'django.contrib.auth.views.password_change', name='changepassword'),
    url(r'^passwordchanged/$', 'django.contrib.auth.views.password_change_done'),
    
    # password reset urls (not working)
    #url(r'^resetpassword/$', 'django.contrib.auth.views.password_reset'),
    #url(r'^resetsent/$', 'django.contrib.auth.views.password_reset_done'),
    #url(r'^setnewpassword/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    #url(r'^setnewpassword/[0-9A-Za-z]+-.+/$', 'django.contrib.auth.views.password_reset_confirm'),
    #url(r'^resetcomplete/$', 'django.contrib.auth.views.password_reset_complete'),

    # admin docs
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # admin
    url(r'^admin/', include(admin.site.urls)),
)

# DEV ONLY!!!!!!!!!!
#
# this magic code snippet allows the dev server to serve anything in media/ and static/
if DEBUG:
    urlpatterns += patterns('',
        #url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT,}),
        #url(r'^static/admin/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_ROOT + '/admin/',}),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_ROOT,})
                            )
