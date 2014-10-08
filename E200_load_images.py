import h5py as _h5
import numpy as _np
import pdb
import matplotlib.pyplot as _plt
# import mytools as _mt
from E200_api_getdat import E200_api_getdat
import scipy.io as _spio
from get_remoteprefix import get_remoteprefix
import os
from classes import *

def E200_load_images(imgstr,uids=None):
	try:
		remote_bool = imgstr.file['data']['VersionInfo']['remotefiles']['dat'][0,0]
	except:
		remote_bool = True
	if remote_bool:
		prefix = get_remoteprefix()
	else:
		prefix = ''
	print 'Prefix is: [{}]'.format(prefix)

	imgdat = E200_api_getdat(imgstr,uids=uids)
	# for val in imgdat:
	#         print os.path.join(prefix,val[1:])
	imgs = [_plt.imread(os.path.join(prefix,val[0:])) for val in imgdat.dat]
	imgs = _np.float64(imgs)

	imgbgdat = E200_api_getdat(imgstr,fieldname='background_dat',uids=imgdat.uid)
	# print imgbgdat
	for i,val in enumerate(imgbgdat.dat):
		# print val
		val = os.path.join(prefix,val[0:])
		mat = _spio.loadmat(val)
		imgbg = mat['img']
		
		if imgs[i,:,:].shape[0] == imgbg.shape[1]:
			imgbg = _np.transpose(imgbg)

		imgs[i,:,:] = _np.fliplr(_np.abs(imgs[i,:,:]-_np.float64(imgbg)))

	return E200_Image(images=_np.array(imgs),dat=imgdat.dat,uid=imgdat.uid)
