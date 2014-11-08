from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'cmsAPI.views.home', name='home'),
    # url(r'^cmsAPI/', include('cmsAPI.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # Points urlconf to the api.urls, which will then handle our urls
    url(r'^cms/', include('MontyPyBlog.urls')),
    # OAuth2
    url(r'^oauth2/', include('provider.oauth2.urls', namespace='oauth2')),
)
