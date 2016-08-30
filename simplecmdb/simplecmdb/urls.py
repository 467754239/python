from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^api/collect/?$', 'hostinfo.views.collect'),
    url(r'^api/collect.json$', 'hostinfo.views.collectjson'),
    url(r'^api/gethosts\.json$', 'hostinfo.views.gethosts'),
    url(r'^api/gethosts$', 'hostinfo.views.gethoststxt'),
    url(r'^api/gethostbyident$', 'hostinfo.views.getHostByIdentity'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
