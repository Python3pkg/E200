import numpy as np
import h5py as h5
import warnings
from scalar_update import *
from vector_update import *
from array_update import *

def E200_api_updateUID(group,UID,value,verbose=False):
	datatype = group.attrs['datatype']
	if verbose: print '\tDatatype is {}'.format(datatype)

	# ======================================
	# Validate value, uid same size
	# ======================================
	if datatype == 'scalar':
		if np.size(value) != np.size(UID):
			raise ValueError('UIDs and values not commensurate sizes. UIDs: {}, Values: {}'.format(UID,value))

	elif datatype == 'vector':
		# ======================================
		# Get right length of value
		# ======================================
		if np.ndim(value) == 1:
			if np.size(UID) != 1:
				raise ValueError('UIDs and values not commensurate sizes. UIDs: {}, Values: {}'.format(UID,value))

		elif np.ndim(value) == 2:
			if np.shape(value)[0] != np.size(UID):
				raise ValueError('UIDs and values not commensurate sizes. UIDs: {}, Values: {}'.format(UID,value))
		else:
			raise ValueError('Number of dimensions for array of vectors incorrect: {} dimensions'.format(np.ndim(value)))

	elif datatype == 'array':
			raise NotImplementedError('Arrays not implemented yet')

	else:
		raise TypeError('This is not a group supported by the E200_api')

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
	
		# ======================================
		# Scalar type
		# ======================================
		if datatype == 'scalar':
			group=scalar_update(group,UID,value,verbose)

		elif datatype == 'vector':
			group=vector_update(group,UID,value,verbose)

		elif datatype == 'array':
			raise NotImplementedError('Arrays not implemented yet')

		else:
			raise TypeError('This is not a group supported by the E200_api')

		# ======================================
		# Write changes to file
		# ======================================
		group.file.flush()
