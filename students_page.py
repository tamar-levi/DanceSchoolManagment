import json
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QFrame
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class StudentsPage(QWidget):
    def __init__(self, stacked_widget, group_name):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.group_name = group_name
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.show_students()

    def show_students(self):
        self.clear_layout()
        self.layout.addWidget(QLabel(f"Students in {self.group_name}:"))

        try:
            with open("data/students.json", encoding="utf-8") as f:
                students = json.load(f).get("students", [])
        except Exception as e:
            self.layout.addWidget(QLabel("Error loading students"))
            print("Error:", e)
            return

        found = False
        for student in students:
            if student.get("group") == self.group_name:
                student_card = self.create_student_card(student)
                self.layout.addWidget(student_card)
                found = True

        if not found:
            self.layout.addWidget(QLabel("No students in this group"))

        back_btn: QPushButton = QPushButton("⬅ Back to group list")
        back_btn.clicked.connect(self.go_back)
        self.layout.addWidget(back_btn)

    def create_student_card(self, student):
        card = QFrame()
        card.setStyleSheet("""
            background-color: #ffffff; 
            border-radius: 12px; 
            margin: 10px; 
            padding: 15px; 
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        """)
        card.setFrameShape(QFrame.StyledPanel)

        student_layout = QVBoxLayout()
        card.setLayout(student_layout)

        icon_label = QLabel()
        pixmap = QPixmap("path_to_icon.png")
        icon_label.setPixmap(pixmap.scaled(50, 50, Qt.KeepAspectRatio))
        student_layout.addWidget(icon_label, alignment=Qt.AlignCenter)

        student_layout.addWidget(QLabel(f"Name: {student['name']}"))
        student_layout.addWidget(QLabel(f"Phone: {student['phone']}"))
        student_layout.addWidget(QLabel(f"Group: {student['group']}"))
        student_layout.addWidget(QLabel(f"Payment Status: {student['payment_status']}"))
        student_layout.addWidget(QLabel(f"Join Date: {student['join_date']}"))

        edit_btn = QPushButton("Edit")
        student_layout.addWidget(edit_btn)

        delete_btn: QPushButton = QPushButton("Delete")
        student_layout.addWidget(delete_btn)

        delete_btn.clicked.connect(lambda: self.delete_student(student['name']))

        return card

    def delete_student(self, student_name):
        try:
            with open("data/students.json", encoding="utf-8") as f:
                data = json.load(f)
                students = data.get("students", [])

            updated_students = [student for student in students if student['name'] != student_name]

            with open("data/students.json", 'w', encoding="utf-8") as f:
                json.dump({"students": updated_students}, f, ensure_ascii=False, indent=4)

            self.show_students()

        except Exception as e:
            print(f"Error deleting student: {e}")

    def go_back(self):
        self.stacked_widget.setCurrentIndex(1)

    def clear_layout(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

