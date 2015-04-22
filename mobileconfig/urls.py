from django.conf.urls import include, url
from mobileconfig.views import MobileConfigView, MultiServerMobileConfigView

urlpatterns = [
    url(r'^(?P<vpn_username>[^/]+)/(?P<server>[\w\.\-]+).mobileconfig$',
        MobileConfigView.as_view(content_type="application/octet-stream"), name='mobile_config'),
    url(r'^(?P<vpn_username>[^/]+).mobileconfig$',
        MultiServerMobileConfigView.as_view(content_type="application/octet-stream"), name='multi_server_mobile_config'),

    #for DEBUG
    url(r'^(?P<vpn_username>[^/]+)/(?P<server>[\w\.\-]+).mobileconfig.txt$',
        MobileConfigView.as_view(content_type="text/plain"), name='mobile_config_txt'),
    url(r'^(?P<vpn_username>[^/]+).mobileconfig.txt$',
        MultiServerMobileConfigView.as_view(content_type="text/plain"), name='multi_server_mobile_config_txt'),
]

