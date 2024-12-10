import cv2
import sys
import base64
import requests
import mediapipe as mp
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap

class FaceDetectionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_detection = self.mp_face_detection.FaceDetection(min_detection_confidence=0.5)
        self.cameras = self.get_available_cameras()
        self.current_camera = 0
        self.cap = cv2.VideoCapture(self.current_camera)
        self.captured_images = []
        self.image_count = 0
        self.image_limit = 100
        self.initUI()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
        
    def get_available_cameras(self):
        camera_indices = []
        for i in range(10): # Check first 10 indices
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                camera_indices.append(i)
                cap.release()
        return camera_indices

    def initUI(self):
        self.setWindowTitle('Face Detection App')
        self.setGeometry(100, 100, 400, 500)
        
        layout = QVBoxLayout()
        
        self.image_label = QLabel(self)
        layout.addWidget(self.image_label)
        
        self.count_label = QLabel(f'Captured Images: 0 / {self.image_limit}', self)
        layout.addWidget(self.count_label)
        
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText('Enter your name')
        layout.addWidget(self.name_input)
        
        self.usn_input = QLineEdit(self)
        self.usn_input.setPlaceholderText('Enter your student number')
        layout.addWidget(self.usn_input)
        
        button_layout = QHBoxLayout()
        
        self.submit_button = QPushButton('Submit', self)
        self.submit_button.clicked.connect(self.submit_data)
        button_layout.addWidget(self.submit_button)
        
        self.reset_button = QPushButton('Reset', self)
        self.reset_button.clicked.connect(self.reset_form)
        button_layout.addWidget(self.reset_button)
        
        layout.addLayout(button_layout)
        
        self.camera_combo = QComboBox(self)
        self.camera_combo.addItems([f"Camera {i}" for i in self.cameras])
        self.camera_combo.currentIndexChanged.connect(self.switch_camera)
        layout.addWidget(self.camera_combo)
        
        self.setLayout(layout)
        
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_detection.process(frame_rgb)
            
            if results.detections:
                for detection in results.detections:
                    bboxC = detection.location_data.relative_bounding_box
                    ih, iw, _ = frame.shape
                    x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                                 int(bboxC.width * iw), int(bboxC.height * ih)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    if self.image_count < self.image_limit:
                        self.capture_image(frame)
            
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            p = convert_to_Qt_format.scaled(400, 300, Qt.KeepAspectRatio)
            self.image_label.setPixmap(QPixmap.fromImage(p))
    
    def capture_image(self, frame):
        _, buffer = cv2.imencode('.png', frame)
        encoded_string = base64.b64encode(buffer).decode('utf-8')
        self.captured_images.append(encoded_string)
        self.image_count += 1
        self.count_label.setText(f'Captured Images: {self.image_count} / {self.image_limit}')
    
    def submit_data(self):
        name = self.name_input.text()
        usn = self.usn_input.text()
        
        if not name or not usn:
            print("Please enter both name and student number.")
            return
        
        data = {
            "name": name,
            "usn": int(usn),
            "images": self.captured_images
        }
        
        server_url = "http://localhost:3000/api/submit" # Replace with your server details
        
        try:
            response = requests.post(server_url, json=data)
            if response.status_code == 200:
                print("Data sent successfully!")
            else:
                print(f"Failed to send data. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def reset_form(self):
        self.name_input.clear()
        self.usn_input.clear()
        self.captured_images = []
        self.image_count = 0
        self.count_label.setText(f'Captured Images: 0 / {self.image_limit}')

    def switch_camera(self, index):
        self.cap.release()
        self.current_camera = self.cameras[index]
        self.cap = cv2.VideoCapture(self.current_camera)

    def closeEvent(self, event):
        self.cap.release()
        self.face_detection.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FaceDetectionApp()
    ex.show()
    sys.exit(app.exec_())