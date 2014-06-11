import h5py as _h5
import numpy as _np
import pdb
import matplotlib.pyplot as _plt
# import mytools as _mt
from E200_api_getdat import E200_api_getdat
import scipy.io as _spio
from get_remoteprefix import get_remoteprefix
import os

def E200_load_images(imgstr,h5file,uids=None):
	try:
		remote_bool = h5file['data']['VersionInfo']['remotefiles']['dat'][0,0]
	except:
		remote_bool = True
	if remote_bool:
		prefix = get_remoteprefix()
	else:
		prefix = ''
	print 'Prefix is: [{}]'.format(prefix)

	imgdat = E200_api_getdat(imgstr,h5file,uids=uids)
	# for val in imgdat:
	#         print os.path.join(prefix,val[1:])
	imgs = [_plt.imread(os.path.join(prefix,val[1:])) for val in imgdat]
	imgs = _np.float64(imgs)

	imgbgdat = E200_api_getdat(imgstr,h5file,fieldname='background_dat',uids=uids)
	# print imgbgdat
	for i,val in enumerate(imgbgdat):
		# print val
		val = os.path.join(prefix,val[1:])
		mat = _spio.loadmat(val)
		imgbg = mat['img']
		
		if imgs[i,:,:].shape[0] == imgbg.shape[1]:
			imgbg = _np.transpose(imgbg)

		imgs[i,:,:] = _np.fliplr(_np.abs(imgs[i,:,:]-_np.float64(imgbg)))
	
	return _np.array(imgs)
