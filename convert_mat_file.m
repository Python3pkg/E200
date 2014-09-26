function data=convert_mat_file(filename)
	data=E200_load_data(filename);
	% save('forpython.mat','data','-v7.3');
end
