import h5py as _h5
import subprocess
import shlex
import os

def E200_load_data(filename):
	
	pwd = os.getcwdu()
	matlab = '/Applications/MATLAB_R2014a.app/bin/matlab -nojvm -nodisplay -nosplash'
	command = '{} -r "addpath(\'~/SDDSTOOLS/mytools/E200/\'); cd(\'{}\'); convert_mat_file(\'{}\'); exit;"'.format(matlab,pwd,filename)
	# command = '{} -r "cd(\'{}\'); ls"'.format(matlab,pwd)
	# command = '{} -r "cd(\'{}\');"'.format(matlab,pwd)
	# print command
	FNULL=open(os.devnull,'w')
	# subprocess.call(shlex.split(command),stdout=FNULL,stderr=subprocess.STDOUT)
	subprocess.call(shlex.split(command))
	
	# f=_h5.File('forpython.mat')
	f=_h5.File('forpython.mat','r',driver='core',backing_store=False)

	return f
