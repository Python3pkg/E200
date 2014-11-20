function data=convert_mat_file(filename)
	display(['Loading filename: ' filename ])
	data=E200_load_data(filename);
	data=E200_save_local(data,'temp');
	% save('forpython.mat','data','-v7.3');
end
