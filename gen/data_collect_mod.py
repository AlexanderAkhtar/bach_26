##this is a general form of the data collection modifications made to the base scripts.

import csv ##used to write the data collected to a .csv.
import time ##used to collect data regarding the time cost of the models.

c = time.time() ##sets a base time that is used to compare and determine how long since start a frame was prosessed.
a = 0 ##used as a counter in situations where there isnt a reasonable alternative to point to the current frame.

with open("result.csv", mode="w", newline='') as csvfile: ##opens the result.csv to allow for writing. 
    field = ["frame nummer", "x=", "y=", "time="] ##sets the columns of the result.csv.
    writer = csv.DictWriter(csvfile, fieldnames=field) ##creates a writer obj.
    writer.writeheader() ##writes the column headers into the result.csv.
    a = a+1 ##itarates the counter variable, should be placed within the base in a reasonable spot.
    d = time.time() ##captures the current time for the second half of the time comparison, should be placed within the base in a reasonable spot.
    writer.writerow({"frame nummer": a, "x=": x_value, "y=": y_value, "time=": d-c}) ##writes the results to the result.csv.
