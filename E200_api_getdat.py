import numpy as _np
import pdb as _pdb
from classes import *
import pdb

def E200_api_getdat(dataset,uids=None,fieldname='dat',verbose=False):
	# ======================================
	# Check version
	# ======================================
	version_bool = 'origin' in dataset.file.attrs.keys()
	if version_bool:
		python_version_bool = (dataset.file.attrs['origin']=='python-h5py')
	else:
		python_version_bool = False

	# ======================================
	# Get available UIDs in dataset
	# ======================================
	avail_uids = dataset['UID'].value

	if python_version_bool:
		if fieldname == 'dat':
			# ======================================
			# Build data from HDF5 refs
			# ======================================
			dat_refs = dataset['dat'].value
			vals = _np.empty((avail_uids.shape[0],),dtype=_np.object)

			for i,val in enumerate(dat_refs):
				vals[i] = dataset.file[val].value

		else:
			vals = dataset[fieldname].value

	else:
		vals=[dataset.file[val[0]] for val in dataset[fieldname]]

		if vals[0].shape[0]>1:
			vals = [_np.array(val).flatten() for val in vals]
			vals = [''.join(vec.view('S2')) for vec in vals]
			vals = _np.array(vals)

	if _np.size(avail_uids)==1:
		# ======================================
		# Match UIDs
		# ======================================
		if avail_uids==uids:
			out_uids=_np.array([avail_uids])
			out_vals=_np.array([vals])
		else:
			out_uids=_np.array([])
			out_vals=_np.array([])
	elif uids==None:
		# ======================================
		# Return all results if no UID requested
		# ======================================
		out_uids = avail_uids
		out_vals = vals
	else:
		# ======================================
		# Match UIDs
		# ======================================
		valbool  = _np.in1d(avail_uids,uids)
		out_vals = vals[valbool]

		out_uids = avail_uids[valbool]

	return E200_Dat(out_vals,out_uids,field=fieldname)
