class E200_Dat(object):
	def __init__(self,dat,uid,field):
		self._dat = dat
		self._uid = uid
		self._field = field

	def _get_dat(self):
		return self._dat
	dat=property(_get_dat)

	def _get_uid(self):
		return self._uid
	uid=property(_get_uid)
	UID=property(_get_uid)

	def _get_field(self):
		return self._field
	field=property(_get_field)

class E200_Image(E200_Dat):
	def __init__(self,images,dat,uid,image_backgrounds=None):
		E200_Dat.__init__(self,dat,uid,field='dat')
		self._images = images
		self._image_backgrounds = image_backgrounds

	def _get_images(self):
		return self._images
	images=property(_get_images)

	def _get_image_backgrounds(self):
		return self._image_backgrounds
	image_backgrounds=property(_get_image_backgrounds)
