import sys
import cv2
import os
import json
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QListView, QLabel, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt, QStringListModel, QMetaObject, QCoreApplication
import datetime
import time
from imgbeddings import imgbeddings
from PIL import Image
import mediapipe as mp
import csv

class Ui_MainWindow_List(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1366, 768)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Main layout
        self.main_layout = QHBoxLayout(self.centralwidget)
        
        # Left side (camera)
        self.camera_layout = QVBoxLayout()
        self.camera_0 = QLabel()
        self.camera_0.setObjectName("camera_0")
        self.camera_0.setMinimumSize(890, 730)
        self.camera_layout.addWidget(self.camera_0)
        self.main_layout.addLayout(self.camera_layout)
        
        # Right side (logo and list)
        self.right_layout = QVBoxLayout()
        
        # Logo
        self.logo_label = QLabel()
        self.logo_label.setObjectName("logo_label")
        self.logo_label.setMinimumSize(450, 200)
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.right_layout.addWidget(self.logo_label)
        
        # List
        self.listView = QListView()
        self.listView.setObjectName("listView")
        self.listView.setMinimumSize(450, 500)
        self.right_layout.addWidget(self.listView)
        
        self.main_layout.addLayout(self.right_layout)
        
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def set_logo(self, logo_path):
        pixmap = QPixmap(logo_path)
        self.logo_label.setPixmap(pixmap.scaled(self.logo_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# Load the face embeddings
with open("face_embeddings.json", "r", encoding="utf-8") as f:
    face_embeddings = json.load(f)

# Initialize imgbeddings
ibed = imgbeddings()

class MainWindow(QMainWindow, Ui_MainWindow_List):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.set_logo("./amaLogo.png")

        self.caps = [
            cv2.VideoCapture(0),
            cv2.VideoCapture(""),
        ]

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frames)
        self.timer.start(60)

        self.log_model = QStringListModel()
        self.listView.setModel(self.log_model)
        self.log_list = []
        self.last_logged_time = {}
        self.start_time = time.time()
        self.frame_count = 0

        # Initialize MediaPipe Face Mesh
        self.face_mesh = mp_face_mesh.FaceMesh(max_num_faces=10, min_detection_confidence=0.5, min_tracking_confidence=0.5)

        # Initialize CSV logging
        self.csv_file_path = "face_detection_logs.csv"
        self.initialize_csv_log()

    def update_frames(self):
        frames = [cap.read()[1] for cap in self.caps]
        
        for i, frame in enumerate(frames):
            if frame is not None:
                camera_label = f"camera_{i}"
                self.process_frame(frame, self.camera_0, camera_label)
        
        self.frame_count += 1
        elapsed_time = time.time() - self.start_time
        if elapsed_time > 1.0:
            fps = self.frame_count / elapsed_time
            self.setWindowTitle(f"Face Recognition - FPS: {fps:.2f}")
            self.start_time = time.time()
            self.frame_count = 0

    def process_frame(self, frame, label, camera_label):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Get bounding box from landmarks
                h, w, _ = frame.shape
                x_min = int(min([landmark.x for landmark in face_landmarks.landmark]) * w)
                x_max = int(max([landmark.x for landmark in face_landmarks.landmark]) * w)
                y_min = int(min([landmark.y for landmark in face_landmarks.landmark]) * h)
                y_max = int(max([landmark.y for landmark in face_landmarks.landmark]) * h)

                # Ensure the bounding box is within the frame
                x_min, y_min = max(0, x_min), max(0, y_min)
                x_max, y_max = min(w, x_max), min(h, y_max)

                # Check if the face region is valid
                if x_min < x_max and y_min < y_max:
                    # Extract face image
                    face_img = frame[y_min:y_max, x_min:x_max]
                    
                    # Check if face_img is not empty
                    if face_img.size > 0:
                        pil_img = Image.fromarray(cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB))
                        embedding = ibed.to_embeddings(pil_img)[0]

                        name = self.recognize_face(embedding)

                        # Draw bounding box and name
                        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                        cv2.rectangle(frame, (x_min, y_min-40), (x_max, y_min), (0, 255, 0), -1)
                        cv2.putText(frame, name, (x_min, y_min-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

                        if name not in ["Unknown", "Loading"]:
                            self.log_face_detection(camera_label, name)

        self.display_frame(frame, label)

    def display_frame(self, frame, label):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

        scaled_qt_image = qt_image.scaled(label.size(), Qt.AspectRatioMode.KeepAspectRatio)
        label.setPixmap(QPixmap.fromImage(scaled_qt_image))

    def recognize_face(self, embedding):
        min_distance = float('inf')
        recognized_name = "unknown"

        for name, stored_embedding in face_embeddings.items():
            distance = np.linalg.norm(np.array(embedding) - np.array(stored_embedding))
            if distance < min_distance:
                min_distance = distance
                recognized_name = name

        if min_distance > 10 and min_distance < 12: # Adjust this threshold as needed
            recognized_name = "Loading"
        elif min_distance > 12:
            recognized_name  = "Unknown"

        return recognized_name

    def log_face_detection(self, cam_label, name):
        current_time = time.time()
        if name not in self.last_logged_time or (current_time - self.last_logged_time[name]) >= 60: # 900 seconds = 15 minutes
            self.last_logged_time[name] = current_time
            self.add_log_entry(name, cam_label)

    def add_log_entry(self, name, cam_label):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - Face detected on {cam_label}: {name}"
        self.log_list.append(log_entry)
        self.log_model.setStringList(self.log_list)
        self.listView.scrollToBottom()
        self.log_to_csv(timestamp, cam_label, name)

    def initialize_csv_log(self):
        if not os.path.exists(self.csv_file_path):
            with open(self.csv_file_path, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['Timestamp', 'Camera', 'Name'])

    def log_to_csv(self, timestamp, camera, name):
        with open(self.csv_file_path, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([timestamp, camera, name])

    def closeEvent(self, event):
        for cap in self.caps:
            cap.release()
        self.face_mesh.close()

def main_camera():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main_camera()
