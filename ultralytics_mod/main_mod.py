import cv2 ##https://github.com/ultralytics/ultralytics
import argparse
import csv
import time

from ultralytics import YOLO
import supervision as sv

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description= "YOLOv8 live")
    parser.add_argument(
        "--webcam-resolution",
        default=[1920, 1080],
        nargs=2,
        type=int
    )
    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    frame_width, frame_height = args.webcam_resolution

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    model = YOLO("yolov8l.pt")

    c = time.time()
    with open("result.csv", mode="w", newline='') as csvfile:
        field = ["frame nummer", "x1=", "y1=","x2=", "y2=", "time="]
        writer = csv.DictWriter(csvfile, fieldnames=field)
        writer.writeheader()

        box_annotator = sv.BoxAnnotator(
            thickness=2,
            text_thickness=2,
            text_scale=1
        )

        while True:
            ret, frame = cap.read()
            a = a+1

            result = model(frame)[0]
            detections = sv.Detections.from_ultralytics(result)
            for i in range(len(detections)):
                x1, y1, x2, y2 = detections.xyxy[i].astype(int)
                d = time.time()
                writer.writerow({"frame nummer": a, "x1=": x1, "y1=": y1,"x2=": x2, "y2=": y2, "time=": d-c})

            frame = box_annotator.annotate(scene=frame, detections=detections)

            cv2.imshow("yolov8", frame)

            if (cv2.waitKey(30) == 27):
                break

if __name__ == "__main__":
    main()
