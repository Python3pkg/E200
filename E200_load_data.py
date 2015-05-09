import tempfile
from .classes import *
import numpy as np
import h5py as _h5
import subprocess
import shlex
import os
import re
from .E200_dataset2str import *
from .get_valid_filename import *
from warnings import warn
import mytools.qt as mtqt
from PyQt4 import QtGui
# from PyQt4 import QtCore
import logging
loggerlevel = logging.DEBUG
logger = logging.getLogger(__name__)

# import ipdb

__all__ = ['E200_load_data']


def E200_load_data(filename, writefile = None, verbose = False, readonly = False, local = False):
    logger.log(level = loggerlevel, msg = 'Input is: filename={}'.format(filename))

    # ======================================
    # Get a verified filename
    # ======================================
    if local:
        vfn = Filename(path='temp.mat', local=local)
    else:
        vfn = Filename(path=filename, local=local)
    processed_path = vfn.processed_path

    logger.log(level=loggerlevel, msg='Processed file path is: processed_file_path={}'.format(processed_path))

    # ======================================
    # Create temporary directory
    # ======================================
    with tempfile.TemporaryDirectory() as tempdir:
        tempfilename = 'temp.h5'
        temppath = os.path.join(tempdir,tempfilename)

        # ======================================
        # Have matlab process file
        # ======================================
        logger.log(level=loggerlevel, msg='Processed file not found, calling matlab to process file.')
        pwd = os.getcwd()
        # matlab = '/Applications/MATLAB_R2014b.app/bin/matlab -nodisplay -nosplash'
        matlab = 'fmatlab -nodisplay -nosplash'
        command = '{matlab} -r "addpath(fullfile(getenv(\'HOME\'),\'E200_DRT/E200_data/\'),\'~/python-dev-modules/E200/\');cd(\'{pwd}\');convert_mat_file(\'{filename}\',\'{outfile}\');exit;"'.format(matlab=matlab, pwd=pwd, filename=filename, outfile=temppath)
        
        logger.log(level=loggerlevel, msg='Command given is: {}'.format(command))
        subprocess.call(shlex.split(command))

        # ======================================
        # Load file processed by matlab
        # ======================================
        logger.log(level=loggerlevel, msg='Loading processed file')
        f = _h5.File(temppath, 'r', driver='core', backing_store=False)

        output = Data(read_file = f)

        return output
        # loadreq = E200_dataset2str(output.rdrill.data.VersionInfo.loadrequest)
        # logger.log(level=loggerlevel, msg='Load request: {}'.format(loadreq))

        # # ======================================
        # # Determine if the loaded file matches
        # # the requested file
        # # ======================================
        # if loadreq == filename:
        #     logger.log(level=loggerlevel, msg='Request matches loaded file, continuing...')
        #     return output
        # else:
        #     logger.log(level=loggerlevel, msg='Request doesn''t match loaded file, removing processed file and retrying...')
        #     try:
        #         os.remove(vfn.processed_path)
        #     except OSError:
        #         pass

        #     try:
        #         os.remove(vfn.py_processed_path)
        #     except OSError:
        #         pass
        #     ipdb.set_trace()
        #     return E200_load_data(
        #         filename   = filename,
        #         writefile  = writefile,
        #         verbose    = verbose,
        #         readonly   = readonly,
        #         local      = local
        #         )


def _load_data(wf):
    processed = wf.create_group('/data/processed')
    groups    = ['arrays', 'scalars', 'images', 'vectors']
    for val in groups:
        processed.create_group(val)

    wf.flush()


class datalevel(object):
    pass


def recursivePopulate(h5data, objData):
    for i, val in enumerate(h5data):
        if type(h5data[val]) == _h5._hl.group.Group:
            setattr(objData, val, datalevel())
            recursivePopulate(h5data[val], getattr(objData, val))
        else:
            setattr(objData, val, h5data[val])
