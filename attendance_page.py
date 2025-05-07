import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from group_attendance_page import GroupAttendancePage

def load_groups():
    with open("data/groups.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        return data["groups"]

def load_students(group_name):
    with open("data/students.json", "r", encoding="utf-8") as file:
        students = json.load(file)["students"]
        return [student for student in students if student["group"] == group_name]

def save_attendance(groups):
    with open("data/groups.json", "w", encoding="utf-8") as file:
        json.dump({"groups": groups}, file, ensure_ascii=False, indent=4)

class AttendancePage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.groups = load_groups()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("בחר קבוצה לניהול נוכחות"))

        for group in self.groups:
            btn: QPushButton = QPushButton(group["name"])
            btn.clicked.connect(lambda _, g=group: self.show_group_attendance(g))
            layout.addWidget(btn)

        back_btn: QPushButton = QPushButton("חזרה לעמוד הראשי")
        back_btn.clicked.connect(self.go_home)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def show_group_attendance(self, group):
        group_attendance_page = GroupAttendancePage(self.stacked_widget, group)
        self.stacked_widget.addWidget(group_attendance_page)
        self.stacked_widget.setCurrentWidget(group_attendance_page)

    def go_home(self):
        self.stacked_widget.setCurrentIndex(0)
