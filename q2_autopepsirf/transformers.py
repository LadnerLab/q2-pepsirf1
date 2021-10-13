import lxml.etree

from q2_reveal.plugin_setup import plugin
from q2_reveal.format_types import RevealSectionsFormat


@plugin.register_transformer
def _0(ff: RevealSectionsFormat) -> lxml.etree._Element:
    with ff.open() as fh:
        return lxml.etree.fromstring(fh.read())


@plugin.register_transformer
def _1(data: lxml.etree._Element) -> RevealSectionsFormat:
    ff = RevealSectionsFormat()
    # Need to use the `.path` because lxml produces Bytes rather than Strings.
    with ff.path.open(mode='w+b') as fh:
        fh.write(lxml.etree.tostring(data))

    return 