import numpy as _np
import h5py as _h5

__all__ = ['Data','Drill','E200_Dat','E200_Image']

class Data(object):
    def __init__(self,read_file,write_file):
        self.read_file=read_file
        self.write_file=write_file
        self.rdrill=Drill(read_file)
        self.wdrill=Drill(write_file)

        # self.data=datalevel()
        # recursivePopulate(self._data,self)

    def close(self):
        self.read_file.close()
        self.write_file.close()

class Drill(object):
    def __init__(self,data):
        self._hdf5 = data
        #  self._mydir = []
        for key in data.keys():
            if key[0]!='#':
                #  self._mydir.append(key)
                out = data[key]
                if type(out) == _h5._hl.group.Group:
                    setattr(self,key,Drill(data[key]))
                elif len(out.shape) == 2:
                    if out.shape[0] == 1 or out.shape[1] == 1:
                        out=out.value.flatten()
                    setattr(self,key,out)
                #  elif type(out) == _h5._hl.dataset.Dataset:
                #          if 
                #          if out[0][0]==_h5.h5r.Reference:
                #                  vals=[out.file[val[0]] for val in out]
                #          else:
                #                  vals = [val for val in out]
                #          if vals[0].shape[0]>1:
                #                  vals = [np.array(val).flatten() for val in vals]
                #                  vals = [''.join(vec.view('S2')) for vec in vals]
                #                  vals = np.array(vals)
                #          else:
                #                  vals = [val[0] for val in vals]
                #                  vals = np.array(vals)
                #          setattr(self,key,vals)
                else:
                    setattr(self,key,data[key])

    def __repr__(self):
        out = '\<E200.E200_load_data.Drill with keys:\n_hdf5'
        for val in self._hdf5.keys():
            out = out + '\n' + val

        out = out[1:] + '\n>'
        return out

class E200_Dat(object):
    def __init__(self,dat,uid,field):
        self._dat = _np.array([dat]).flatten()
        self._uid = _np.int64([uid]).flatten()
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
