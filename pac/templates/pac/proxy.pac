function FindProxyForURL(url, host) {
    {% block proxy_set %}
    {% if protocol == "https" %}
    var PROXY = "HTTPS {{ host }}:{{ port }};";
    {% elif protocol == "socks5" %}
    var PROXY = "SOCKS5 {{ host }}:{{ port }}; SOCKS {{ host }}:{{ port }};";
    {% endif %}
    {% if protocol == "http" %}
    var PROXY = "PROXY {{ host }}:{{ port }};";
    {% endif %}
    {% endblock %}
    {% block intranet_check %}
    if (isPlainHostName(host) || (host == "127.0.0.1") || (host == "localhost")
    {% for subnet,mask in intranet_addresses %}
    || (isInNet(host, "{{ subnet }}", "{{ mask }}"))
    {% endfor %}
    {% for domain in direct_domains %}
    || dnsDomainIs(host, "{{ domain }}")
    {% endfor %} ){
        return  "DIRECT";
    }
    {% endblock %}
    {% block main %}
    {% endblock %}
    {% block default_action %}
    return PROXY;
    {% endblock %}
}
