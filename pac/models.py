from django.template.loader import render_to_string

intranet_addresses = [
  ["127.0.0.0", "255.0.0.0"],
  ["10.0.0.0", "255.0.0.0"],
  ["172.16.0.0", "255.0.0.0"],
  ["192.168.0.0", "255.255.0.0"],
]

class PacGenerator(object):

    @classmethod
    def generate(cls, mode, servers):
        context = {
            'servers' : servers
        }
        return render_to_string(
            cls.get_template_name(mode), 
            cls.prepare_context(context)
        )

    @staticmethod
    def get_template_name(mode):
        return "pac/proxy.%s.pac" % mode
 
    @classmethod
    def prepare_context(cls, context):
        if context.get('servers'):
            context['proxy'] = cls.convert_proxy_string(context.get('servers'))
        else:
            context['proxy'] = cls.build_proxy_item(
                context['protocol'], context['host'], context['port'])
        context['intranet_addresses'] = intranet_addresses
        return context
        
    @classmethod
    def convert_proxy_string(cls, servers):
        plist = []
        for item in servers:
            protocol, host, port = item.split("_", 2)
            plist.append(cls.build_proxy_item(protocol, host, port))
        return "".join(plist)

    @classmethod
    def build_proxy_item(cls, protocol, host, port):
        context = {'host' : host, 'port' : port}
        if protocol == 'https':
            return "HTTPS %(host)s:%(port)s;" % context
        elif protocol == 'socks5':
            return "SOCKS5 %(host)s:%(port)s; SOCKS %(host)s:%(port)s;" % context
        elif protocol == 'http':
            return "PROXY %(host)s:%(port)s;" %context

