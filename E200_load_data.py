from classes import *
import numpy as np
import h5py as _h5
import subprocess
import shlex
import os
import re
from E200_dataset2str import *
from get_valid_filename import *
from warnings import warn
import mytools.qt as mtqt
from PyQt4 import QtGui,QtCore
import logging
loggerlevel = logging.DEBUG
logger=logging.getLogger(__name__)

import pdb

__all__ = ['Data','E200_load_data']


def E200_load_data(filename,experiment='E200',writefile=None,verbose=False,readonly=False,local=False):
    logger.log(level=loggerlevel,msg='Input is: filename={} experiment={}'.format(filename,experiment))

    # ======================================
    # Get a verified filename
    # ======================================
    if local:
        vfn = Filename(path='temp.mat',experiment=experiment,local=local)
    else:
        vfn = Filename(path=filename,experiment=experiment,local=local)
    processed_path = vfn.processed_path

    logger.log(level=loggerlevel,msg='Processed file path is: processed_file_path={}'.format(processed_path))

    if os.path.isfile(processed_path):
        logger.log(level=loggerlevel,msg='Found processed file')
    else:
        logger.log(level=loggerlevel,msg='Processed file not found, calling matlab to process file.')
        pwd = os.getcwdu()
        matlab = '/Applications/MATLAB_R2014b.app/bin/matlab -nodisplay -nosplash'
        #  matlab = 'fmatlab -nodisplay -nosplash'
        command = '{matlab} -r "addpath(fullfile(getenv(\'HOME\'),\'testbed/E200_DRT/E200_data/\'),\'~/python-dev-modules/E200/\');cd(\'{pwd}\');convert_mat_file(\'{filename}\');exit;"'.format(matlab=matlab,pwd=pwd,filename=filename)
    
        logger.log(level=loggerlevel,msg='Command given is: {}'.format(command))
        subprocess.call(shlex.split(command))

    if os.path.isfile(processed_path):
        logger.log(level=loggerlevel,msg='Loading processed file')
        f = _h5.File(processed_path,'r',driver='core',backing_store=False)
    else:
        raise IOError('Final error: Could not find processed file')

    if writefile==None:
        writefile = vfn.py_processed_path
        #  logger.log(level=loggerlevel,msg='Creating file for writing: {}'.format(writefile))

    if os.path.exists(writefile):
        if readonly:
            logger.log(level=loggerlevel,msg='Reading file: {}'.format(writefile))
            wf = _h5.File(writefile,'r+')
        else:
            title = 'File already exists'
            maintext = 'WARNING: File already exists!'
            infotext = 'Overwrite file: {}?'.format(writefile)
            buttons = np.array([
                mtqt.Button('Overwrite',QtGui.QMessageBox.AcceptRole),
                mtqt.Button(QtGui.QMessageBox.Abort,escape=True),
                mtqt.Button('Load file',default=True)
                ])
            buttonbox = mtqt.ButtonMsg(title=title,maintext=maintext,infotext=infotext,buttons=buttons)
            clicked = buttonbox.clickedArray

            if clicked[0]:
                warn('Overwriting file: {}'.format(writefile),UserWarning,stacklevel=2)
                wf = _h5.File(writefile,'w')
                _load_data(wf)
            elif clicked[1]:
                raise IOError('No valid directory chosen.')
            elif clicked[2]:
                logger.log(level=loggerlevel,msg='Reading file: {}'.format(writefile))
                wf = _h5.File(writefile,'r+')
            else:
                raise LookupError('Didn''t detect button')
    else:
        logger.log(level=loggerlevel,msg='Opening file for writing: {}'.format(writefile))
        wf = _h5.File(writefile,'w')
        _load_data(wf)

    wf.attrs['origin']  = 'python-h5py'
    wf.attrs['version'] = _h5.version.version

    output = Data(read_file = f,write_file = wf)

    loadreq = E200_dataset2str(output.rdrill.data.VersionInfo.loadrequest)
    logger.log(level=loggerlevel,msg='Load request: {}'.format(loadreq))
    actualvfn = Filename(path=filename,experiment=experiment,local=False)

    if loadreq == actualvfn.valid_path:
        logger.log(level=loggerlevel,msg='Request matches loaded file, continuing...')
        return output
    else:
        logger.log(level=loggerlevel,msg='Request doesn''t match loaded file, removing processed file and retrying...')
        try:
            os.remove(vfn.processed_path)
        except OSError:
            pass

        try:
            os.remove(vfn.py_processed_path)
        except OSError:
            pass
        pdb.set_trace()
        return E200_load_data(
            filename   = filename,
            experiment = experiment,
            writefile  = writefile,
            verbose    = verbose,
            readonly   = readonly,
            local      = local
            )

def _load_data(wf):
    processed=wf.create_group('/data/processed')
    groups = ['arrays','scalars','images','vectors']
    for val in groups:
        processed.create_group(val)

    wf.flush()

class datalevel(object):
    pass

def recursivePopulate(h5data,objData):
    for i,val in enumerate(h5data):
        if type(h5data[val])==_h5._hl.group.Group:
            setattr(objData,val,datalevel())
            recursivePopulate(h5data[val],getattr(objData,val))
        else:
            setattr(objData,val,h5data[val])

