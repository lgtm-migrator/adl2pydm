"""
MEDM text widget with dynamic attribute should be a PyDMLabel.

- screen: xxx-R6-0.adl
- three instances with names: text text_1 text_2

Also, all PV names in the display rules should start with the ``ca://`` protocol
specification.  Each of these widgets has one PV name for testing.
"""

import os
import pytest

from xml.etree import ElementTree

from . import _core
from ._core import tempdir


@pytest.mark.parametrize("key", "text text_1 text_2".split())
def test_issue62_fixed(key, tempdir):
    assert os.path.exists(tempdir)

    _core.convertAdlFile("xxx-R6-0.adl", "/tmp")  # TODO: developer

    uiname = _core.convertAdlFile("xxx-R6-0.adl", tempdir)
    full_uiname = os.path.join(tempdir, uiname)
    _core.assertTrue(os.path.exists(full_uiname))

    root = ElementTree.parse(full_uiname).getroot()
    screen = _core.getSubElement(root, "widget")
    composite = _core.getNamedWidget(screen, "composite")

    widget = _core.getNamedWidget(composite, key)
    assert widget is not None
    # _core.assertEqualClassName(widget, "PyDMLabel", key)
    _core.assertEqualPropertyString(widget, "text", "Moving")
    # test for "ca://" prefix on PV in the display rules
    prop = _core.getNamedProperty(widget, "rules")
    rules = _core.getSubElement(prop, "string")
    k = '"channel":'
    pos = rules.text.find(k)
    assert pos > 0
    fragment = rules.text[pos+len(k):].strip().strip('"')
    assert len(fragment) > 0
    assert fragment.startswith("ca://xxx:")
