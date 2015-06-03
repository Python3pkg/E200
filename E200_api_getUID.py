import numpy as np
# from convertH5ref import convertH5ref as _convertH5ref
from pytools.convertH5ref import convertH5ref as _convertH5ref


def E200_api_getUID(struct, val, f=None):
    if f is None:
        f = struct._hdf5
    uids = struct['UID']
    vals = struct['dat']

    uids = uids[:, 0]
    try:
        vals = _convertH5ref(vals, f)
    except:
        vals = np.array(vals).flatten()

    return uids[vals == val]
