import numpy as np
import h5py as h5
import warnings
from scalar_update import *

def E200_api_updateUID(group,UID,value,verbose=False):
	# ======================================
	# Validate value, UID same size
	# ======================================
	if np.size(value) != np.size(UID):
		raise ValueError('Values and UIDs not commensurate sizes')

	if np.size(UID)>1:
		# ======================================
		# Run through list of UID's, processing
		# individually
		# ======================================
		if verbose: print 'Multiple UIDs entered, updating recursively'

		# ======================================
		# Check for duplicate UIDs and sort
		# ======================================
		UID_sorted,inds = np.unique(UID,return_index=True)
		value_sorted    = value[inds]
		if np.size(UID_sorted) != np.size(UID):
			raise ValueError('UIDs aren''t unique: {}'.format(UID))

		for i,uid in enumerate(UID_sorted):
			E200_api_updateUID(group,value=value_sorted[i],UID=uid,verbose=verbose)

	else:
		# ======================================
		# Retrieve data type
		# ======================================
		if verbose: print 'Single UID entered: {}'.format(UID)
		datatype = group.attrs['datatype']

		if verbose: print '\tDatatype is {}'.format(datatype)
	
		# ======================================
		# Scalar type
		# ======================================
		if datatype == 'scalar':
			group=scalar_update(group,UID,value,verbose)

		elif datatype == 'vector':
			pass
		elif datatype == 'array':
			pass
		else:
			raise TypeError('This is not a group supported by the E200_api')

		# ======================================
		# Write changes to file
		# ======================================
		group.file.flush()
