from django.views.generic.base import TemplateView
from django.conf import settings
from pac.models import PacGenerator

pac_modes = ["default", "auto", "whitelist", "whitelistip"]
protocols = ['http', 'socks5', 'https']


class PacView(TemplateView):

    def get_template_names(self):
        return [PacGenerator.get_template_name(self.kwargs['mode']), "pac/proxy.pac"]
        
    def get_context_data(self, **kwargs):
        context = super(PacView, self).get_context_data(**kwargs)
        if context.get('servers'):
            context['servers'] = context['servers'].split("/")
        context = PacGenerator.prepare_context(context)
        return context

class PacBuildView(TemplateView):

    def get_template_names(self):
        return ["pac/build.html"];

    def get_context_data(self, **kwargs):
        context = super(PacBuildView, self).get_context_data(**kwargs)
        context['protocols'] = protocols
        context['pac_modes'] = pac_modes
        return context


class PacIndexView(TemplateView):

    template_name = "pac/server_list.html"
    server_list = getattr(settings, 'PAC_SERVER_LIST', [])

    def get_context_data(self, **kwargs):
        context = super(PacIndexView, self).get_context_data(**kwargs)
        context['server_list'] = [self._parse_server(x) for x in self.server_list]
        context['mode_list'] = pac_modes
        return context

    def _parse_server(self, proxy_str):
        protocol, host_port = proxy_str.split("://", 1)
        host, port = host_port.split(":")
        return {"protocol" : protocol, "host" : host, "port" : port}
