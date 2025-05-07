import json
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QListWidget, QInputDialog
import os

class GroupAttendancePage(QWidget):
    def __init__(self, stacked_widget, group):
        super().__init__()
        self.date_list = None
        self.stacked_widget = stacked_widget
        self.group = group
        self.attendance_data = {}
        self.load_attendance()
        self.init_ui()

    def load_attendance(self):
        path = f"attendances/attendance_{self.group['id']}.json"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self.attendance_data = json.load(f)
        else:
            self.attendance_data = {}

    def save_attendance(self):
        path = f"attendances/attendance_{self.group['id']}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.attendance_data, f, ensure_ascii=False, indent=2)

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"ניהול נוכחות - {self.group['name']}"))

        self.date_list: QPushButton = QListWidget()
        for date in self.attendance_data.keys():
            self.date_list.addItem(date)
        self.date_list.itemClicked.connect(self.open_date_attendance)
        layout.addWidget(self.date_list)

        add_date_btn: QPushButton = QPushButton("הוסף תאריך חדש")
        add_date_btn.clicked.connect(self.add_new_date)
        layout.addWidget(add_date_btn)

        back_btn: QPushButton = QPushButton("חזרה לקבוצות")
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def add_new_date(self):
        date, ok = QInputDialog.getText(self, "הוסף תאריך", "הכנס תאריך (למשל 07/05/2025):")
        if ok and date:
            if date not in self.attendance_data:
                self.attendance_data[date] = {}
                self.save_attendance()
                self.date_list.addItem(date)

    def open_date_attendance(self, item):
        from attendance_table_page import AttendanceTablePage
        page = AttendanceTablePage(self.stacked_widget, self.group, item.text())
        self.stacked_widget.addWidget(page)
        self.stacked_widget.setCurrentWidget(page)

    def go_back(self):
        self.stacked_widget.setCurrentIndex(2)
