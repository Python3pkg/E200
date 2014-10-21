import numpy as _np
import pdb as _pdb
from classes import *
import pdb
import h5py as h5

def E200_api_getdat(dataset,UID=None,fieldname='dat',verbose=False):
	# ======================================
	# Check version
	# ======================================
	version_bool = 'origin' in dataset.file.attrs.keys()
	if version_bool:
		python_version_bool = (dataset.file.attrs['origin']=='python-h5py')
	else:
		python_version_bool = False
	if verbose: print 'Matlab version: {}'.format(not python_version_bool)

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
		# ======================================
		# Deref if necessary
		# ======================================
		if type(dataset[fieldname][0][0]) == h5.h5r.Reference:
			vals=[dataset.file[val[0]] for val in dataset[fieldname]]
		else:
			vals = [val for val in dataset[fieldname]]

		if vals[0].shape[0]>1:
			vals = [_np.array(val).flatten() for val in vals]
			vals = [''.join(vec.view('S2')) for vec in vals]
			vals = _np.array(vals)
		else:
			vals = [val[0] for val in vals]
			vals = _np.array(vals)

	if _np.size(avail_uids)==1:
		# ======================================
		# Match UIDs
		# ======================================
		if avail_uids==UID:
			out_uids=_np.array([avail_uids])
			out_vals=_np.array([vals])
		else:
			out_uids=_np.array([])
			out_vals=_np.array([])
	elif (UID is None):
		# ======================================
		# Return all results if no UID requested
		# ======================================
		out_uids = avail_uids
		out_vals = vals
	else:
		# ======================================
		# Match UIDs
		# ======================================
		valbool  = _np.in1d(avail_uids,UID)
		out_vals = vals[valbool]

		out_uids = avail_uids[valbool]

	if verbose:
		total = _np.size(out_uids)
		print 'Number of UIDs found: {}'.format(total)

	return E200_Dat(out_vals,out_uids,field=fieldname)
