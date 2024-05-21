import pandas as pd

#a simple program to reduce the frame nummer value by one
model = 'result-ultralytics-YOLOv8x-oiv7'
file_path = 'C:/Users/Alexander/Desktop/bachelor/data/pre_compare_' + model + '/' + model + '.csv' #the file path of the unaltered data


o = pd.read_csv(file_path, index_col=False)
o['frame nummer'] -= 1

o.to_csv('C:/Users/Alexander/Desktop/bachelor/data/pre_compare_' + model + '/modified_test_' + model + '.csv', index=False)