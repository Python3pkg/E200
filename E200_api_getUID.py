import numpy as np
# from convertH5ref import convertH5ref as _convertH5ref
from mytools.convertH5ref import convertH5ref as _convertH5ref

def E200_api_getUID(struct,val,f):
	uids = struct['UID']
	vals = struct['dat']

	uids = uids[:,0]
	try:
		vals = _convertH5ref(vals,f)
	except:
		vals = np.array(vals).flatten()

	return uids[vals==val]
