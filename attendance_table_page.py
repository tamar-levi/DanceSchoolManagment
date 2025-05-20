import os
import json
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QScrollArea, QCheckBox, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from datetime import datetime


class AttendanceTablePage(QWidget):
    def __init__(self, navigate_back, group):
        super().__init__()
        self.navigate_back = navigate_back
        self.group = group
        self.attendance_data = {}

        self.init_ui()
        self.load_attendance()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel(f"רשימת נוכחות - {self.group['name']}")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.attendance_layout = QVBoxLayout()
        self.load_attendance_table()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_content.setLayout(self.attendance_layout)
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)

        add_date_btn = QPushButton("הוסף תאריך נוכחות")
        add_date_btn.clicked.connect(self.add_attendance_date)
        layout.addWidget(add_date_btn)

        back_btn = QPushButton("חזרה")
        back_btn.clicked.connect(self.navigate_back)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def load_attendance(self):
        path = f"attendances/attendance_{self.group['id']}.json"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self.attendance_data = json.load(f)

    def save_attendance(self):
        os.makedirs("attendances", exist_ok=True)  # ✅ יוצר את התיקייה אם לא קיימת
        path = f"attendances/attendance_{self.group['id']}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.attendance_data, f, ensure_ascii=False, indent=2)

    def load_attendance_table(self):
        for date, students in self.attendance_data.items():
            date_label = QLabel(date)
            date_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
            self.attendance_layout.addWidget(date_label)

            for student in students:
                student_card = self.create_student_card(student)
                self.attendance_layout.addWidget(student_card)

            line = QFrame()
            line.setFrameShape(QFrame.Shape.HLine)
            line.setFrameShadow(QFrame.Shadow.Sunken)
            self.attendance_layout.addWidget(line)

    def add_attendance_date(self):
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.attendance_data[date] = self.group["students"]
        self.save_attendance()

        # ננקה את התצוגה ונבנה מחדש עם התאריך החדש
        for i in reversed(range(self.attendance_layout.count())):
            widget = self.attendance_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.load_attendance_table()

    def create_student_card(self, student):
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        name_label = QLabel(student["name"])
        name_label.setFont(QFont("Arial", 12))

        checkbox = QCheckBox()
        checkbox.setChecked(True)

        layout.addWidget(name_label)
        layout.addWidget(checkbox)

        widget.setLayout(layout)
        widget.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                padding: 10px;
                border-radius: 10px;
                margin-bottom: 5px;
            }
        """)

        return widget
