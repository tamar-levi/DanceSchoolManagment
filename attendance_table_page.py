import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QPushButton, QMessageBox
import os

class AttendanceTablePage(QWidget):
    def __init__(self, stacked_widget, group, date):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.group = group
        self.date = date
        self.checkboxes = {}
        self.students = self.load_students()
        self.attendance_data = self.load_attendance()
        self.init_ui()

    def load_students(self):
        with open("data/students.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return [s for s in data["students"] if s["group"] == self.group["name"]]

    def load_attendance(self):
        path = f"attendances/attendance_{self.group['id']}.json"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_attendance(self):
        directory = "attendances"
        if not os.path.exists(directory):
            os.makedirs(directory)

        path = f"attendances/attendance_{self.group['id']}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.attendance_data, f, ensure_ascii=False, indent=2)

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"נוכחות - {self.group['name']} בתאריך {self.date}"))

        date_data = self.attendance_data.get(self.date, {})

        for student in self.students:
            cb = QCheckBox(student["name"])
            cb.setChecked(date_data.get(student["name"], False))
            layout.addWidget(cb)
            self.checkboxes[student["name"]] = cb

        save_btn: QPushButton = QPushButton("שמור נוכחות")
        save_btn.clicked.connect(self.save_attendance_data)
        layout.addWidget(save_btn)

        back_btn: QPushButton = QPushButton("חזרה לתאריכים")
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def save_attendance_data(self):
        self.attendance_data[self.date] = {
            name: cb.isChecked() for name, cb in self.checkboxes.items()
        }
        self.save_attendance()
        QMessageBox.information(self, "הצלחה", "הנוכחות נשמרה בהצלחה")

    def go_back(self):
        self.stacked_widget.setCurrentIndex(2)
