import h5py as _h5
import numpy as _np
import pdb
import matplotlib.pyplot as _plt
import mytools as _mt
import scipy.io as _spio

def E200_load_images(imgstr,h5file,uids=None):
	imgdat = _mt.E200.E200_api_getdat(imgstr,h5file)
	imgs = [_plt.imread(val) for val in imgdat]
	imgs = _np.float64(imgs)

	imgbgdat = _mt.E200.E200_api_getdat(imgstr,h5file,fieldname='background_dat')
	# print imgbgdat
	for i,val in enumerate(imgbgdat):
		# print val
		mat = _spio.loadmat(val)
		imgbg = mat['img']

		if imgs[i,:,:].shape[0] == imgbg.shape[1]:
			imgbg = _np.transpose(imgbg)

		imgs[i,:,:] = _np.abs(imgs[i,:,:]-_np.float64(imgbg))
	
	return _np.array(imgs)
