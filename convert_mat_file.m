function data=convert_mat_file(filename)
	display(['Loading filename: ' filename ])
	data=E200_load_data(filename);
	% data.raw = rmfield(data.raw,'metadata')
	data.raw.metadata = rmfield(data.raw.metadata,'E200_state')
	keep = {'set_num',
		'step_value',
		'XPS_LI20_DWFA_M1',
		'XPS_LI20_DWFA_M2',
		'XPS_LI20_DWFA_M3',
		'XPS_LI20_DWFA_M4',
		'XPS_LI20_DWFA_M5',
		'LI20_LGPS_3011_BDES',
		'LI20_LGPS_3031_BDES',
		'LI20_LGPS_3091_BDES',
		'LI20_LGPS_3141_BDES',
		'LI20_LGPS_3151_BDES',
		'LI20_LGPS_3261_BDES',
		'LI20_LGPS_3311_BDES',
		'LI20_LGPS_3330_BDES'
		};
	for i = 1:length(keep)
		scalars.(keep{i}) = data.raw.scalars.(keep{i});
	end
	% data.raw = rmfield(data.raw,'scalars')
	data.raw.scalars = scalars
	data=E200_save_local(data,'temp_processed');
	% save('forpython.mat','data','-v7.3');
end
