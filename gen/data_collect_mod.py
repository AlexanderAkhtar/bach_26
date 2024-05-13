d = time.time()
writer.writerow({"frame nummer": a, "x=": points[idTo][0], "y=": points[idTo][1], "time=": d-c})
writer.writerow({"frame nummer": a, "x=": points[idFrom][0], "y=": points[idFrom][1], "time=": d-c})
