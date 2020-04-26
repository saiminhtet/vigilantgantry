# -*- coding: utf-8 -*-

"""
~~~~~~~~~~~~~~~
This file is the entrypoint to the program.
"""

import argparse, os

# from utils import vid_utils

from video_processor.video_processor import VideoProcessor

from person_detector.person_detector import PersonDetector


from person_detector.person_detector import PersonDetector
from face_detector.face_detector import FaceDetector
from face_segmentor.face_segmentor import FaceSegmentor


VIDEO_SOURCE = os.getenv("VIDEO_SOURCE", "sample/sample.mp4")
PERSON_DETECTION_ROI_BOUNDARY = tuple(
    os.getenv("PERSON_DETECTION_ROI_BOUNDARY", default=((0, 0), (1280, 720)))
)
PERSON_DETECTION_INTERCEPT_BOUNDARY = list(
    os.getenv("PERSON_DETECTION_INTERCEPT_BOUNDARY", default=[600, 350, 700, 450])
)
GANTRY_ID = int(os.getenv("GANTRY_ID", default=1))
FACE_SEG_THRESHOLD_VALUE = float(os.getenv("FACE_SEG_THRESHOLD_VALUE", default=0.5))
FULL_SCREEN_DISPLAY = bool(os.getenv("FULL_SCREEN_DISPLAY", default=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="VigilantGantry Face Segmentation Engine"
    )
    parser.add_argument(
        "--video_source",
        dest="video_source",
        type=str,
        default="sample/sample.mp4",
        help="insert binary video file path or rtsp address or webcam id",
    )

    parser.add_argument(
        "--person_detect_roi_boundary",
        type=str,
        default=PERSON_DETECTION_ROI_BOUNDARY,
        help="insert coordinates in which persons will be detection",
    )
    parser.add_argument(
        "--person_detect_intercept_boundary",
        type=str,
        default=PERSON_DETECTION_INTERCEPT_BOUNDARY,
        help="insert coordinates in which faces will be detection",
    )
    parser.add_argument(
        "--gantry_id", type=str, default=GANTRY_ID, help="insert gantry id"
    )

    parser.add_argument(
        "--face_seg_threshold_value",
        type=int,
        default=FACE_SEG_THRESHOLD_VALUE,
        help="insert proportion of exposed face over total face area",
    )

    parser.add_argument(
        "--full_screen_display",
        type=bool,
        default=FULL_SCREEN_DISPLAY,
        help="insert True for full screen display",
    )

    args = parser.parse_args()

    # if video source is webcam, convert str to int
    video_source = args.video_source
    if video_source is not None and video_source.isdigit():
        video_source = int(video_source)

    video_session = VideoProcessor(
        video_source=video_source,
        video_width=1280,
        video_height=720,
        person_detect_roi_boundary=args.person_detect_roi_boundary,
        person_detect_intercept_boundary=args.person_detect_intercept_boundary,
        gantry_id=args.gantry_id,
        face_seg_threshold_value=args.face_seg_threshold_value,
        full_screen_display=args.full_screen_display,
    )

    person_detector = PersonDetector(
        class_path="person_detector/data/coco.names",
        config_path="person_detector/cfg/yolov3.cfg",
        weights_path="person_detector/weights/yolov3.weights",
        batch_size=1,
        nms_threshold=0.4,
        scales="1,2,3",
        confidence=0.8,
        num_classes=80,
        resolution="416",
    )
    face_detector = FaceDetector()
    face_segmentor = FaceSegmentor()
    video_session.process_video(person_detector, face_detector, face_segmentor)
