# IMPORTS
import glob
import numpy as np
import scipy.signal


# VARIABLES
orig_folder = 'exp_res\\processed_motiondata\\free_talk_couples'
dest_folder = 'exp_res\\processed_motiondata\\free_talk_couples_final'


# FUNCTIONS
def main():
    # read file
    files = glob.glob(orig_folder + '\\*.*')
    for file in files:
        file_name = file.split('\\')[-1]
        print(file_name)

        with open(file, 'r') as f:
            test_axis = []
            for line in f:
                # one axis for test
                axis_val = line.split(',')[2].strip()
                test_axis.append(round(float(axis_val), 3))
            
            # 1. interpolation

            # 2. difference
            diff_axis = np.diff(test_axis, 1)
            # print(diff_axis)
            
            # 3. LPF


# ENTRY
if __name__ == '__main__':
    main()