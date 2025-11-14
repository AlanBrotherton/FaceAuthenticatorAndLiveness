import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QTextEdit,
    QVBoxLayout, QHBoxLayout, QFileDialog, QSizePolicy, QMessageBox
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

from save_face import save_face_from_image
from verify_face import verify_face
from liveness_check import liveness_check

# Clear saved face data and preview image at startup
for file in ["saved_face.npy", "saved_face_preview.jpg"]:
    if os.path.exists(file):
        os.remove(file)

# Define constants for file paths
SAVE_PATH = "saved_face.npy"
PREVIEW_IMAGE_PATH = "saved_face_preview.jpg"

class FaceAuthApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Face Authentication")
        self.setup_ui()

    def setup_ui(self):
        # Title
        self.title = QLabel("Face Authentication and Liveness Application", self)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont("Arial", 18, QFont.Bold))

        # Buttons
        self.save_btn = QPushButton("Step 1: Upload and Save Face")
        self.auth_btn = QPushButton("Step 2: Authenticate")
        self.reset_btn = QPushButton("Reset")  # <-- Add this line
        self.quit_btn = QPushButton("Quit")

        self.save_btn.clicked.connect(self.step1_save)
        self.auth_btn.clicked.connect(self.step2_authenticate)
        self.reset_btn.clicked.connect(self.reset_app)  # <-- Add this line
        self.quit_btn.clicked.connect(QApplication.quit)

        # Preview
        self.preview = QLabel(self)
        self.preview.setAlignment(Qt.AlignCenter)
        self.preview.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.preview.setStyleSheet("border: 1px solid gray;")

        # Log
        self.log = QTextEdit(self)
        self.log.setReadOnly(True)

        # Layouts
        button_layout = QVBoxLayout()
        for btn in [self.save_btn, self.auth_btn, self.reset_btn, self.quit_btn]:  # <-- Add reset_btn here
            button_layout.addWidget(btn)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.preview)
        right_layout.addWidget(self.log)

        main_layout = QHBoxLayout()
        main_layout.addLayout(button_layout, 1)
        main_layout.addLayout(right_layout, 3)

        full_layout = QVBoxLayout()
        full_layout.addWidget(self.title)
        full_layout.addLayout(main_layout)

        self.setLayout(full_layout)
        self.update_preview()

        # Initial button states
        self.auth_btn.setEnabled(False)

    def log_msg(self, message):
        self.log.append(message)

    def update_preview(self):
        if os.path.exists(PREVIEW_IMAGE_PATH):
            pixmap = QPixmap(PREVIEW_IMAGE_PATH).scaled(
                self.preview.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.preview.setPixmap(pixmap)
        else:
            self.preview.clear()

    def step1_save(self):
        self.log_msg("Opening file dialog to upload image...")
        result = save_face_from_image()
        if result:
            self.log_msg("Face successfully saved.")
            self.update_preview()
            self.save_btn.setStyleSheet("background-color: green; color: white;")
            self.save_btn.setEnabled(False)
            self.auth_btn.setEnabled(True)
        else:
            self.log_msg("Face not saved. Try another image.")

    def step2_authenticate(self):
        if not os.path.exists(SAVE_PATH):
            self.log_msg("No saved face found. Complete Step 1 first.")
            return
        self.log_msg("Starting face verification...")
        verify_result = verify_face()
        if verify_result:
            self.log_msg("Face verified successfully.")
            self.log_msg("Starting liveness check...")
            liveness_result = liveness_check()
            if liveness_result:
                self.log_msg("Liveness check passed. User authenticated.")
                self.auth_btn.setStyleSheet("background-color: green; color: white;")
                self.auth_btn.setEnabled(False)
            else:
                self.log_msg("Liveness check failed.")
        else:
            self.log_msg("Face verification failed. Not a match.")

    def reset_app(self):
        # Remove saved files
        for file in [SAVE_PATH, PREVIEW_IMAGE_PATH]:
            if os.path.exists(file):
                os.remove(file)
        # Reset buttons
        self.save_btn.setEnabled(True)
        self.save_btn.setStyleSheet("")
        self.auth_btn.setEnabled(False)
        self.auth_btn.setStyleSheet("")
        # Clear preview and log
        self.preview.clear()
        self.log.clear()
        self.log_msg("App reset. Please start from Step 1.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FaceAuthApp()
    window.showMaximized()
    sys.exit(app.exec_())
