import cv2
import argparse
import csv
import time
from video_reader import VideoReader

from ultralytics import YOLO
import supervision as sv

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description= "YOLOv8 live")
    parser.add_argument(
        '--video', 
        help='Path to video file', ##might need to be help not file_name
        type=str, 
        default=''
    )
    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()
    if args.video == '' and args.webcam == '':
        raise ValueError('--video has to be provided')
    if args.video != '':
        frame_provider = VideoReader(args.video)
        is_video = True
    base_height = 1920
    #fx = args.fx
    model = YOLO("yolov8l.pt")
    c = time.time()
    a = 1
    with open("result.csv", mode="w", newline='') as csvfile:
        field = ["frame nummer", "x1=", "y1=","x2=", "y2=", "time="]
        writer = csv.DictWriter(csvfile, fieldnames=field)
        writer.writeheader()

        box_annotator = sv.BoxAnnotator(
            thickness=2,
            text_thickness=2,
            text_scale=1
        )

        for frame in frame_provider:
            result = model(frame)[0]
            detections = sv.Detections.from_ultralytics(result)
            for i in range(len(detections)):
                x1, y1, x2, y2 = detections.xyxy[i].astype(int)
                if (detections.class_id[i].astype(int) == 0):
                    d = time.time()
                    writer.writerow({"frame nummer": a , "x1=": x1, "y1=": y1,"x2=": x2, "y2=": y2, "time=": d-c})

            a = a+1
            frame = box_annotator.annotate(scene=frame, detections=detections)
            cv2.imshow("yolov8", frame)
            if (cv2.waitKey(30) == 27):
                break

if __name__ == "__main__":
    main()
