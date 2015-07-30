import os as _os
_on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not _on_rtd:
    import h5py as _h5

from .classes import Data


def E200_load_local(filename, orig_file=None):
    """
    .. versionadded:: 1.4

    Load a previously-saved file to avoid having to reprocess everything through Matlab.
    """
    f = _h5.File(filename, 'r', driver='core', backing_store=False)
    return Data(read_file = f, filename=orig_file)
