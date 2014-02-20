import numpy as _np
import pdb as _pdb

def E200_api_getdat(dataset,uids,h5file):
	valbool=_np.in1d(dataset['UID'][:,0],uids)
	vals=_np.array([h5file[val[0]][0,0] for val in dataset['dat']])
	return vals[valbool]
	# _pdb.set_trace()
