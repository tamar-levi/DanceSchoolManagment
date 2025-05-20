import json
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QDateEdit, QMessageBox, QComboBox
)
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QDateEdit, QMessageBox, QComboBox
)
from PyQt5.QtCore import QDate

class AddStudentPage(QWidget):
    def __init__(self, stacked_widget, group_name):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.group_name = group_name 

        self.stacked_widget = stacked_widget
        self.group_name = group_name

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("הוסף תלמידה"))

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("הכנס שם תלמידה")
        layout.addWidget(self.name_input)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("הכנס מספר פלאפון")
        layout.addWidget(self.phone_input)

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("הכנס מספר תעודת זהות")
        layout.addWidget(self.id_input)

        self.group_input = QComboBox()
        self.load_groups()
        layout.addWidget(self.group_input)

        self.payment_status_input = QComboBox()
        self.payment_status_input.addItems(["חוב", "יתרת זכות", "שולם"])
        layout.addWidget(QLabel("סטטוס תשלום"))
        layout.addWidget(QLabel("סטטוס תשלום"))
        layout.addWidget(self.payment_status_input)

        self.join_date_input = QDateEdit()
        self.join_date_input.setDate(QDate.currentDate())
        self.join_date_input.setDisplayFormat("dd/MM/yyyy")
        layout.addWidget(QLabel("תאריך הצטרפות"))
        layout.addWidget(QLabel("תאריך הצטרפות"))
        layout.addWidget(self.join_date_input)

        add_button = QPushButton("הוסף תלמידה")
        add_button.clicked.connect(self.add_student)
        layout.addWidget(add_button)

        back_btn = QPushButton("⬅ חזרה לעמוד הקבוצות")
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn)

    def add_student(self):
        student_id = self.id_input.text().strip()
        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        payment_status = self.payment_status_input.currentText().strip()
        join_date = self.join_date_input.text().strip()

        if not student_id or not name or not phone or not payment_status or not join_date:
            QMessageBox.warning(self, "שגיאה", "אנא מלא/י את כל השדות לפני הוספת תלמידה.")
            return

        try:
            with open("data/students.json", encoding="utf-8") as f:
                students_data = json.load(f)
        except FileNotFoundError:
            students_data = {"students": []}

        if "students" not in students_data or not isinstance(students_data["students"], list):
            students_data["students"] = []

        for student in students_data["students"]:
            if student.get("id") == student_id:
                QMessageBox.warning(self, "שגיאה", f"תלמידה עם ת.ז. {student_id} כבר קיימת.")
                return

        new_student = {
            "id": student_id,
            "name": name,
            "phone": phone,
            "group": self.group_name,
            "payment_status": payment_status,
            "join_date": join_date
        }

        students_data["students"].append(new_student)

        try:
            with open("data/students.json", 'w', encoding="utf-8") as f:
                json.dump(students_data, f, ensure_ascii=False, indent=4)
            QMessageBox.information(self, "הצלחה", "התלמידה נוספה בהצלחה!")
            self.go_back()
            QMessageBox.information(self, "הצלחה", "התלמידה נוספה בהצלחה!")
            self.go_back()
        except Exception as e:
            QMessageBox.critical(self, "שגיאה", f"שגיאה בשמירה: {e}")
            QMessageBox.critical(self, "שגיאה", f"שגיאה בשמירה: {e}")

    def go_back(self):
        self.stacked_widget.setCurrentIndex(0)
        self.stacked_widget.setCurrentIndex(0)
