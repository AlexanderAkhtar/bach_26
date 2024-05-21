import pandas as pd

path_to_data = 'C:/Users/Alexander/Desktop/bachelor/data'
model = 'result-ultralytics-YOLOv8x-oiv7'
pose_estimation = False #trigger that determines what version of result checker is used pose estimation vs person detection
detection_factor = 0.05
start_hw = 11 #sets the start and end time for the hwmonitor files
slutt_hw = 222

test_result_path = path_to_data + '/pre_compare_' + model + '/modified_test_' + model + '.csv' #sets the file paths for each of the input information
true_result_path = 'C:/Users/Alexander/Desktop/bachelor/data/modified_true_result.csv'
cpu_path1 = path_to_data + '/pre_compare_' + model + '/[CSV]/AMD Ryzen 9 3900X CCX #0 Utilization.csv'
cpu_path2 = path_to_data + '/pre_compare_' + model + '/[CSV]/AMD Ryzen 9 3900X CCX #1 Utilization.csv'
cpu_path3 = path_to_data + '/pre_compare_' + model + '/[CSV]/AMD Ryzen 9 3900X CCX #2 Utilization.csv'
cpu_path4 = path_to_data + '/pre_compare_' + model + '/[CSV]/AMD Ryzen 9 3900X CCX #3 Utilization.csv'
gpu_path = path_to_data + '/pre_compare_' + model + '/[CSV]/NVIDIA GeForce RTX 3060 GPU Utilization.csv'
mem_path = path_to_data + '/pre_compare_' + model + '/[CSV]/ASRock B550M-ITXac System Memory Utilization.csv'
fp_path = path_to_data + '/compare_' + model + '/false_positive_' + model + '.csv' #sets the file path for the output files
fn_path = path_to_data + '/compare_' + model + '/false_negative_' + model + '.csv'
total_prediction_path = path_to_data + '/compare_' + model + '/total_prediction_' + model + '.csv'
report_path = path_to_data + '/compare_' + model + '/report_' + model + '.csv'

def get_entries(frame_number, file_path): #returns all the entries in a result file that are of the given frame_number
    original = pd.read_csv(file_path)
    filtered = original[original['frame nummer'] == frame_number]
    return filtered

def reshape_hw(start, slutt, file_path):#excludes all the entries in the hwmonitor files that are outside the time interval set by the start and slutt
    original = pd.read_csv(file_path)
    f1 = original[original[0] <= start]
    filtered = original[f1[0] >= slutt]
    return filtered

def within_bounds_pose(x, y, df1):#checks if a given point x,y is within a true result bounding box, and returns a mask to be used for filtering the original input
    for idx, row in df1.iterrows():
        if row['XMin'] <= x <= row['XMax'] and row['YMin'] <= y <= row['YMax']:
            return False
    return True

def within_bounds_detection(x1, y1, x2, y2, df1):#does the same as within_bounds_pose(), but is designed for detection CVM, therefor it takes 2 sets of x,y values
    for idx, row in df1.iterrows():
        if row['XMin'] <= x1 <= row['XMax'] and row['YMin'] <= y1 <= row['YMax'] and row['XMin'] <= x2 <= row['XMax'] and row['YMin'] <= y2 <= row['YMax']:
            return False
    return True

def is_point_within_bounds(x, y, xmin, xmax, ymin, ymax):#cheks if the given x and y values is within the bounding box described by the x and y min and max values
    return xmin <= x <= xmax and ymin <= y <= ymax

def has_points_within_bounds_pose(row, df2):# cheks if the true result bounding box has a prediction within it
    for idx, point in df2.iterrows():
        if is_point_within_bounds(point['x='], point['y='], row['XMin'], row['XMax'], row['YMin'], row['YMax']):
            return True
    return False

def has_points_within_bounds_detection(row, df2):#does the same as has_points_within_bounds_pose(), but is designed for detection CVM,
    for idx, point in df2.iterrows():
        if is_point_within_bounds(point['x1='], point['y1='], row['XMin'], row['XMax'], row['YMin'], row['YMax']) and is_point_within_bounds(point['x2='], point['y2='], row['XMin'], row['XMax'], row['YMin'], row['YMax']):
            return True
    return False

def reduce_result(file_result):# used to reduce the size of a predicted bounding bow by a certain factor
    file_result['x1='] = file_result['x1='].multiply(1+detection_factor).astype(int)
    file_result['y1='] = file_result['y1='].multiply(1+detection_factor).astype(int)
    file_result['x2='] = file_result['x2='].multiply(1-detection_factor).astype(int)
    file_result['y2='] = file_result['y2='].multiply(1-detection_factor).astype(int)

def find_max_and_mean(file_path): #finds the max and average values of a hwmonitor .csv file
    file = pd.read_csv(file_path)
    max = file[file.columns[1]].max()
    avg = file[file.columns[1]].mean()
    return max, avg

def cpu_max_and_mean(cpu_path1, cpu_path2, cpu_path3, cpu_path4): # takes the 4 cpu cores and findes the max and average values of the hwmonitor .csv files.
    cpumax1, cpuavg1 = find_max_and_mean(cpu_path1)
    cpumax2, cpuavg2 = find_max_and_mean(cpu_path2)
    cpumax3, cpuavg3 = find_max_and_mean(cpu_path3)
    cpumax4, cpuavg4 = find_max_and_mean(cpu_path4)
    cpumax = max(cpumax1, cpumax2, cpumax3, cpumax4)
    cpuavg = (cpuavg1 + cpuavg2 + cpuavg3 + cpuavg4)/4
    return cpumax, cpuavg

total_prediction = pd.DataFrame() #creates the listes and dataframes used to record the output data
report = pd.DataFrame()
false_positive = []
false_negative = []

if (pose_estimation):    #determines if the PE or PD versions of the evaluation script should be ran
    for i in range(2691): #itarates over every
        true_result = get_entries(i, true_result_path) #grabs the relevant frames entries
        test_result = get_entries(i, test_result_path)

        new_line = {'frame number': i, 'total predicions': test_result.shape[0], 'frame time': test_result['time='].mean()} #gathers and writes the information to the total prediction
        total_prediction = pd.concat([total_prediction, pd.DataFrame([new_line])], ignore_index=True)

        mask1 = test_result.apply(lambda row: within_bounds_pose(row['x='], row['y='], true_result), axis=1)#gathers and writes the information to the false positive file
        false_positive.append(test_result[mask1]) 

        mask2 = true_result.apply(lambda row: not has_points_within_bounds_pose(row, test_result), axis=1) #gathers and writes the information to the false negative file
        false_negative.append(true_result[mask2])
else: # this is the person detection version of the above code, difference being that the reduce_results() is ran and the detection versions of the helper functions is used
    for i in range(2691):
        true_result = get_entries(i, true_result_path)
        test_result = get_entries(i, test_result_path)
        reduce_result(test_result)

        new_line = {'frame number': i, 'total predicions': test_result.shape[0], 'frame time': test_result['time='].mean()}
        total_prediction = pd.concat([total_prediction, pd.DataFrame([new_line])], ignore_index=True)

        mask1 = test_result.apply(lambda row: within_bounds_detection(row['x1='], row['y1='], row['x2='], row['y2='], true_result), axis=1)
        false_positive.append(test_result[mask1]) 

        mask2 = true_result.apply(lambda row: not has_points_within_bounds_detection(row, test_result), axis=1)
        false_negative.append(true_result[mask2])

concat_fp = pd.concat(false_positive, ignore_index=True) # concatinates the false positives and false negatives 
concat_fn = pd.concat(false_negative, ignore_index=True)


cpumax, cpuavg = cpu_max_and_mean(cpu_path1, cpu_path2, cpu_path3, cpu_path4) #generates and gathers the hwmonitor information
gpumax, gpuavg = find_max_and_mean(gpu_path)
memmax, memavg = find_max_and_mean(mem_path)

#creates the report file entry
report_line = {'frame number': 2691, 
              'total time taken': total_prediction['frame time'].max(), 
              'total number of predictions': total_prediction['total predicions'].sum(), 
              'total number of false positives': concat_fp.shape[0],
              'total number of false negatives': concat_fn.shape[0],
              'predicition accuracy (correct estimation/total estimation)': ((total_prediction['total predicions'].sum() - concat_fp.shape[0])/total_prediction['total predicions'].sum()),
              'FPS frame number/total time taken': (2691/total_prediction['frame time'].max()),
              'CPU max usage': cpumax,
              'CPU avg usage': cpuavg,
              'GPU max usage': gpumax,
              'GPU avg usage': gpuavg,
              'Memory max usage': memmax,
              'Memory avg usage': memavg,
               }

report = pd.concat([report, pd.DataFrame([report_line])], ignore_index=True) #concatinates the report file 

total_prediction.to_csv(total_prediction_path, index=False)#saves all the outpur files
report.to_csv(report_path, index=False)
concat_fp.to_csv(fp_path, index=False)
concat_fn.to_csv(fn_path, index=False)