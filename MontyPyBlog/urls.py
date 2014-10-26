from django.conf.urls import patterns, url
from MontyPyBlog import views


urlpatterns = patterns(
    '',
    # Ex: /cms/
    url(r'^$', views.index, name='index'),
    # Ex: /cms/post/7/
    url(r'^post/(?P<post_id>\w+)/$', views.get_post, name='getPost'),
    # Ex: /cms/post/patch/7/
    url(r'^post/patch/(?P<post_id>\w+)/$', views.patch_post, name='patchPost'),
    # Ex: /cms/post/create/
    url(r'^post/create/(?P<user_id>\w+)/$', views.post_post, name='postPost'),
    # Ex: /cms/user/7/
    url(r'^user/(?P<user_id>\w+)/$', views.get_user, name='getUser'),
    # Ex: /cms/user/patch/7/
    url(r'^user/patch/(?P<user_id>\w+)/$', views.patch_user, name='patchPost'),
    # Ex: /cms/user/login/7/
    url(r'^user/login/(?P<user_id>\w+)/$', views.post_login, name='postLogin'),
    # Ex: /cms/user/logout/7/
    url(r'^user/logout/(?P<user_id>\w+)/$', views.post_logout, name='postLogout'),
)
