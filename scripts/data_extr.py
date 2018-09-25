# IMPORTS
import glob
import json
import operator as op
import pickle
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt


# VARIABLES
orig_folder = 'exp_res\\raw_motiondata\\free_talk_couples'
dest_folder = 'exp_res\\processed_motiondata\\free_talk_couples'
pickle_folder = 'exp_res\\raw_motiondata\\pickles'
# (joint number, joint param): head yaw, head pitch, body yaw, body pitch
target_param = [('head dir', 0), ('head dir', 1), (3,5), (3,4), (20,5), (20,4)]
param_len = op.mul(2, op.add(len(target_param), 1))
np.set_printoptions(linewidth=400)  # no newline within a record


# FUNCTIONS
def cal_gender(average, entry):
    gender = 0
    for n, val in enumerate(entry):
        if abs(val - average[n]) < abs(val - average[n + int(param_len/2)]):
            gender -= 1
        else:
            gender += 1
    if gender <= 0:
        return 0
    else:
        return 1

def get_values(people_data, raw_values):
    for param in target_param:
        joint = str(param[0])
        dimen = int(param[1])
        if joint in people_data:
            # head dir
            if joint == 'head dir':
                val = float(people_data[joint].split(',')[dimen])
            # joint
            else:
                val = float(people_data[joint][dimen])
            raw_values.append(val)
        else:
            raw_values.append(0)
    raw_values.append(0)  # TODO VAD data
    return raw_values

# file -> f -> json_frames -> frames -> raw_series
# name:str -> object:object -> lines:str[] -> object:json[] -> values:float[]
def main():
    files = glob.glob(orig_folder + '\\*.*')
    for file in files:
        file_name = file.split('\\')[-1]
        print('Processing: ' + file_name)

        # read each frame
        json_frames = []
        with open(file, 'r') as f:
            bracket_stack = 0
            json_frame = []
            for line in f:
                line = line.rstrip()
                if len(line) == 0:
                    continue
                # push
                if line[-1] == '{':
                    bracket_stack += 1
                # pop when }
                elif line[-1] == '}':
                    bracket_stack -= 1
                # pop when },
                elif len(line) >= 2 and line[-2] == '}':
                    bracket_stack -= 1
                json_frame.append(line)
                if bracket_stack == 0:
                    json_frames.append(json_frame)
                    json_frame = []
            del json_frame  # delete this frame, prep for next

        # parse each frame
        frames = []
        for json_frame in json_frames:
            frame_str = '\n'.join(json_frame)
            frames.append(json.loads(frame_str))

        # timestamp frame
        starttime = ''
        if 'start time' not in frames[0]:
            raise ValueError()
        starttime = float(frames[0]['start time'])
        starttime = datetime.fromtimestamp(starttime)
        del frames[0]  # frames[0] => time info

        # get values
        raw_series = []
        for frame in frames:
            body_count = 0
            if 'people' in frame:
                body_count = len(frame['people'])
            else:
                continue
            
            raw_values = []
            if body_count == 0:
                raw_values = [0] * param_len
            elif body_count == 1:
                raw_values = get_values(frame['people'][0], raw_values)
            elif body_count == 2:
                raw_values = get_values(frame['people'][0], raw_values)
                raw_values = get_values(frame['people'][1], raw_values)
                # TODO gender dicision
                if frame['people'][0]["3"][1] < frame['people'][1]["3"][1]:
                    # change
                    raw_values = raw_values[int(len(raw_values)/2):] \
                     + raw_values[:int(len(raw_values)/2)]
                else:
                    # no change
                    pass
            raw_series.append(raw_values)

        # check integrity
        average_vals = [0] * param_len
        for n in range(len(raw_series)):
            if len(raw_series[n]) == param_len:
                average_vals = list(map(op.add, average_vals, raw_series[n]))
        average_vals = [i/len(raw_series) for i in average_vals]
        for n in range(len(raw_series)):
            if len(raw_series[n]) == len(target_param) + 1:
                gender = cal_gender(average_vals, raw_series[n])
                if gender == 0:
                    raw_series[n] = raw_series[n] + [0] * (int(param_len/2))
                else:
                    raw_series[n] = [0] * (int(param_len/2)) + raw_series[n]
            elif len(raw_series[n]) == param_len:
                pass
            else:
                print(raw_series[n])
                raise ValueError('check length')
        
        # list to numpy array
        raw_series = np.array(raw_series, dtype=float)

        # statistics info
        header_top = f'--{file_name}-----'
        header_time = f'start_time:\t{starttime.isoformat()}'
        header_frames = f'n_frames:\t{len(raw_series)}'
        header_freq = f'frequency:\t30 frame / sec'
        header_span = f'time_span:\t{len(raw_series)/30}'
        avrg_array = []
        loss_array = []
        tran_series = raw_series.T
        for records in tran_series:
            nonzero_rec = []
            for record in records:
                if record:
                    nonzero_rec.append(record)
            if len(nonzero_rec) == 0:
                avrg_array.append(0)
            else:
                avrg_array.append(sum(nonzero_rec)/len(nonzero_rec))
            loss_array.append(len(nonzero_rec)/len(records))
        header_avrg = f'average:\t{avrg_array}'
        header_loss = f'loss_rate:\t{loss_array}'
        header_end = '-' * 20
        header = '\n'.join([header_top, header_time, header_frames, header_freq, header_span, header_avrg, header_loss, header_end])
        print(header)

        # save
        with open(dest_folder + '\\' + file_name, 'w') as f:
            # print meta-info
            f.write(header + '\n')
            for values in raw_series:
                f.write(str(values) + '\n')
                    

# ENTRY
if __name__ == '__main__':
    main()
