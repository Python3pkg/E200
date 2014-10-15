import numpy as _np
import h5py as h5

def vector_update(group,UID,value,verbose):
	uids = group['UID'].value
	dat  = group['dat'].value
	if verbose: print '\tAdding UID: {}, value: {}'.format(UID,value)
	# ======================================
	# Validate it's a numpy vector
	# with a good data type
	# Turns out variable length HDF5 arrays
	# work for everything except np.float64
	# ======================================
	value = _np.array(value)
	# Verify vector
	ndim = _np.ndim(value)
	if ndim != 1:
		raise ValueError('Too many dimensions for a vector: {} dimensions'.format(ndim))

	# Verify data type
	valtype = value.dtype
	if valtype == _np.float64 or valtype == _np.dtype(object):
		raise ValueError('Not a valid type for HDF5 variable-length dataset: "{}" type'.format(valtype))

	if _np.size(uids) == 0:
		# ======================================
		# If first entry
		# ======================================
		if verbose: print '\tNo UIDs present yet, adding UID: {}, value: {}'.format(UID,value)

		del group['UID']
		del group['dat']

		group.create_dataset('UID',data=UID)
		group.create_dataset('dat',data=value)

	elif _np.size(uids) > 0:
		# ======================================
		# If entries already present
		# ======================================
		if verbose:
			print '\tUIDs present'
			print '\t\tUIDs:\t{}'.format(uids)
			print '\t\tDat:\t{}'.format(dat)

		# ======================================
		# Check if types match
		# ======================================
		if valtype == dat[0].dtype:
			if verbose: print '\tInput type matches existing type'
		else:
			raise TypeError('Input value type "{}" doesn''t match existing type "{}"'.format(type(value),dat.dtype))

		# ======================================
		# Find matches
		# ======================================
		uid_match = _np.in1d(uids,UID)
		uid_match_total = _np.sum(uid_match)

		if uid_match_total == 0:
			# ======================================
			# No matches, add UID and value
			# ======================================
			if verbose: 'No matches, adding'
			del group['UID']
			del group['dat']

			new_uids = _np.append(uids,UID)
			new_dat = _np.empty(_np.shape(new_uids),dtype=object)
			if _np.size(uids) == 1:
				new_dat[0] = dat
			else:
				new_dat[0:-1] = dat
			new_dat[-1] = value
			
			# print 'testing'
			# print dat
			# print value
			# print new_dat

			group.create_dataset('UID',data=new_uids)

			dt = h5.special_dtype(vlen=valtype)
			dset = group.create_dataset('dat',_np.shape(new_uids),dtype=dt)
			for i,val in enumerate(new_dat):
				dset[i] = val

		elif uid_match_total == 1:
			# ======================================
			# 1 match, replace value
			# ======================================
			if verbose:
				print '\tOne match, replacing.'
				print '\tOld value: {}, New value: {}'.format(dat[uid_match][0],value)
			ind = _np.where(uid_match)[0][0]
			group['dat'][ind] = value
			
		elif uid_match_total > 1:
			# ======================================
			# Too many matches, corruption?
			# ======================================
			raise LookupError('Multiple unique IDs exist. ({} uids with values: {})'.format(uid_match_total,uids[uid_match]))

	return group
