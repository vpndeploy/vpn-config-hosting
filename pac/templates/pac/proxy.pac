function FindProxyForURL(url, host) {
    if (isPlainHostName(host) || (host == "127.0.0.1") || (host == "localhost")
    {% for subnet,mask in intranet_addresses %}
    || (isInNet(host, "{{ subnet }}", "{{ mask }}"))
    {% endfor %}
    {% for domain in direct_domains %}
    || dnsDomainIs(host, "{{ domain }}")
    {% endfor %} ){
        return  "DIRECT";
    }
    {% if protocol == "spdy" %}
    return  "HTTPS {{ host }}:{{ port }};";
    {% elif protocol == "socks5" %}
    return  "SOCKS5 {{ host }}:{{ port }}; SOCKS {{ host }}:{{ port }};";
    {% endif %}
    {% if protocol == "http" %}
    return  "PROXY {{ host }}:{{ port }};";
    {% endif %}
}
