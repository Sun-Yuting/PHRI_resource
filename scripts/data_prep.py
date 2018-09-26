# IMPORTS
import glob
import numpy as np
import re
import operator as op


# VARIABLES
orig_folder = 'exp_res\\processed_motiondata\\free_talk_couples'
dest_folder = 'exp_res\\processed_motiondata\\free_talk_couples_final'
val_pattern = r'(-?\d+\.\d*)'
param_len = 14


# FUNCTIONS
# 10Hz output
def mov_avrg(series, window=10, hop=3):
    new_series = []
    for n in range(0, len(series), hop):
        if n + window >= len(series):
            break
        n_slice = series[n:n+window]
        n_slice = [i for i in n_slice if i]
        new_series.append(n_slice)
    return new_series

def main():
    # read file
    files = glob.glob(orig_folder + '\\*.*')
    for file in files:
        file_name = file.split('\\')[-1]
        print(file_name)

        raw_data = []
        with open(file, 'r') as f:
            for line in f:
                if line[0] != '[':
                    continue
                record = []
                val_iter = re.finditer(val_pattern, line)
                for val in val_iter:
                    record.append(float(val.group()))
                if len(record) != param_len:
                    raise ValueError('wrong joint number')
                else:
                    raw_data.append(record)

        raw_series = np.array(raw_data).T

        # moving average as: interpolater, LPF
        mov_series = []
        for n in range(len(raw_series)):
            mov_series.append(mov_avrg(raw_series[n]))
        mov_series = np.array(mov_series)
        # print(mov_series)

        # difference


        # with open(file, 'r') as f:
        #     val_series = []
        #     # line string into vals float
        #     for line in f:
        #         vals = line[1:-2].split(',')  # remove '[' and ']/n'
        #         vals_oneline = []
        #         # string to float, round
        #         for val in vals:
        #             val = round(float(val))
        #             vals_oneline.append(val)
        #         # append a line
        #         val_series.append(vals_oneline)
        #     print(val_series)
        #     # python list to numpy array
        #     val_series = np.asarray(val_series)
        #     print(val_series.shape)


# ENTRY
if __name__ == '__main__':
    main()