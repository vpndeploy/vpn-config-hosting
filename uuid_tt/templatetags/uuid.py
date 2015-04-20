from __future__ import absolute_import
from django import template
import uuid
BASE_UUID = uuid.UUID("{FB319859-FB1F-402E-84A2-460A1FB35E4E}")

register = template.Library()

@register.filter
def uuid5(arg1, arg2=None):
    def _to_str(v):
        if type(v) is unicode:
            return v.encode("utf-8")
        else:
            return str(v)
    v = arg1
    if arg2 is not None:
        v += ":" + _to_str(arg2)
    return unicode(uuid.uuid5(BASE_UUID, v))
