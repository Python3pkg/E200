function data=convert_mat_file(filename,outfile)
    display(['Loading filename: ' filename ])
    data=E200_load_data(filename);
    save(outfile,'data','-v7.3');
end
