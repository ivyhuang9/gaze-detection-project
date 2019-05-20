import os
import pandas as pd


def get_features(video_path, video_name, video_format, feature_extraction_exe):
    """
    Extracts OpenFace features from a video file.
    
    Parameters:
        video_path (String): path to the video (including the end slash, and not including the video name)
        video_name (String): name of the video (not including the video format)
        video_format (String): video file format (e.g. .mov)
        feature_extraction_exe (String): path to FeatureExtraction executable within OpenFace
    """
    os.system(feature_extraction_exe + ' -f "' + video_path + video_name + video_format + '"')

def reformat_data(processed_path, video_name, human_readable = False):
    """
    Reformats the CSV output of OpenFace FeatureExtraction into the PsychDS format. Creates a CSV file named
    ReformattedData.csv with the newly reformatted data.
    
    Parameters:
        processed_path (String): 
        video_name (String): 
        human_readable (bool):
            True if should output reformatted file in a human_readable format (i.e. each row reflects a
                change in the trackname)
            False otherwise (i.e. for comparing purposes as in the compare_data function)
    """
    #finds csv output from running OpenFace
    data = pd.read_csv(video_path + "processed/" + video_name + ".csv", engine='python', delimiter = ', ')   
    #forms DataFrame in desired output format
    reformatted_data = pd.DataFrame(columns=['Time', 'Duration', 'Trackname', 'Comments'])  
    #for human_readable = True
    new_index = 0
    
    for index, row in data.iterrows():
        horizontal_gaze_angle = row['gaze_angle_x']
        if row['success'] == 0:
            trackname = 'off'
        elif row['gaze_0_x'] < row['gaze_1_x']:
            trackname = 'away'
        elif horizontal_gaze_angle >= 0.22:
            trackname = 'right'
        else:
            trackname = 'left'
        
        if human_readable:
            if new_index == 0 or reformatted_data.loc[new_index - 1]['Trackname'] != trackname:
                reformatted_data.loc[new_index] = [row['timestamp'], 0, trackname, '(null)']
                new_index += 1
        else:
            reformatted_data.loc[index] = [row['timestamp'], 0, trackname, '(null)']
            
    reformatted_data.to_csv(video_path + "Reformatted_Data.csv", index=False)
    

def convert_to_seconds(row):
    """
    Helper function. Converts the timestamp of a row in a CSV file into seconds.
    
    Returns:
        float: the timestamp in seconds
    """
    return row['Hour']*3600 + row['Minute']*60 + row['Second'] + float(row['Frame'])/30

def compare_data(original_csv_path, new_csv_path, time_offset):
    """
    
    
    Assumes that the original CSV 
    
    Parameters:
        original_csv_path: path to the CSV file containing the original data (i.e. the standard being
            comparing to)
        new_csv_path: path to the CSV file containing the new data (i.e. the)
        time_offset: number of seconds that pass in the video before the first trial starts
    
    Returns:
        float: accuracy of data in the new CSV file when compared to the original CSV file
    """
    original_csv = pd.read_csv(original_csv_path, engine='python', delimiter = '\t') #assumes tsv file
    new_csv = pd.read_csv(new_csv_path, engine='python', delimiter = ',')

    start_time = convert_to_seconds(original_csv.iloc[0])

    original_index = 0
    new_index = 0
    num_correct = 0
    count = 0
    false_trial = 0
    
    while new_index < len(new_csv):
        if new_csv.iloc[new_index]['Time'] >= time_offset:
            if original_index < len(original_csv):
                time_since = convert_to_seconds(original_csv.iloc[original_index]) - start_time
            while time_since < new_csv.iloc[new_index]['Time'] and original_index < len(original_csv):
                original_index += 1
                if original_index < len(original_csv):
                    time_since = convert_to_seconds(original_csv.iloc[original_index]) - start_time
            original_index -= 1
            #check if trial is ongoing
            if original_csv.iloc[original_index]['Trial'] == False:
                false_trial += 1
                continue
            #check if correct classification if trial is ongoing
            if new_csv.iloc[new_index]['Trackname'] == original_csv.iloc[original_index]['Type']:
                num_correct += 1
            count += 1
        new_index += 1
    return num_correct/count

video_path = "/Users/ivyhuang/Downloads/UROP/"
#video_name = "10123B.24.M.TL2-24-B"
video_name = "7292A.25.M.HABLA25-1"
video_format = ".mov"
feature_extraction_exe = "/Users/ivyhuang/Downloads/OpenFace-master/build/bin/FeatureExtraction"

#get_features(video_path + video_name + "/", video_name, video_format, feature_extraction_exe)
#reformat_data(video_path + video_name + "/", video_name, 11)
accuracy = compare_data(video_path + video_name + "/" + video_name + "_timecourse_data.tsv", video_path + video_name + "/Reformatted_Data.csv", 11)
print(accuracy)