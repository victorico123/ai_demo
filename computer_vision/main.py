# import cv2
# import argparse
# from ultralytics import YOLO
# import supervision as sv
# import numpy as np


# ZONE_POLYGON = np.array([
#     [0, 0],
#     [1, 0],
#     [1, 1],
#     [0, 1]
# ])

# def parse_arguments() -> argparse.Namespace:
#     """Parse command-line arguments."""
#     parser = argparse.ArgumentParser(description="Crowd Photo Detection Script")
#     parser.add_argument(
#         "--webcam-resolution", 
#         default=[1280, 720], 
#         nargs=2, 
#         type=int
#     )
#     parser.add_argument(
#         "--model",
#         type=int,
#         default=1,
#         choices=[1, 2],  # Model selection [1: YoloV11n, 2: YoloV11n-face]
#         help="Model used ([1] YoloV11n, [2] YoloV11n-face)"
#     )
#     parser.add_argument(
#         "--area",
#         type=int,
#         default=1,
#         choices=[1, 2],  # Area selection [1: whole screen, 2: half screen]
#         help="Area to focus on ([1] whole screen, [2] half screen)"
#     )
#     parser.add_argument(
#         "--source",
#         type=int,
#         default=0,
#         choices=[0, 1, 2],  # Source selection [0: laptop camera, 1: webcam, 2: crowd.mp4]
#         help="Source to focus on ([0]laptop camera, [1] webcam, [2] crowd.mp4)"
#     )
#     args = parser.parse_args()
#     return args


# def main():
#     args = parse_arguments()
#     frame_width, frame_height = args.webcam_resolution

#     # Adjust ZONE_POLYGON based on the area argument
#     cap=None
#     if args.source == 0:
#         cap = cv2.VideoCapture(0)
#     elif args.source == 1:
#         cap = cv2.VideoCapture(1)
#     elif args.source == 2:
#         source="./source/crowd.mp4"
#         cap = cv2.VideoCapture(source)
#     else:
#         print("Error: Invalid source selected")
#         return
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

#     # Load the YOLO model
#     try:
#         model_location=""
#         if args.model == 1:
#             model_location="./model/yolo11n.pt"           
#         elif args.model == 2:
#             model_location="./model/yolov11n-face.pt"
#         model = YOLO(model_location)
#     except Exception as e:
#         print(f"Error: Could not load YOLO model from {args.model}. Exception: {e}")
#         return

#     box_annotator = sv.BoxAnnotator(
#         thickness=2,
#         text_scale=1
#     )

#     # Adjust ZONE_POLYGON based on the area argument
#     if args.area == 1:
#         zone_polygon = np.array([
#             [0, 0],
#             [1, 0],
#             [1, 1],
#             [0, 1]
#         ])
#     elif args.area == 2:
#         zone_polygon = np.array([
#             [0, 0],
#             [0.5, 0],
#             [0.5, 1],
#             [0, 1]
#         ])
#     else:
#         print("Error: Invalid area selected")
#         return

#     zone_polygon = (ZONE_POLYGON * np.array(args.webcam_resolution)).astype(int)
#     zone = sv.PolygonZone(polygon=zone_polygon, frame_resolution_wh=tuple(args.webcam_resolution))
#     zone_annotator = sv.PolygonZoneAnnotator(
#         zone=zone, 
#         color=sv.Color.blue(),
#         thickness=2,
#         text_thickness=4,
#         text_scale=2
#     )

#     FPS = 1/60
#     FPS_MS = int(FPS * 1000)

#     while True:
#         ret, frame = cap.read()
#         frame = cv2.flip(frame, 1)

#         # Resize the frame to a smaller resolution (e.g., 640x360)
#         frame_resized = cv2.resize(frame, (640, 360))  # Resize to 640x360 or any other resolution you prefer

#         # Perform inference on the resized frame
#         result = model(frame_resized, agnostic_nms=True)[0]
#         detections = sv.Detections.from_yolov8(result)
#         detections = detections[detections.class_id == 0]

#         frame = box_annotator.annotate(
#             scene=frame, 
#             detections=detections, 
#             skip_label=True
#         )

#         zone.trigger(detections=detections)
#         frame = zone_annotator.annotate(scene=frame)      

#         cv2.imshow("yolov8", frame)
#         cv2.waitKey(FPS_MS)


# if __name__ == "__main__":
#     main()


import cv2
import argparse
from ultralytics import YOLO
import supervision as sv
import numpy as np


ZONE_POLYGON = np.array([
    [0, 0],
    [1, 0],
    [1, 1],
    [0, 1]
])

def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Crowd Photo Detection Script")
    parser.add_argument(
        "--webcam-resolution", 
        default=[1280, 720], 
        nargs=2, 
        type=int
    )
    parser.add_argument(
        "--model",
        type=int,
        default=1,
        choices=[1, 2],  # Model selection [1: YoloV11n, 2: YoloV11n-face]
        help="Model used ([1] YoloV11n, [2] YoloV11n-face)"
    )
    parser.add_argument(
        "--area",
        type=int,
        default=1,
        choices=[1, 2],  # Area selection [1: whole screen, 2: half screen]
        help="Area to focus on ([1] whole screen, [2] half screen)"
    )
    parser.add_argument(
        "--source",
        type=int,
        default=0,
        choices=[0, 1, 2],  # Source selection [0: laptop camera, 1: webcam, 2: crowd.mp4]
        help="Source to focus on ([0] laptop camera, [1] webcam, [2] crowd.mp4)"
    )
    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    frame_width, frame_height = args.webcam_resolution

    # Set up the video capture source
    cap = None
    if args.source == 0:
        cap = cv2.VideoCapture(0)
    elif args.source == 1:
        cap = cv2.VideoCapture(1)
    elif args.source == 2:
        source = "./source/crowd.mp4"
        cap = cv2.VideoCapture(source)
    else:
        print("Error: Invalid source selected")
        return
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    # Load the YOLO model
    try:
        model_location = ""
        if args.model == 1:
            model_location = "./model/yolo11n.pt"
        elif args.model == 2:
            model_location = "./model/yolov11n-face.pt"
        model = YOLO(model_location)
    except Exception as e:
        print(f"Error: Could not load YOLO model from {model_location}. Exception: {e}")
        return

    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_scale=1
    )

    # Adjust ZONE_POLYGON based on the area argument
    if args.area == 1:
        zone_polygon = np.array([
            [0, 0],
            [1, 0],
            [1, 1],
            [0, 1]
        ])
    elif args.area == 2:
        zone_polygon = np.array([
            [0, 0],
            [0.5, 0],
            [0.5, 1],
            [0, 1]
        ])
    else:
        print("Error: Invalid area selected")
        return

    zone_polygon = (ZONE_POLYGON * np.array(args.webcam_resolution)).astype(int)
    zone = sv.PolygonZone(polygon=zone_polygon, frame_resolution_wh=tuple(args.webcam_resolution))
    zone_annotator = sv.PolygonZoneAnnotator(
        zone=zone, 
        color=sv.Color.blue(),
        thickness=2,
        text_thickness=4,
        text_scale=2
    )

    FPS = 1/60
    FPS_MS = int(FPS * 1000)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame from source.")
            break

        frame = cv2.flip(frame, 1)

        # Resize the frame to a smaller resolution (e.g., 640x360)
        resized_width, resized_height = 640, 360
        frame_resized = cv2.resize(frame, (resized_width, resized_height))

        # Perform inference on the resized frame
        result = model(frame_resized, agnostic_nms=True)[0]
        detections = sv.Detections.from_yolov8(result)

        # Scale the bounding box coordinates back to the original frame dimensions
        scale_x = frame_width / resized_width
        scale_y = frame_height / resized_height
        detections.xyxy[:, [0, 2]] *= scale_x  # Scale x-coordinates
        detections.xyxy[:, [1, 3]] *= scale_y  # Scale y-coordinates

        # Filter detections for class_id 0 (e.g., person)
        detections = detections[detections.class_id == 0]

        # Annotate the original frame with bounding boxes
        frame = box_annotator.annotate(
            scene=frame, 
            detections=detections, 
            skip_label=True
        )

        # Annotate the frame with the polygon zone
        zone.trigger(detections=detections)
        frame = zone_annotator.annotate(scene=frame)      

        cv2.imshow("yolov8", frame)
        if cv2.waitKey(FPS_MS) & 0xFF == ord('q'):  # Press 'q' to quit
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
