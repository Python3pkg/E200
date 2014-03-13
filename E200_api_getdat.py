import numpy as _np
import pdb as _pdb

def E200_api_getdat(dataset,h5file,uids=None):
	vals=_np.array([h5file[val[0]][0,0] for val in dataset['dat']])
	if uids==None:
		return vals
	else:
		valbool=_np.in1d(dataset['UID'][:,0],uids)
		return vals[valbool]
	# _pdb.set_trace()
