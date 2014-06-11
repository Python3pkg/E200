function convert_mat_file(filename)
	load(filename);

	save('forpython.mat','data','-v7.3');
end
