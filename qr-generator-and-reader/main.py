from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
    QFileDialog,
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import qrcode
import io
import cv2


# Store QR image globally so we can save it later
generated_qr_image = None


def generate_qrcode():
    global generated_qr_image

    url = entry_url.text()
    if not url:
        QMessageBox.critical(window, "Error", "Please enter a valid URL.")
        return

    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=5,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Create an image of the QR code
    qr_image = qr.make_image(fill_color="black", back_color="white")
    generated_qr_image = qr_image  # Save for download

    # Convert PIL Image to QPixmap
    buffer = io.BytesIO()
    qr_image.save(buffer, format="PNG")
    buffer.seek(0)
    pixmap = QPixmap()
    pixmap.loadFromData(buffer.getvalue())

    # Display the QR code in the application
    qr_label.setPixmap(pixmap)
    qr_result_label.setText("✅ QR code generated successfully!")
    download_button.setVisible(True)


def download_qrcode():
    global generated_qr_image

    if not generated_qr_image:
        QMessageBox.warning(window, "Warning", "No QR code to download.")
        return

    file_path, _ = QFileDialog.getSaveFileName(
        window, "Save QR Code", "qrcode.png", "PNG Files (*.png)"
    )

    if file_path:
        try:
            generated_qr_image.save(file_path, format="PNG")
            QMessageBox.information(window, "Saved", "QR code saved successfully.")
        except Exception as e:
            QMessageBox.critical(window, "Error", f"Failed to save QR code: {e}")


def read_qr_from_image():
    file_path, _ = QFileDialog.getOpenFileName(
        window, "Select a PNG image", "", "PNG Files (*.png)"
    )
    if not file_path:
        return

    img = cv2.imread(file_path)
    if img is None:
        QMessageBox.warning(window, "Error", "Failed to load the image.")
        return

    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(img)

    if data:
        qr_detected_label.setText(f"🔍 QR Code detected:\n{data}")
    else:
        qr_detected_label.setText("⚠️ No valid QR code detected.")


# Create the application and main window
app = QApplication([])
window = QWidget()
window.setWindowTitle("QR Code Utility")
window.setGeometry(100, 100, 450, 580)
window.setStyleSheet("background-color: #f0f4f7;")

# Layout
layout = QVBoxLayout()

# === Title ===
title_label = QLabel("🔧 QR Code Reader and Generator")
title_label.setFont(QFont("Helvetica", 16, QFont.Bold))
title_label.setAlignment(Qt.AlignCenter)
layout.addWidget(title_label)

# === Image QR Reader Section ===
image_section_label = QLabel("Upload a PNG image with a QR code")
image_section_label.setFont(QFont("Helvetica", 12))
image_section_label.setAlignment(Qt.AlignCenter)
layout.addWidget(image_section_label)

button_upload = QPushButton("Upload Image and Read QR")
button_upload.setFont(QFont("Helvetica", 11))
button_upload.setStyleSheet(
    "QPushButton { background-color: #28a745; color: white; padding: 6px; }"
    "QPushButton:pressed { background-color: #1e7e34; }"
)
button_upload.clicked.connect(read_qr_from_image)
layout.addWidget(button_upload)

qr_detected_label = QLabel("")
qr_detected_label.setFont(QFont("Helvetica", 11))
qr_detected_label.setAlignment(Qt.AlignCenter)
qr_detected_label.setStyleSheet("color: #333; background-color: #f0f4f7;")
qr_detected_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
qr_detected_label.setCursor(Qt.IBeamCursor)
layout.addWidget(qr_detected_label)

# === QR Code Generator Section ===
generator_section_label = QLabel("Enter a URL to generate a QR code")
generator_section_label.setFont(QFont("Helvetica", 12))
generator_section_label.setAlignment(Qt.AlignCenter)
layout.addWidget(generator_section_label)

entry_url = QLineEdit()
entry_url.setFont(QFont("Helvetica", 12))
entry_url.setPlaceholderText("https://example.com")
layout.addWidget(entry_url)

button_generate = QPushButton("Generate QR Code")
button_generate.setFont(QFont("Helvetica", 12))
button_generate.setStyleSheet(
    "QPushButton { background-color: #007bff; color: white; padding: 6px; }"
    "QPushButton:pressed { background-color: #0056b3; }"
)
button_generate.clicked.connect(generate_qrcode)
layout.addWidget(button_generate)

qr_label = QLabel()
qr_label.setAlignment(Qt.AlignCenter)
qr_label.setStyleSheet("background-color: #f0f4f7;")
layout.addWidget(qr_label)

qr_result_label = QLabel("")
qr_result_label.setFont(QFont("Helvetica", 12))
qr_result_label.setAlignment(Qt.AlignCenter)
qr_result_label.setStyleSheet("color: #333; background-color: #f0f4f7;")
layout.addWidget(qr_result_label)

# Download Button (initially hidden)
download_button = QPushButton("⬇️ Download QR Code")
download_button.setFont(QFont("Helvetica", 11))
download_button.setStyleSheet(
    "QPushButton { background-color: #17a2b8; color: white; padding: 5px; }"
    "QPushButton:pressed { background-color: #117a8b; }"
)
download_button.setVisible(False)
download_button.clicked.connect(download_qrcode)
layout.addWidget(download_button)

# Finalize layout
window.setLayout(layout)
window.show()
app.exec_()
