from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^web_user_search/$', 'web_user_search.views.index'),
    (r'^web_user_search/new$', 'web_user_search.views.new_user'),
    (r'^web_user_search/search$', 'web_user_search.views.search'),
    # Example:
    # (r'^LearnDjango/', include('LearnDjango.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
