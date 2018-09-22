# IMPORTS
import glob
import json


# VARIABLES
orig_folder = 'exp_res\\raw_motiondata\\free_talk_couples'
dest_folder = 'exp_res\\processed_motiondata\\free_talk_couples'
# (joint number, joint param): head yaw, head pitch, body yaw, body pitch
target_param = [(3,5), (3,4), (20,5), (20,4)]


# FUNCTIONS
def get_values(people_data, raw_values):
    if 'head dir' in people_data:
        raw_values.append(float(people_data["head dir"].split(',')[2]))
        raw_values.append(float(people_data["head dir"].split(',')[1]))
    else:
        raw_values.append(0)
        raw_values.append(0)
    if '20' in people_data:
        raw_values.append(people_data["20"][5])
        raw_values.append(people_data["20"][4])
    else:
        raw_values.append(0)
        raw_values.append(0)
    raw_values.append(0)  # VAD

    return raw_values

def main():
    files = glob.glob(orig_folder + '\\*.*')
    for file in files:
        file_name = file.split('\\')[-1]
        print(file_name)

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
            del json_frame

        # parse each frame
        frames = []
        for json_frame in json_frames:
            frame_str = '\n'.join(json_frame)
            frames.append(json.loads(frame_str))

        del frames[0] # del first frame, only meta-info

        # get values
        raw_series = []
        id_list = []
        for frame in frames:
            body_count = 0
            if 'people' in frame:
                body_count = len(frame['people'])
            else:
                continue
            
            raw_values = []
            if body_count == 0:
                raw_values = [0] * ((len(target_param) + 1) * 2)
            elif body_count == 1:
                raw_values = get_values(frame['people'][0], raw_values)
            elif body_count == 2:
                raw_values = get_values(frame['people'][0], raw_values)
                raw_values = get_values(frame['people'][1], raw_values)
                if frame['people'][0]["3"][1] < frame['people'][1]["3"][1]:
                    # change
                    raw_values = raw_values[int(len(raw_values)/2):] \
                     + raw_values[:int(len(raw_values)/2)]
                else:
                    # no change
                    pass
            raw_series.append(raw_values)

        # save
        with open(dest_folder + '\\' + file_name, 'w') as f:
            for values in raw_series:
                f.write(str(values) + "\n")
                    
        # debug
        print(len(frames))


# ENTRY
if __name__ == '__main__':
    main()