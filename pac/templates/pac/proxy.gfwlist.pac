{% extends "pac/proxy.pac" %}
{% block main %}
    var domains = {
    {% for domain in domains %}
        "{{ domain }}" : 1,{% endfor %}
    };
    var hasOwnProperty = Object.hasOwnProperty;
    var suffix;
    var pos = host.lastIndexOf('.');
    pos = host.lastIndexOf('.', pos - 1);
    while(1) {
        if (pos <= 0) {
            if (hasOwnProperty.call(domains, host)) {
                return PROXY;
            } else {
                return 'DIRECT';
            }
        }
        suffix = host.substring(pos + 1);
        if (hasOwnProperty.call(domains, suffix)) {
            return PROXY;
        }
        pos = host.lastIndexOf('.', pos - 1);
    }
{% endblock main %}
