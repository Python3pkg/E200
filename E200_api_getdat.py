import numpy as _np
import pdb as _pdb
from classes import *
import pdb

def E200_api_getdat(dataset,uids=None,fieldname='dat'):
	version_bool = 'origin' in dataset.file.attrs.keys()
	if version_bool:
		python_version_bool = (dataset.file.attrs['origin']=='python-h5py')
	else:
		python_version_bool = False

	if python_version_bool:
		vals = dataset[fieldname][()]
	else:
		vals=[dataset.file[val[0]] for val in dataset[fieldname]]

		if vals[0].shape[0]>1:
			vals = [_np.array(val).flatten() for val in vals]
			vals = [''.join(vec.view('S2')) for vec in vals]
			vals = _np.array(vals)

	avail_uids = dataset['UID'][()]

	if uids==None:
		out_uids = avail_uids
	else:
		valbool=_np.in1d(avail_uids,uids)
		vals = vals[valbool]

		out_uids = avail_uids[valbool]
	return E200_Dat(vals,out_uids,field=fieldname)
