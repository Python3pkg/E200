from ..get_remoteprefix import get_remoteprefix
import os
import re
import scisalt as ss
import shutil


def copydata(src, dst=None):
    """
    .. versionadded:: 1.4

    Copies data from *src* path to *dst* path. If *dst* is not specified, copies to the current prefix.
    """
    if dst is None:
        dst = get_remoteprefix()
    
    src_prefix = re.search('.*(?=nas/nas)', src).group(0)
    
    # =======================
    # Determine path
    # =======================
    dataset_path = re.search('nas.*', src).group(0)
    root, ext = os.path.splitext(dataset_path)
    if ext != '':
        dataset_path = os.path.dirname(dataset_path)
    
    src_path = os.path.dirname(dataset_path)
    
    # =======================
    # Make directories
    # =======================
    path = os.path.join(dst, src_path)
    try:
        os.makedirs(path)
    except:
        pass
    
    # =======================
    # Remove existing data
    # =======================
    exist_path = os.path.join(dst, dataset_path)
    if os.path.lexists(exist_path):
        button = ss.qt.ButtonMsg('Data appears here: delete and replace data?', buttons=['Yes', 'No'])
        if button.clickeditem == 'Yes':
            dataset_dst = os.path.join(dst, dataset_path)
            try:
                shutil.rmtree(dataset_dst)
            except:
                pass
    
            # =======================
            # Copy existing data
            # =======================
            dataset_src = os.path.join(src_prefix, dataset_path)
            shutil.copytree(dataset_src, dataset_dst)
        else:
            raise RuntimeError('User does not want to replace data: old data still used.')
