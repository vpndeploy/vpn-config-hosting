import os
from django.views.generic.base import TemplateView
from django.conf import settings

pac_modes = ["default", "auto", "whitelist", "whitelistip"]
protocols = ['http', 'socks5', 'https']

intranet_addresses = [
  ["127.0.0.0", "255.0.0.0"],
  ["10.0.0.0", "255.0.0.0"],
  ["172.16.0.0", "255.0.0.0"],
  ["192.168.0.0", "255.255.0.0"],
]


class PacView(TemplateView):

    def get_template_names(self):
        return ["pac/proxy.%s.pac" % self.kwargs['mode'], "pac/proxy.pac"]
        
    def get_context_data(self, **kwargs):
        context = super(PacView, self).get_context_data(**kwargs)
        if context.get('servers'):
            context['proxy'] = self.convert_proxy_string(context.get('servers'))
        else:
            context['proxy'] = self.build_proxy_item(
                context['protocol'], context['host'], context['port'])

        context['intranet_addresses'] = intranet_addresses
        return context

    def convert_proxy_string(self, data):
        plist = []
        for item in data.split("/"):
            protocol, host, port = item.split("_", 2)
            plist.append(self.build_proxy_item(protocol, host, port))
        return "".join(plist)

    def build_proxy_item(self, protocol, host, port):
        context = {'host' : host, 'port' : port}
        if protocol == 'https':
            return "HTTPS %(host)s:%(port)s;" % context
        elif protocol == 'socks5':
            return "SOCKS5 %(host)s:%(port)s; SOCKS %(host)s:%(port)s;" % context
        elif protocol == 'http':
            return "PROXY %(host)s:%(port)s;" %context

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
