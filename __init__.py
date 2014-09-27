import setQS
from E200_load_data import E200_load_data
from E200_api_getUID import E200_api_getUID
from E200_load_images import E200_load_images
from E200_api_getdat import E200_api_getdat
from eaxis import *
# from eaxis import eaxis
# from eaxis import eaxis_ELANEX
# from eaxis import yaxis_ELANEX
# from eaxis import yanalytic
# from eaxis import E_no_eta
# from eaxis import y_no_eta

# from get_remoteprefix import get_remoteprefix
from get_remoteprefix import *
from get_valid_filename import *

import h5py as _h5

class Data(object):
	def __init__(self,filename,experiment='E200'):
		self._filename=filename
		self._f=E200_load_data(filename,experiment)
	
		self.data=self._f['data']
		# self.data=datalevel()
		# recursivePopulate(self._data,self)

class datalevel(object):
	pass

def recursivePopulate(h5data,objData):
	for i,val in enumerate(h5data):
		if type(h5data[val])==_h5._hl.group.Group:
			setattr(objData,val,datalevel())
			recursivePopulate(h5data[val],getattr(objData,val))
		else:
			setattr(objData,val,h5data[val])


