"""shared classes definitions"""
from lxml.etree import _Element, Element

from abc import ABC

xml = "{http://www.w3.org/XML/1998/namespace}"


class StructuralElement(ABC):
    """Base class for all Structural Elements"""

    def __init__(self) -> None:
        self.name = self.__class__.__name__
        super().__init__()

    @property
    def _attrib(self) -> dict[str, str]:
        """dict with tmx compliant key:value pairs. used when building lxml element"""
        attrs: dict = dict()
        for key in vars(self).items():
            if key == "lang":
                attrs[f"{xml}lang"] = getattr(self, key)
            elif key in ["tmf", "encoding"]:
                attrs[f"o-{key}"] = getattr(self, key)
            elif key == "prop_type":
                attrs["type"] = getattr(self, key)
            else:
                attrs[key] = getattr(self, key)
        return attrs

    @property
    def _element(self) -> _Element:
        """lxml Element representation of the class."""
        elem: _Element = Element(self.name)
        for key, value in self._attrib.items():
            if value is not None:
                elem.set(key, value)
        return elem
