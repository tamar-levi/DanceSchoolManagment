import os
import json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QScrollArea, QCheckBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class AttendanceTablePage(QWidget):
    def __init__(self, navigate_back, group, date):
        super().__init__()
        self.navigate_back = navigate_back
        self.group = group
        self.date = date
        self.attendance_data = {}
        self.init_ui()
        self.load_attendance()

    def init_ui(self):
        layout = QVBoxLayout()
        title = QLabel(f"רשימת נוכחות - {self.group['name']} - {self.date}")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.attendance_layout = QVBoxLayout()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_content.setLayout(self.attendance_layout)
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)

        save_btn = QPushButton("שמור נוכחות")
        save_btn.clicked.connect(self.save_attendance)
        layout.addWidget(save_btn)

        back_btn = QPushButton("חזרה")
        back_btn.clicked.connect(self.navigate_back)
        layout.addWidget(back_btn)

        self.setLayout(layout)

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

    def load_attendance_table(self):
        for student in self.group["students"]:
            present = self.attendance_data.get(self.date, {}).get(str(student["id"]), False)
            student_card = self.create_student_card(student, present)
            self.attendance_layout.addWidget(student_card)

    def create_student_card(self, student, present):
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignRight)

        name_label = QLabel(student["name"])
        name_label.setFont(QFont("Arial", 12))

        checkbox = QCheckBox()
        checkbox.setChecked(present)

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
