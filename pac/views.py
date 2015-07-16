import os
from django.views.generic.base import TemplateView
from django.conf import settings

pac_modes = ["default", "gfwlist", "chnroutes", "whitelist"]
protocols = ['http', 'socks5', 'https']

intranet_addresses = [
  ["127.0.0.0", "255.0.0.0"],
  ["10.0.0.0", "255.0.0.0"],
  ["172.16.0.0", "255.0.0.0"],
  ["192.168.0.0", "255.255.0.0"],
]

GFWLIST_FILE = os.path.join(os.path.dirname(__file__), 'gfwlist.txt')

class PacView(TemplateView):

    def get_template_names(self):
        return ["pac/proxy.%s.pac" % self.kwargs['mode'], "pac/proxy.pac"]
        
    def get_context_data(self, **kwargs):
        context = super(PacView, self).get_context_data(**kwargs)
        context['intranet_addresses'] = intranet_addresses
        if self.kwargs['mode'] == 'gfwlist':
            context.update(self.build_from_gfwlist())
        return context

    def build_from_gfwlist(self):
        from gfwlist2pac.main import parse_gfwlist, reduce_domains, decode_gfwlist, combine_lists
        with open(GFWLIST_FILE, 'r') as fp:
            content = fp.read()
        content = decode_gfwlist(content)
        gfwlist = combine_lists(content, None)
        domains = parse_gfwlist(gfwlist)
        domains = reduce_domains(domains)
        return {
            'domains': domains
        }

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
