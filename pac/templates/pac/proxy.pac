function FindProxyForURL(url, host) {
    if (isPlainHostName(host) || (host == "127.0.0.1") || (host == "localhost")
    {% for subnet,mask in intranet_addresses %}
    || (isInNet(host, "{{ subnet }}", "{{ mask }}"))
    {% endfor %}
    return "{{ proxy }}";
}
