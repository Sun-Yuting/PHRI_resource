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
            val_series = []
            # line string into vals float
            for line in f:
                vals = line[1:-2].split(',')  # remove '[' and ']/n'
                vals_oneline = []
                # string to float, round
                for val in vals:
                    val = round(float(val))
                    vals_oneline.append(val)
                # append a line
                val_series.append(vals_oneline)
            print(val_series)
            # python list to numpy array
            val_series = np.asarray(val_series)
            print(val_series.shape)


# ENTRY
if __name__ == '__main__':
    main()