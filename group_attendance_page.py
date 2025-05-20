import json
import os
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QListWidget, QInputDialog, QMessageBox

class GroupAttendancePage(QWidget):
    def __init__(self, stacked_widget, group):
        super().__init__()
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
        os.makedirs("attendances", exist_ok=True)
        path = f"attendances/attendance_{self.group['id']}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.attendance_data, f, ensure_ascii=False, indent=2)

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"ניהול נוכחות - {self.group['name']}"))

        self.date_list = QListWidget()
        for date in self.attendance_data.keys():
            self.date_list.addItem(date)
        self.date_list.itemClicked.connect(self.open_date_attendance)
        layout.addWidget(self.date_list)

        add_date_btn = QPushButton("הוסף תאריך חדש")
        add_date_btn.clicked.connect(self.add_new_date)
        layout.addWidget(add_date_btn)

        back_btn = QPushButton("חזרה לקבוצות")
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
        full_group = self.get_full_group_by_id(self.group["id"])
        if not full_group or not full_group.get("students"):
            QMessageBox.warning(self, "שגיאה", "לא נמצאה קבוצה עם תלמידות.")
            return

        page = AttendanceTablePage(self.go_back, full_group, item.text())
        self.stacked_widget.addWidget(page)
        self.stacked_widget.setCurrentWidget(page)

    def get_full_group_by_id(self, group_id):
        print("טוען קבוצה לפי group_id:", group_id)

        group = None
        if os.path.exists("data/groups.json"):
            print("קובץ groups.json קיים.")
            with open("data/groups.json", "r", encoding="utf-8") as f:
                groups_data = json.load(f)
                for g in groups_data.get("groups", []):
                    print("בודק קבוצה:", g["name"], "| id:", g["id"])
                    if str(g["id"]) == str(group_id):
                        group = g
                        print("נמצאה קבוצה מתאימה:", group)
                        break
        else:
            print("קובץ groups.json לא קיים!")

        if not group:
            print("לא נמצאה קבוצה עם id:", group_id)
            return None

        students = []
        if os.path.exists("data/students.json"):
            print("קובץ students.json קיים.")
            with open("data/students.json", "r", encoding="utf-8") as f:
                students_data = json.load(f)
                for s in students_data.get("students", []):
                    print("בודק תלמידה:", s["name"], "| שייכת לקבוצה:", s.get("group"))
                    if s.get("group", "").strip() == group["name"].strip():
                        print("נוספה תלמידה:", s["name"])
                        students.append({"id": s["id"], "name": s["name"]})
        else:
            print("קובץ students.json לא קיים!")

        print("מספר תלמידות שנמצאו:", len(students))
        group["students"] = students
        return group

    def go_back(self):
        self.stacked_widget.setCurrentIndex(2)
