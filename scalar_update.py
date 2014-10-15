import numpy as _np

def scalar_update(group,UID,value,verbose):
	uids = group['UID'].value
	dat  = group['dat'].value
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
		if type(value) == dat.dtype:
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
			new_dat  = _np.append(dat,value)

			group.create_dataset('UID',data=new_uids)
			group.create_dataset('dat',data=new_dat)

		elif uid_match_total == 1:
			# ======================================
			# 1 match, replace value
			# ======================================
			if verbose:
				print '\tOne match, replacing.'
				print '\tOld value: {}, New value: {}'.format(dat[uid_match],value)
			ind = _np.where(uid_match)[0][0]
			group['dat'][ind] = value
			
		elif uid_match_total > 1:
			# ======================================
			# Too many matches, corruption?
			# ======================================
			raise LookupError('Multiple unique IDs exist. ({} uids with values: {})'.format(uid_match_total,uids[uid_match]))

	return group
