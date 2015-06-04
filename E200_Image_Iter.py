import numpy as _np
from .E200_load_images import E200_load_images
import ipdb
import logging
logger = logging.getLogger(__name__)


# ======================================
# Image iterator
# ======================================
class E200_Image_Iter(object):
    def __init__(self, imgstr, uids=None, numperset=50):
        # ======================================
        # Initialize requested iterator
        # ======================================
        self._numperset = numperset
        self._imgstr    = imgstr
        self._uids      = uids

    def __iter__(self):
        # ======================================
        # Initialize this loop
        # ======================================
        self._subind = 0
        if self._uids is None:
            self._uids = self._imgstr.UID

        self.load_next_batch()

        return self

    def __next__(self):
        if self._imgs_ind >= self._num_uids_load:
            self.load_next_batch()

        out = self._images.images[self._imgs_ind]
        self._imgs_ind = self._imgs_ind + 1
        return out

    def load_next_batch(self):
            # ======================================
            # Load only up to the next batch avail.
            # uids to prevent memory overflow
            # ======================================
            # ipdb.set_trace()
            num_uids_left = _np.size(self._uids)
            logger.debug('Number of UIDs left: {}'.format(num_uids_left))

            if num_uids_left == 0:
                raise StopIteration

            self._num_uids_load = _np.min([num_uids_left, self._numperset])
            uids = self._uids[0:self._num_uids_load]

            self._images = E200_load_images(self._imgstr, UID=uids)
            self._imgs_ind = 0

            self._uids = _np.delete(self._uids, slice(0, self._num_uids_load))

            return
