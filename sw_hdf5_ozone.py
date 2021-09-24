import h5py

def save_list_to_dat(data_list, out_filepath, header=None):
    '''
    Save data in format [[],[]] into DAT file 
    - CSV 
    - with \t delimeter 
    - \n line endings
    '''
    write_list = []

    for data in data_list:
        output_str = ""
        for val in data:
            output_str += str(val) + "\t"
        output_str = output_str[:-1]
        output_str += "\n"
        write_list.append(output_str)

    with open(out_filepath,"w") as f:
        f.writelines(write_list)

def process_file(filepath):
    f = h5py.File(filepath, 'r')
    list(f.keys())

def main():
    print("Script is started")

    filepath = ".\\input\\o3col2020080212.hdf"
    
    process_file(filepath)

    print("Script is ended")

if __name__ == "__main__":
    main()