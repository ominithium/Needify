from django.conf.urls import patterns, include, url



from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'projects.views.index', name='home'),
    url(r'^add_needed/', 'projects.views.add_needed', name="add_needed"),
    url(r'^about/$', 'projects.views.aboutus', name="aboutus"),
    url(r'^register/$', 'projects.views.register', name='register'),
    url(r'^login/$', 'projects.views.user_login', name="login"),
    url(r'^logout/$', 'projects.views.user_logout', name="logout"),
    url(r'^needed/(?P<needed_title_url>\w+)/$', 'projects.views.detail', name="needed"),
    url(r'^needed/(?P<needed_title_url>\w+)/votes/$', 'projects.views.vote', name='vote'),
    url(r'^user/(?P<user_url>\w+)/$', 'projects.views.userPage', name='UserPage'),
    url(r'^captcha/', include('captcha.urls')),
    
    url(r'^admin/', include(admin.site.urls)),
)
