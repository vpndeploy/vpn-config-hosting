from django.views.generic.base import TemplateView
from django.conf import settings

class MobileConfigView(TemplateView):

    template_name = "mobileconfig/ikev2.mobileconfig"

    def get_context_data(self, **kwargs):
        context = super(MobileConfigView, self).get_context_data(**kwargs)
        context['conf_uid'] = "ikev2-%s-%s" %(context['server'], context['vpn_username'])
        context['ca_common_name'] = settings.MOBILE_CONFIG_CA_COMMON_NAME
        context['ca_cert_content'] = settings.MOBILE_CONFIG_CA_CERT_CONTENT
        context['include_password'] = False
        return context
