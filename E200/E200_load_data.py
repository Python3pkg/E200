from .E200_dataset2str import *     # NOQA
from .classes import *              # NOQA
from .get_valid_filename import *   # NOQA
from .get_matlab import get_matlab
import logging
import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import h5py as _h5
import shlex
import subprocess
import tempfile
loggerlevel = logging.DEBUG
logger      = logging.getLogger(__name__)

__all__ = ['E200_load_data']


def E200_load_data(filename, savefile=None):
    """
    Loads  dataset file where *filename* is a :code:`str` of the relative location of the file (i.e. ``nas/nas-li20-pm00/E200/2015/20150602/E200_17712``). If specified, saves the intermediate h5py file to *savefile*.

    Returns an instance of :class:`E200.Data`.

    *Note: this function calls Matlab code; it is not surprising to see Matlab open in the terminal.*
    """
    logger.log(level = loggerlevel, msg = 'Input is: filename={}'.format(filename))

    # ======================================
    # Create temporary directory
    # ======================================
    if savefile is None:
        with tempfile.TemporaryDirectory() as tempdir:
            tempfilename = 'temp.h5'
            temppath = _os.path.join(tempdir, tempfilename)
            return _process_file(filename=filename, temppath=temppath)
    else:
        return _process_file(filename=filename, temppath=savefile)


def _process_file(filename, temppath):
    # ======================================
    # Have matlab process file
    # ======================================
    logger.log(level=loggerlevel, msg='Processed file not found, calling matlab to process file.')
    pwd = _os.getcwd()
    matlab = get_matlab()
    curdir = _os.path.dirname(_os.path.realpath(__file__))
    command = '{matlab} -r "addpath(\'{curdir}\');convert_mat_file(\'{filename}\',\'{outfile}\');exit;"'.format(matlab=matlab, curdir=curdir, pwd=pwd, filename=filename, outfile=temppath)
    
    logger.log(level=loggerlevel, msg='Command given is: {}'.format(command))
    subprocess.call(shlex.split(command))

    # ======================================
    # Load file processed by matlab
    # ======================================
    logger.log(level=loggerlevel, msg='Loading processed file')
    f = _h5.File(temppath, 'r', driver='core', backing_store=False)

    output = Data(read_file = f, filename=filename)

    return output


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
