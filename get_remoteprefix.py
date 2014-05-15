#!/usr/bin/env python
import os
import sys
import ConfigParser
import inspect
from PyQt4 import QtGui,QtCore


def get_remoteprefix():
	app = QtGui.QApplication.instance()
	if not app:
		app = QtGui.QApplication([sys.argv[0]])

	# =====================================
	# Default prefix
	# =====================================
	def_prefix='/Volumes/PWFA_4big'

	config_path = get_configpath()

	# =====================================
	# Try to read the prefix
	# =====================================
	config=ConfigParser.ConfigParser()
	try:
		config.read(config_path)
		prefix=config.get('Prefs','prefix')
	except:
		prefix = def_prefix

	# =====================================
	# Test the prefix
	# =====================================
	datapath = os.path.join(prefix,'nas','nas-li20-pm00')
	while not os.path.isdir(datapath):
		# Drive may not be mounted: warn user, allow to mount drive or change prefix
		msgbox = QtGui.QMessageBox()
		msgbox.setText('WARNING: Path to data doesn\'t exist!')
		msgbox.setInformativeText('Data not found at {}. Drive may not be mounted.'.format(datapath))
		tryagainbtn = msgbox.addButton('Try again.',msgbox.AcceptRole)
		msgbox.setDefaultButton(tryagainbtn)
		locatebtn = msgbox.addButton('Locate folder containing /nas.',msgbox.AcceptRole)
		abortbtn = msgbox.addButton(msgbox.Abort)
		msgbox.setEscapeButton(abortbtn)
		msgbox.exec_()

		if msgbox.clickedButton() == abortbtn:
			raise IOError('No valid directory chosen.')
		elif msgbox.clickedButton() == locatebtn:
			prefix=get_directory()
			set_remoteprefix(config,prefix)
			datapath = os.path.join(prefix,'nas','nas-li20-pm00')
			# datapath=prefix

	return prefix

def set_remoteprefix(config,prefix):
	try:
		config.add_section('Prefs')
	except:
		pass

	config.set('Prefs','prefix',prefix)
	with open(get_configpath(),'wb') as configfile:
		config.write(configfile)

def get_configpath():
	this_path=inspect.stack()[0][1]
	this_dir = os.path.dirname(this_path)
	config_path = os.path.join(this_dir,'FACET_data.cfg')

	return config_path

def get_directory():
	window = QtGui.QFileDialog.getExistingDirectory(directory='/')
	return str(window)
