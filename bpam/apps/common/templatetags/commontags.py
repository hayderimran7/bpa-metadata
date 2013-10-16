from django import template

register = template.Library()

from django import template
from bpam import __version__ as bpam_version

class BpamVersionNode(template.Node):
    def render(self, context):
        return "%s" % (bpam_version)

def do_bpam_version(parser, token):
    return BpamVersionNode()

register.tag('bpam_version', do_bpam_version)

print "register code ran"
