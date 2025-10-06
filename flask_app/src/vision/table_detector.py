import cv2
import threading
import time
import base64
import json
import numpy as np
from ..config import Config


class TableDetector:
    def __init__(self, camera_source=0):
        self.camera_source = camera_source
        self.capture = cv2.VideoCapture(camera_source)
        self.running = True
        self.camera_available = self.capture.isOpened()
        self.results = {}
        self.regions = {}
        self._frame_lock = threading.Lock()
        self._last_frame_jpeg = None

        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.capture:
            self.capture.release()
        self.camera_available = False

    def add_or_update_region(self, region):
        # region contains table_id, x, y, width, height
        tid = int(region.get('table_id'))
        self.regions[tid] = {
            'table_number': region.get('table_number'),
            'x': int(region.get('x', 0)),
            'y': int(region.get('y', 0)),
            'width': int(region.get('width', 0)),
            'height': int(region.get('height', 0))
        }

    def get_results(self):
        # return a copy
        return dict(self.results)

    def frame_generator(self):
        # yields jpeg frame bytes
        while True:
            with self._frame_lock:
                if self._last_frame_jpeg is None:
                    time.sleep(0.05)
                    continue
                frame = self._last_frame_jpeg
            yield frame
            time.sleep(0.03)

    def _run(self):
        ok, prev = self.capture.read()
        if not ok:
            return
        prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)

        while self.running:
            ok, frame = self.capture.read()
            if not ok:
                time.sleep(0.1)
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # simple motion detection per region
            for tid, region in self.regions.items():
                x, y, w, h = region['x'], region['y'], region['width'], region['height']
                roi = gray[y:y + h, x:x + w]
                prev_roi = prev_gray[y:y + h, x:x + w]

                if roi.size == 0 or prev_roi.size == 0:
                    continue

                diff = cv2.absdiff(roi, prev_roi)
                non_zero = np.sum(diff > 25)
                motion_ratio = non_zero / float(max(1, roi.size))

                # color detection (skin-tone by simplistic HSV ranges)
                roi_color = frame[y:y + h, x:x + w]
                hsv = cv2.cvtColor(roi_color, cv2.COLOR_BGR2HSV)
                lower = np.array([0, 30, 60])
                upper = np.array([20, 255, 255])
                mask = cv2.inRange(hsv, lower, upper)
                skin_ratio = float(np.count_nonzero(mask)) / float(max(1, mask.size))

                score = min(1.0, motion_ratio * 2 + skin_ratio * 0.8)
                status = (
                    'empty' if score < 0.05
                    else ('occupied' if score >= 0.2 else 'reserved')
                )

                self.results[tid] = {
                    'table_number': region.get('table_number'),
                    'status': status,
                    'confidence': float(score),
                    'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
                    'detected_by': 'camera'
                }

                # draw rectangle and label
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(
                    frame,
                    f"{region.get('table_number')} {status} {score:.2f}",
                    (x, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    1
                )

            # JPEG encode
            ret, jpeg = cv2.imencode('.jpg', frame)
            if ret:
                with self._frame_lock:
                    self._last_frame_jpeg = jpeg.tobytes()

            prev_gray = gray
            time.sleep(0.2)
