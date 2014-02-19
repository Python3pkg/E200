import numpy as np
from convertH5ref import convertH5ref as _convertH5ref

def E200_api_getUID(struct,val,f):
	uids = struct['UID']
	vals = struct['dat']

	uids = uids[:,0]
	vals = _convertH5ref(vals,f)

	return uids[vals==val]
