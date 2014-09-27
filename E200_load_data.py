import h5py as _h5
import subprocess
import shlex
import os
import re
from get_valid_filename import *

def E200_load_data(filename,experiment,verbose=False):
	if verbose: print 'Input is: filename={} experiment={}'.format(filename,experiment)
	vfn = Filename(path=filename,experiment=experiment)
	processed_path = vfn.processed_path

	if verbose: print 'Processed file path is: processed_file_path={}'.format(processed_path)

	if os.path.isfile(processed_path):
		if verbose: print 'Found processed file, loading'
		f = _h5.File(processed_path,'r',driver='core',backing_store=False)
	else:
		if verbose: print 'Processed file not found, calling matlab to process file.'
		pwd = os.getcwdu()
		matlab = '/Applications/MATLAB_R2014a.app/bin/matlab -nojvm -nodisplay -nosplash'
		command = '{} -r "addpath(\'~/SDDSTOOLS/mytools/E200/\'); cd(\'{}\'); convert_mat_file(\'{}\'); exit;"'.format(matlab,pwd,filename)
	
		subprocess.call(shlex.split(command))
		
		f=_h5.File('forpython.mat','r',driver='core',backing_store=False)

	return f
