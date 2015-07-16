from django.conf.urls import url
from pac.views import PacView
from pac.views import PacIndexView, PacBuildView

urlpatterns = [
    url(r'^$',
        PacIndexView.as_view(content_type="text/html"), name='pac_index'),

    url(r'^build/$',
        PacBuildView.as_view(content_type="text/html"), name='build_pac'),

    url(r'^(?P<mode>[^/]+)/(?P<protocol>(https|socks5|http))/(?P<host>[\w\.\-]+)_(?P<port>\d+).pac$',
        PacView.as_view(content_type="application/x-javascript-config"), name='pac'),

    url(r'^(?P<mode>[^/]+)/(?P<protocol>(https|socks5|http))/(?P<host>[\w\.\-]+)_(?P<port>\d+).txt$',
        PacView.as_view(content_type="text/plain"), name='pac-txt'),
]
