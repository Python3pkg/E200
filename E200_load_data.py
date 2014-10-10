import numpy as np
import h5py as _h5
import subprocess
import shlex
import os
import re
from get_valid_filename import *
from warnings import warn
import mytools.qt as mtqt
from PyQt4 import QtGui,QtCore

__all__ = ['Data','E200_load_data']

class Data(object):
	def __init__(self,read_file,write_file):
		self.read_file=read_file
		self.write_file=write_file

		# self.data=datalevel()
		# recursivePopulate(self._data,self)

	def close(self):
		self.read_file.close()
		self.write_file.close()

def E200_load_data(filename,experiment='E200',writefile=None,verbose=False):
	if verbose: print 'Input is: filename={} experiment={}'.format(filename,experiment)
	vfn = Filename(path=filename,experiment=experiment)
	processed_path = vfn.processed_path

	if verbose: print 'Processed file path is: processed_file_path={}'.format(processed_path)

	if os.path.isfile(processed_path):
		if verbose: print 'Found processed file'
	else:
		if verbose: print 'Processed file not found, calling matlab to process file.'
		pwd = os.getcwdu()
		matlab = '/Applications/MATLAB_R2014a.app/bin/matlab -nojvm -nodisplay -nosplash'
		command = '{} -r "addpath(\'~/SDDSTOOLS/mytools/E200/\'); cd(\'{}\'); convert_mat_file(\'{}\'); exit;"'.format(matlab,pwd,filename)
	
		subprocess.call(shlex.split(command))

	if os.path.isfile(processed_path):
		if verbose: print 'Loading processed file'
		f = _h5.File(processed_path,'r',driver='core',backing_store=False)
	else:
		raise IOError('Final error: Could not find processed file')

	if writefile==None:
		writefile = vfn.py_processed_path
	if verbose: print 'Creating file for writing: {}'.format(writefile)
	if os.path.exists(writefile):
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
			warn('Reading file: {}'.format(writefile),UserWarning,stacklevel=2)
			wf = _h5.File(writefile,'r+')
		else:
			raise LookupError('Didn''t detect button')
	else:
		wf = _h5.File(writefile,'w')
		_load_data(wf)

	wf.attrs['origin']  = 'python-h5py'
	wf.attrs['version'] = _h5.version.version

	return Data(read_file = f,write_file = wf)

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


