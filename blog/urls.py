from django.conf.urls import url, include

from .views import *
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
# from django.contrib.flatpages import sitemaps
from django.views.decorators.cache import cache_page




urlpatterns = [
    url(r'^$', Post_list.as_view()),
    url(r'^search/$', search),
    url(r'^contact/$', contact),
    url(r'^authors/$', Authors.as_view()),
    url(r'^(?P<pk>\d+)$', Post_list_detail.as_view()),

    url(r'^logout/$', logout_page),
    # url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'},),
    url(r'^login/$', auth_views.login),  # If user is not login it will redirect to login page
    # url(r'^login/$', login_user),  # If user is not login it will redirect to login page
    url(r'^register/$', register),

    url(r'^my_view/$', my_view),
    # url(r'^my_view_choose/$', cache_page(60 * 15)(my_view_choose)),
    url(r'^my_view_choose/$', my_view_choose),
    url(r'^register_success/$', register_success),

    url(r'^big_csv/$', some_streaming_csv_view),
    url(r'^csv/$', download_csv),
    url(r'^pdf/$', pdf_downloader),
    url(r'^img/$', img_downloader),

    url(r'^internalization/$', internalization),
    url(r'^test/$', test),



    # url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
    # name='django.contrib.sitemaps.views.sitemap')

]
