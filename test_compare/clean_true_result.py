import pandas as pd #imports the pandas library, used to manipulate the .csv folder

file_path = "C:/Users/Alexander/Desktop/bachelor/true_result/annotations/default-annotations-bbox.csv" #the file path of the unaltered data
height = 1080
width = 1920

original = pd.read_csv(file_path, index_col=False) #reads in the .csv from file_path into a pandas dataframe
filtered = original.drop(columns=['Source', 'Confidence', 'IsOccluded', 'IsTruncated', 'IsGroupOf', 'IsDepiction', 'IsInside']) #remove all unnecessary columns from the dataframe
filtered['ImageID'] = filtered['ImageID'].str[8:] #removes the first 8 char from the string in ImageID column, this is done so that the next line only has numbers to parse
filtered['ImageID'] = filtered['ImageID'].astype(int) #converts the string of numbers to a int value
filtered = filtered.rename(columns={'ImageID': 'frame nummer'}) #renames the ImageID column to frame nummer

#because the raw data is in the form of a double percent of screen, the 4 lines under multiply the height and width also it rounds to a discrete integer
filtered['XMin'] = filtered['XMin'].multiply(width).astype(int)
filtered['XMax'] = filtered['XMax'].multiply(width).astype(int)
filtered['YMin'] = filtered['YMin'].multiply(height).astype(int)
filtered['YMax'] = filtered['YMax'].multiply(height).astype(int)

filtered.to_csv('C:/Users/Alexander/Desktop/bachelor/data/modified_true_result.csv', index=False) #saves the modifications to a new .csv file