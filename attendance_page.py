import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from group_attendance_page import GroupAttendancePage

def load_groups():
    try:
        with open("data/groups.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("groups", [])
    except Exception as e:
        print("שגיאה בטעינת קבוצות:", e)
        return []

class AttendancePage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def showEvent(self, event):
        super().showEvent(event)
        self.refresh()

    def refresh(self):
        self.clear_layout()
        groups = load_groups()

        title = QLabel("בחר קבוצה לניהול נוכחות")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        self.layout.addWidget(title)

        for group in groups:
            btn: QPushButton = QPushButton(group["name"])
            btn.setStyleSheet("background-color: #bbdefb; padding: 8px; font-size: 14px;")
            btn.clicked.connect(lambda _, g=group: self.show_group_attendance(g))
            self.layout.addWidget(btn)

        back_btn: QPushButton = QPushButton("⬅ חזרה לעמוד הראשי")
        back_btn.setStyleSheet("margin-top: 15px; background-color: #e0e0e0;")
        back_btn.clicked.connect(self.go_home)
        self.layout.addWidget(back_btn)

    def clear_layout(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def show_group_attendance(self, group):
        page = GroupAttendancePage(self.stacked_widget, group)
        self.stacked_widget.addWidget(page)
        self.stacked_widget.setCurrentWidget(page)

    def go_home(self):
        self.stacked_widget.setCurrentIndex(0)
