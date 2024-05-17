"""Module for object detection using Ultralytics YOLOv8."""

import urllib.request
from pathlib import Path
from random import randint

import cv2
from ultralytics import YOLO

MODELS = ["yolov8n", "yolov8s", "yolov8m"]


class ObjectDetector:
    """Detects objects in images using YOLOv8 models."""

    def __init__(self, model_name="yolov8s"):
        """Initializes the ObjectDetector.

        Args:
            model_name: The name of the YOLOv8 model to use (e.g., "yolov8n").
        """

        if model_name not in MODELS:
            raise ValueError(f"Invalid model name. Choose from: {MODELS}")

        self.model_name = model_name
        self.model_path = f"{model_name}.pt"
        self.model_url = f"https://github.com/ultralytics/assets/releases/download/v8.2.0/{self.model_path}"
        # TODO Update the model path to take from models dir
        base_dir = Path(__file__).resolve().parent 
        self.face_model_path = str(base_dir/"yolov8n-face.pt")

        # Download if model doesn't exist
        if not Path(self.model_path).is_file():
            self._download_model()

        self.model = YOLO(self.model_path)
        self.face_model = YOLO(self.face_model_path)

    def _download_model(self):
        """Downloads the specified YOLOv8 model."""
        print(f"Downloading model: {self.model_name} from {self.model_url}")
        urllib.request.urlretrieve(self.model_url, self.model_path)
        print("Download complete!")

    def detect_objects(self, image_path):
        """Detects objects in an image.

        Args:
            image_path: Path to the image file.

        Returns:
            List of detections, each a list of [x1, y1, x2, y2, class_name, confidence].
        """
        # common objects
        d1 = self.model.predict(image_path)

        # face detections
        d2 = self.face_model.predict(image_path)
        results = []
        for detection in [d1, d2]:
            for box in detection[0].boxes:
                results.append(
                    [round(x) for x in box.xyxy[0].tolist()]
                    + [
                        detection[0].names[int(box.cls[0])],
                        round(box.conf[0].item(), 2),
                    ]
                )

        return results

    def visualize_predictions(
        self, image_path, predictions, class_colors=None, font_scale=0.5
    ):
        """Visualizes predictions on the image."""

        image = cv2.imread(image_path)
        class_colors = class_colors or self._generate_random_colors(predictions)

        for x1, y1, x2, y2, class_name, confidence in predictions:
            color = class_colors[class_name]
            text = f"{class_name} ({confidence:.2f})"

            # Calculate text size and baseline
            (text_width, text_height), baseline = cv2.getTextSize(
                text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 1
            )

            # Ensure text stays within bounding box
            text_x = min(x1, x2 - text_width)
            text_y = min(y1, y2 - text_height + baseline)

            # Draw bounding box
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

            # Draw text label
            cv2.putText(
                image,
                text,
                (text_x, text_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                font_scale,
                color,
                1,
            )

        cv2.imwrite(f"{image_path}_visualized.jpg", image)

    def _generate_random_colors(self, predictions):
        """Generates random colors for classes in predictions."""
        unique_classes = set(p[4] for p in predictions)
        return {
            name: (randint(0, 255), randint(0, 255), randint(0, 255))
            for name in unique_classes
        }