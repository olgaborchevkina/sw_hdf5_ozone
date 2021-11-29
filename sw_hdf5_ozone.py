from pyhdf.SD import SD, SDC
from pathlib import Path
import re
import glob

SDS_O3_COLUMN = "O3_column"
SDS_03_STD = "O3_std"
DATA_STEP = 0.5
LAT_START = -90.0
LONG_START = -179.5

class GeoFilter:
    
    lat_min = 0
    lat_max = 0
    long_min = 0
    long_max = 0
    
    def __init__(self, lat_min, lat_max, long_min, long_max) -> None:
        self.lat_min = lat_min
        self.lat_max = lat_max
        self.long_min = long_min
        self.long_max = long_max
        
    def is_accepted(self, lat, long) -> bool:
        if lat >= self.lat_min and lat <= self.lat_max and long >= self.long_min and long <= self.long_max:
            return True
        else:
            return False

def lat_idx_to_value(idx):
    return LAT_START + 0.5 * idx

def long_idx_to_value(idx):
    return LONG_START + 0.5 * idx

def log(msg):
    print("[OZONE] " + msg)

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

def process_file(filepath, geo_filter):
    result = list()

    # Extract data from filename
    sample_datetime = Path(filepath).stem[-10:]
    sample_data = sample_datetime[:-2]
    sample_data = sample_data[:4] + "." + '.'.join(re.findall('..', sample_data[4:]))
    sample_time = sample_datetime[-2:] + ":00:00"
    measure_time = sample_data + " " + sample_time

    # Extract HDF data
    hdf_file = SD(filepath, SDC.READ)
    datasets_dic = hdf_file.datasets()
    sds_obj = hdf_file.select(SDS_O3_COLUMN)
    data_arr = sds_obj.get() # get sds data

    for lat_idx in range(len(data_arr)):
        for long_idx in range(len(data_arr[lat_idx])):
            lat = lat_idx_to_value(lat_idx)
            long = long_idx_to_value(long_idx)
            if geo_filter.is_accepted(lat, long):
                measure = [measure_time, lat, long, data_arr[lat_idx][long_idx]]
                result.append(measure)
        
    return result

def main():
    log("Script is started")

    result = list()
    
    files = glob.glob("./input/*.hdf")    
    output_path = ".\\output\output.dat"
    geo_filter = GeoFilter(lat_min=50.0, lat_max=70.0, long_min=20.0, long_max=30.0)

    for filepath in files:
        log("Process >> " + filepath)

        try:
            result += process_file(filepath, geo_filter)
            log(f"Finish processing of <{filepath}>")
    
        except Exception as e:
            log("Cannot process >> ", filepath)
            log("Reason >> " + str(e))
            
        finally:
            pass

    log(f"Results saved to {output_path}")
    save_list_to_dat(result, output_path)

    log("Script is ended")

if __name__ == "__main__":
    main()