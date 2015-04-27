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

class MobileConfigIndexView(TemplateView):

    template_name = "mobileconfig/multiserver_config_list.html"
    server_list = getattr(settings, 'MOBILE_CONFIG_SERVER_LIST', [])

    def get_context_data(self, **kwargs):
        context = super(MobileConfigIndexView, self).get_context_data(**kwargs)
        context['server_list'] = self.server_list
        return context

class MultiServerMobileConfigView(TemplateView):

    template_name = "mobileconfig/multiserver.ikev2.mobileconfig"
    server_list = getattr(settings, 'MOBILE_CONFIG_SERVER_LIST', [])

    def get_context_data(self, **kwargs):
        context = super(MultiServerMobileConfigView, self).get_context_data(**kwargs)
        server_list = self.request.GET.get("server_list", "").strip()
        if server_list == "":
            server_list = self.server_list
        else:
            server_list = server_list.split(",")

        context['payloads'] = [
            {"server" :  server, "id" : "ikev2-%s-%s" %(server, context["vpn_username"])}
            for server in server_list
        ]
        context['conf_uid'] = "ikev2-%s" %(context['vpn_username'])
        context['ca_common_name'] = settings.MOBILE_CONFIG_CA_COMMON_NAME
        context['ca_cert_content'] = settings.MOBILE_CONFIG_CA_CERT_CONTENT
        context['include_password'] = False
        return context
