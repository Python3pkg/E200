import h5py as _h5
import numpy as _np
import pdb

def E200_load_images(dat,h5file):
	strlist = [u''.join(unichr(c) for c in h5file[obj_ref]) for obj_ref in dat]
	# return strlist
	# imgfiles= _np.array([val for val  in strlist])
	imgfiles= _np.array([_np.fliplr(_np.rot90(_h5.File(val)['img'],3)) for val  in strlist])
	# pdb.set_trace()
	return imgfiles
