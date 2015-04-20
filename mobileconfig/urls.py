from django.conf.urls import include, url
from mobileconfig.views import MobileConfigView

urlpatterns = [
    url(r'^(?P<vpn_username>[^/]+)/(?P<server>[\w\.\-]+).mobileconfig$',
        #MobileConfigView.as_view(content_type="application/octet-stream"), name='mobile_config'),
        MobileConfigView.as_view(content_type="text/plain"), name='mobile_config'),
]

