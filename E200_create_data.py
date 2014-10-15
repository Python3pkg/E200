__all__ = ['E200_create_data']
def E200_create_data(group_parent,group_name,datatype):
	# ======================================
	# Check if group name already exists
	# ======================================
	if group_name in group_parent.keys():
		raise IndexError('Data with name "{}" already exists.'.format(group_name))

	# ======================================
	# Create different kinds of groups
	# ======================================
	if datatype == 'scalar':
		group_child = _create_group_basic(group_parent,group_name,datatype)
	elif datatype == 'vector':
		group_child = _create_group_basic(group_parent,group_name,datatype)
	elif datatype == 'array':
		group_child = _create_group_basic(group_parent,group_name,datatype)
	else:
		raise TypeError('Datatype "{}" is not supported'.format(datatype))

	return group_child

def _create_group_basic(group_parent,group_name,datatype):
	group_child = group_parent.create_group(group_name)
	group_child.attrs.create('datatype',datatype)
	group_child.create_dataset('UID',shape=(0,))
	group_child.create_dataset('dat',shape=(0,))
	return group_child
