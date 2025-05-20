import os
import json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QScrollArea, QCheckBox, QFrame,
    QGraphicsDropShadowEffect, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QTimer
from PyQt5.QtGui import QFont, QColor

class AnimatedCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.NoFrame)
        
        # Add shadow effect
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QColor(0, 0, 0, 30))
        self.shadow.setOffset(0, 4)
        self.setGraphicsEffect(self.shadow)
        
        self.setStyleSheet("""
            AnimatedCard {
                background-color: #ffffff;
                border-radius: 8px;
                border: none;
            }
        """)

class AttendanceTablePage(QWidget):
    def __init__(self, navigate_back, group, date):
        super().__init__()
        self.navigate_back = navigate_back
        self.group = group
        self.date = date
        self.attendance_data = {}
        
        # Set background color
        self.setStyleSheet("background-color: #f5f7fa;")
        
        self.init_ui()
        self.load_attendance()
        
        # Run entrance animation
        QTimer.singleShot(100, self.run_entrance_animation)

    def init_ui(self):
        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        self.setLayout(layout)
        
        # Header card
        header_card = AnimatedCard()
        header_layout = QVBoxLayout(header_card)
        
        # Title
        title = QLabel(f"רשימת נוכחות")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel(f"{self.group['name']} - {self.date}")
        subtitle.setFont(QFont("Segoe UI", 16))
        subtitle.setStyleSheet("color: #7f8c8d;")
        subtitle.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header_card)
        
        # Attendance list card
        attendance_card = AnimatedCard()
        attendance_layout = QVBoxLayout(attendance_card)
        attendance_layout.setContentsMargins(15, 15, 15, 15)
        attendance_layout.setSpacing(10)
        
        # Attendance list header
        header_widget = QWidget()
        header_widget.setStyleSheet("""
            QWidget {
                background-color: #3498db;
                border-radius: 6px;
                padding: 10px;
            }
        """)
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(15, 10, 15, 10)
        
        name_header = QLabel("שם התלמידה")
        name_header.setFont(QFont("Segoe UI", 12, QFont.Bold))
        name_header.setStyleSheet("color: white;")
        
        attendance_header = QLabel("נוכחות")
        attendance_header.setFont(QFont("Segoe UI", 12, QFont.Bold))
        attendance_header.setStyleSheet("color: white;")
        
        header_layout.addWidget(attendance_header)
        header_layout.addWidget(name_header, 1)  # Stretch factor to align right
        
        attendance_layout.addWidget(header_widget)
        
        # Scroll area for attendance list
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        scroll_content = QWidget()
        self.attendance_layout = QVBoxLayout(scroll_content)
        self.attendance_layout.setContentsMargins(0, 0, 0, 0)
        self.attendance_layout.setSpacing(8)
        
        scroll_area.setWidget(scroll_content)
        attendance_layout.addWidget(scroll_area)
        
        layout.addWidget(attendance_card)
        
        # Buttons card
        buttons_card = AnimatedCard()
        buttons_layout = QHBoxLayout(buttons_card)
        buttons_layout.setSpacing(15)
        
        # Save button
        save_btn = QPushButton("שמור נוכחות")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.clicked.connect(self.save_attendance)
        
        # Back button
        back_btn = QPushButton("חזרה")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.clicked.connect(self.navigate_back)
        
        buttons_layout.addWidget(save_btn)
        buttons_layout.addWidget(back_btn)
        
        layout.addWidget(buttons_card)
        
        # Store references to cards for animation
        self.cards = [header_card, attendance_card, buttons_card]

    def run_entrance_animation(self):
        for i, card in enumerate(self.cards):
            animation = QPropertyAnimation(card, b"pos")
            animation.setDuration(500)
            animation.setStartValue(card.pos() + QPoint(0, 50))
            animation.setEndValue(card.pos())
            animation.setEasingCurve(QEasingCurve.OutCubic)
            
            # Use QTimer to delay the start of animation
            QTimer.singleShot(i * 100, animation.start)

    def load_attendance(self):
        path = f"attendances/attendance_{self.group['id']}.json"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self.attendance_data = json.load(f)
        if self.date not in self.attendance_data:
            self.attendance_data[self.date] = {}
        self.load_attendance_table()

    def save_attendance(self):
        os.makedirs("attendances", exist_ok=True)
        for i in range(self.attendance_layout.count()):
            widget = self.attendance_layout.itemAt(i).widget()
            if isinstance(widget, QWidget):
                name_label = widget.findChild(QLabel)
                checkbox = widget.findChild(QCheckBox)
                if name_label and checkbox:
                    name = name_label.text()
                    student = next((s for s in self.group["students"] if s["name"] == name), None)
                    if student:
                        self.attendance_data[self.date][str(student["id"])] = checkbox.isChecked()

        path = f"attendances/attendance_{self.group['id']}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.attendance_data, f, ensure_ascii=False, indent=2)
            
        # Show animation feedback
        for i in range(self.attendance_layout.count()):
            widget = self.attendance_layout.itemAt(i).widget()
            if isinstance(widget, QWidget):
                animation = QPropertyAnimation(widget, b"styleSheet")
                animation.setDuration(500)
                animation.setStartValue(widget.styleSheet())
                animation.setEndValue("""
                    QWidget {
                        background-color: #d4edda;
                        padding: 10px;
                        border-radius: 10px;
                        margin-bottom: 5px;
                    }
                """)
                animation.start()
                
                # Reset style after animation
                QTimer.singleShot(1000, lambda w=widget: w.setStyleSheet("""
                    QWidget {
                        background-color: #f0f0f0;
                        padding: 10px;
                        border-radius: 10px;
                        margin-bottom: 5px;
                    }
                """))

    def load_attendance_table(self):
        for student in self.group["students"]:
            present = self.attendance_data.get(self.date, {}).get(str(student["id"]), False)
            student_card = self.create_student_card(student, present)
            self.attendance_layout.addWidget(student_card)

    def create_student_card(self, student, present):
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 5, 15, 5)
        
        name_label = QLabel(student["name"])
        name_label.setFont(QFont("Segoe UI", 12))
        name_label.setStyleSheet("color: #2c3e50;")
        
        checkbox = QCheckBox()
        checkbox.setStyleSheet("""
            QCheckBox {
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 2px solid #3498db;
            }
            QCheckBox::indicator:checked {
                background-color: #3498db;
                image: url(icons/checkmark.png);
            }
        """)
        checkbox.setChecked(present)
        
        layout.addWidget(checkbox)
        layout.addWidget(name_label, 1)  # Stretch factor to align right
        
        widget.setLayout(layout)
        widget.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                padding: 10px;
                border-radius: 10px;
                margin-bottom: 5px;
            }
            QWidget:hover {
                background-color: #e0e0e0;
            }
        """)
        
        return widget
