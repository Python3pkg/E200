import numpy as _np
import pdb as _pdb

def E200_api_getdat(dataset,h5file,uids=None,fieldname='dat'):
	# vals=_np.array([h5file[val[0]][0,0] for val in dataset['dat']])
	vals=[h5file[val[0]] for val in dataset[fieldname]]
	if vals[0].shape[0]>1:
		vals = [_np.array(val).flatten() for val in vals]
		# vals = [(u''.join(unichr(c) for c in vec) for vec in vals]
		# print vals
		vals = [''.join(vec.view('S2')) for vec in vals]
		vals = _np.array(vals)

	if uids==None:
		return vals
	else:
		valbool=_np.in1d(dataset['UID'][:,0],uids)
		# return vals
		return vals[valbool]
	# _pdb.set_trace()

