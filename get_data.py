import os
import pandas as pd

video_loc = "/Users/ivyhuang/Downloads/OpenFace-master/samples/2015-10-15-15-14.avi"
feature_extraction_exe = "/Users/ivyhuang/Downloads/OpenFace-master/build/bin/FeatureExtraction"

#extracts OpenFace features from video file at video_loc
os.system(feature_extraction_exe + ' -f "' + video_loc + '"')

#finds output from running OpenFace
data = pd.read_csv('/Users/ivyhuang/Downloads/processed/2015-10-15-15-14.csv', engine='python', delimiter = ', ')

#forms DataFrame in desired output format
reformatted_data = pd.DataFrame(columns=['Time', 'Duration', 'Trackname', 'Comments'])

for index, row in data.iterrows():
    time = int(round(row['timestamp'] * 1000)) #time in milliseconds
    horizontal_gaze_angle = row['gaze_angle_x']
    trackname = 'right' if horizontal_gaze_angle < 0 else 'left'
    reformatted_data.loc[index] = [time, 0, trackname, '(null)']

reformatted_data.to_csv('Reformatted_Data.csv', index=False)