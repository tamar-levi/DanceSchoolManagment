import json
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from students_page import StudentsPage

class GroupsPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.build_group_buttons()

    def build_group_buttons(self):
        self.clear_layout()
        self.layout.addWidget(QLabel("בחרי קבוצה:"))

        try:
            with open("data/groups.json", encoding="utf-8") as f:
                data = json.load(f)
                groups = data.get("groups", [])
        except Exception as e:
            groups = []
            self.layout.addWidget(QLabel("Error loading groups"))
            print("Error reading JSON file:", e)

        for group_name in groups:
            btn: QPushButton =  QPushButton(group_name["name"])
            btn.setStyleSheet("background-color: #f8bbd0; padding: 8px; font-size: 14px;")
            btn.clicked.connect(lambda _, name=group_name["name"]: self.show_students(name))
            self.layout.addWidget(btn)

        back_btn: QPushButton = QPushButton("חזרה לעמוד הראשי")
        back_btn.clicked.connect(self.go_home)
        self.layout.addWidget(back_btn)

        add_student_button: QPushButton = QPushButton("הוסף תלמידה")
        add_student_button.clicked.connect(self.add_student_page)
        self.layout.addWidget(add_student_button)

    def show_students(self, group_name):
        students_page = StudentsPage(self.stacked_widget, group_name)
        self.stacked_widget.addWidget(students_page)
        self.stacked_widget.setCurrentWidget(students_page)

    def go_home(self):
        self.stacked_widget.setCurrentIndex(0)

    def add_student_page(self):
        self.stacked_widget.setCurrentIndex(4)

    def clear_layout(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
