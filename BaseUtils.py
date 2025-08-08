import os
import sys
import typing

class Version(typing.NamedTuple):
    major: int
    minor: int
    build: int

    def as_simple_string(self) -> str:
        return ".".join(str(item) for item in self)

def tuplize_version(version: str) -> Version:
    return Version(*(int(piece, 10) for piece in version.split(".")))

__version__ = "0.6.3"
version_tuple = tuplize_version(__version__)

instance_name = "MultiworldGG"
archipelago_guid = "{{918BA46A-FAB8-460C-9DFF-AE691E1C865D}}"

def is_frozen() -> bool:
    return typing.cast(bool, getattr(sys, 'frozen', False))


def local_path(*path: str) -> str:
    """
    Returns path to a file in the local MultiworldGG installation or source.
    This might be read-only and user_path should be used instead for ROMs, configuration, etc.
    """
    if hasattr(local_path, 'cached_path'):
        pass
    elif is_frozen():
        if hasattr(sys, "_MEIPASS"):
            # we are running in a PyInstaller bundle
            local_path.cached_path = sys._MEIPASS  # pylint: disable=protected-access,no-member
        else:
            # cx_Freeze
            local_path.cached_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    else:
        import __main__
        if globals().get("__file__") and os.path.isfile(__file__):
            # we are running in a normal Python environment
            local_path.cached_path = os.path.dirname(os.path.abspath(__file__))
        elif hasattr(__main__, "__file__") and os.path.isfile(__main__.__file__):
            # we are running in a normal Python environment, but AP was imported weirdly
            local_path.cached_path = os.path.dirname(os.path.abspath(__main__.__file__))
        else:
            # pray
            local_path.cached_path = os.path.abspath(".")

    return os.path.join(local_path.cached_path, *path)

class ByValue:
    """
    Mixin for enums to pickle value instead of name (restores pre-3.11 behavior). Use as left-most parent.
    See https://github.com/python/cpython/pull/26658 for why this exists.
    """
    def __reduce_ex__(self, prot):
        return self.__class__, (self._value_, )