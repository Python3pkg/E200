import numpy as np

def E200_api_updateUID(group,val,UID,verbose=False):
	if type(UID) == np.ndarray:
		UID = UID[0]
	# If UID exists
	val = np.array([val])
	if 'UID' in group:
		# Get UIDS
		uids=group['UID'][()]
		dat = group['dat'][()]
		if np.ndim(uids)==0:
			# print 'a'
			if UID == uids:
				print 'oh noes'
				dat = val
			else:
				uids = np.append(uids,UID)
				dat = np.append(dat,val,axis=0)
				print dat
				del group['UID']
				group['UID'] = uids
		elif UID in uids:
			# print 'b'
			dat[uids==UID] = val
		else:
			# print 'hello'
			uids = np.append(uids,UID)
			dat = np.append(dat,val,axis=0)
			del group['UID']
			group['UID'] = uids

		del group['dat']
		group['dat']=dat
	# If no UID exists
	else:
		# Add UID
		group['UID'] = [UID]
		group['dat'] = val

	group.file.flush()
	if verbose:
		print 'UID in file is: {}'.format(group['UID'][()])
		print 'Dat in file is:'
		print group['dat'][()]
