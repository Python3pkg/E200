import os as _os
_on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not _on_rtd:
    import numpy as _np
    import h5py as _h5

import ipdb as pdb
import re as _re
import logging as _logging
_logger = _logging.getLogger(__name__)

from .E200_Dat import E200_Dat
__all__ = ['E200_api_getdat', '_numarray2str']


def _numarray2str(numarray):
    chars = [chr(val) for val in numarray.flatten()]
    string = ''.join(chars)
    return string


def E200_api_getdat(dataset, UID=None, fieldname='dat', default=None):
    """
    Load data from a *dataset*, which must be either an :class:`E200.Drill` or an :class:`h5py.Group` class. If no *UID* is given, all available UIDs are loaded. The *fieldname* determines which member is loaded from the *dataset*.

    Returns an instance of :class:`E200.E200_Dat`.
    """
    if type(dataset) != _h5.Group:
            dataset = dataset._hdf5

    _logger.debug('Accessing: {}'.format(dataset.name))
    # ======================================
    # Check version
    # ======================================
    version_bool = 'origin' in dataset.file.attrs.keys()
    if version_bool:
        python_version_bool = (dataset.file.attrs['origin'] == 'python-h5py')
    else:
        python_version_bool = False
    _logger.debug('Matlab version: {}'.format(not python_version_bool))

    # ======================================
    # Get available UIDs in dataset
    # ======================================
    avail_uids = dataset['UID'].value

    if python_version_bool:
        if fieldname == 'dat':
            # ======================================
            # Build data from HDF5 refs
            # ======================================
            dat_refs = dataset['dat'].value
            vals = _np.empty((avail_uids.shape[0], ), dtype=_np.object)

            for i, val in enumerate(dat_refs):
                vals[i] = dataset.file[val].value

        else:
            vals = dataset[fieldname].value

    else:
        if dataset.name == '/data/raw/metadata/E200_state' or dataset.name == '/data/raw/metadata/param':
            return None

        # ======================================
        # Deref if necessary
        # ======================================
        if not _re.match('/data/', dataset.name):
            vals = [dataset.file[val] for val in dataset[fieldname]]
            vals = _np.array(vals)
        else:
            if type(dataset[fieldname][0][0]) == _h5.h5r.Reference:
                vals = [dataset.file[val[0]] for val in dataset[fieldname]]
            else:
                vals = [val for val in dataset[fieldname]]

            if vals[0].shape[0] > 1:
                vals = [_np.array(val).flatten() for val in vals]
                # vals = [''.join(vec.view('S2')) for vec in vals]
                vals = [[chr(vec) for vec in val] for val in vals]
                vals = [''.join(val) for val in vals]
                vals = _np.array(vals)
            else:
                vals = [val[0] for val in vals]
                vals = _np.array(vals)

    avail_uids_num = _np.size(avail_uids)
    _logger.debug('Number of available uids: {}'.format(avail_uids_num))
    if (UID is None):
        # ======================================
        # Return all results if no UID requested
        # ======================================
        out_uids = avail_uids
        out_vals = vals
    elif avail_uids_num == 1:
        # ======================================
        # One UID, matches
        # ======================================
        if avail_uids == UID:
            _logger.debug('Not empty')
            out_uids = _np.array([avail_uids])
            out_vals = _np.array([vals]).flatten()
        # ======================================
        # One uid, no match, no default
        # ======================================
        elif default is None:
            out_uids = _np.array([])
            out_vals = _np.array([])
        # ======================================
        # One UID, no match, default
        # ======================================
        elif default is not None:
            out_uids = _np.array([UID])
            out_vals = _np.array([default])
    else:
        # ======================================
        # Multiple available UIDs
        # ======================================
        valbool  = _np.in1d(avail_uids, UID)
        out_vals = vals[valbool]

        out_uids = avail_uids[valbool]

        # ======================================
        # Fill in default
        # ======================================
        if default is not None:
            default = _np.array(default)

            # ======================================
            # Find UIDs without values
            # ======================================
            diff_uids = _np.setxor1d(avail_uids, UID)
            diff_uids = _np.intersect1d(diff_uids, UID)

            # ======================================
            # If default is the wrong shape, use an
            # array with the first value of default
            # ======================================
            if out_vals.size > 0:
                if default.shape != out_vals[0].shape:
                    default_orig = default
                    default = _np.ones_like(out_vals[0]) * default.flatten()[0]
                    _logger.warning('Default wrong shape: {}. Setting defaults as: {}'.format(default_orig, default), stack_info=True)

            # ======================================
            # Create diff_vals array, right size,
            # with defaults
            # ======================================
            shape = (diff_uids.size,) + default.shape

            diff_vals = _np.empty(shape)
            diff_vals[:] = default

            # ======================================
            # Combine with found uids, values
            # ======================================
            out_uids = _np.concatenate([out_uids, diff_uids])
            out_vals = _np.concatenate([out_vals, diff_vals])

    # ======================================
    # Sort UIDs
    # ======================================
    ind_sort = _np.argsort(out_uids.flatten())
    out_uids  = out_uids[ind_sort]
    out_vals = out_vals[ind_sort]

    n_uids = _np.size(out_uids)
    _logger.debug('Number of UIDs found: {}'.format(n_uids))

    # ======================================
    # Print UIDs for debugging
    # ======================================
    if n_uids > 10:
        _logger.debug('Showing only first 10 UIDs')
        show_uids = out_uids[0:10]
    else:
        show_uids = out_uids

    for uid in show_uids:
        try:
            debug_uid = _np.int64(uid[0])
        except IndexError:
            debug_uid = _np.int64(uid)
        _logger.debug('UID: {:d}'.format(debug_uid))
    #  out_uids = _np.array([out_uids]).flatten()

    return E200_Dat(out_vals, out_uids, field=fieldname)
