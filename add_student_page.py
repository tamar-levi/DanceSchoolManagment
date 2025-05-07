# add_student_page.py
import json
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QDateEdit, QMessageBox
from PyQt5.QtCore import QDate

class AddStudentPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("הוסף תלמידה"))

        # שם תלמידה
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("הכנס שם תלמידה")
        layout.addWidget(self.name_input)

        # טלפון
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("הכנס מספר פלאפון")
        layout.addWidget(self.phone_input)

        # שדה ID
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("הכנס מספר תעודת זהות")
        layout.addWidget(self.id_input)

        # קבוצה
        self.group_input = QComboBox()
        self.load_groups()
        layout.addWidget(self.group_input)

        # סטטוס תשלום
        self.payment_status_input = QComboBox()
        self.payment_status_input.addItems(["חוב", "יתרת זכות", "שולם"])
        layout.addWidget(self.payment_status_input)

        # תאריך הצטרפות
        self.join_date_input = QDateEdit()
        self.join_date_input.setDate(QDate.currentDate())
        self.join_date_input.setDisplayFormat("dd/MM/yyyy")
        layout.addWidget(self.join_date_input)

        # כפתור הוספה
        add_button = QPushButton("הוסף תלמידה")
        add_button.clicked.connect(self.add_student)
        layout.addWidget(add_button)

        # כפתור חזרה
        back_btn = QPushButton("⬅ חזרה לעמוד הקבוצות")
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn)

    def load_groups(self):
        try:
            with open("data/groups.json", encoding="utf-8") as f:
                data = json.load(f)
                groups = data.get("groups", [])
                group_names = [group["name"] for group in groups]
                self.group_input.addItems(group_names)
        except Exception as e:
            print(f"Error loading groups: {e}")
            self.group_input.addItem("Error loading groups")

    def add_student(self):
        student_id = self.id_input.text().strip()
        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        group = self.group_input.currentText().strip()
        payment_status = self.payment_status_input.currentText().strip()
        join_date = self.join_date_input.text().strip()

        # בדיקת שדות חובה
        if not student_id or not name or not phone or not group or not payment_status or not join_date:
            QMessageBox.warning(self, "שגיאה", "אנא מלא/י את כל השדות לפני הוספת תלמידה.")
            return

        print(f"הוספת תלמידה: {student_id}, {name}, {phone}, {group}, {payment_status}, {join_date}")

        try:
            with open("data/students.json", encoding="utf-8") as f:
                students_data = json.load(f)
            students_data["students"].append({
                "id": student_id,
                "name": name,
                "phone": phone,
                "group": group,
                "payment_status": payment_status,
                "join_date": join_date
            })
            with open("data/students.json", "w", encoding="utf-8") as f:
                json.dump(students_data, f, ensure_ascii=False, indent=4)
                self.go_back()
        except Exception as e:
            print(f"שגיאה בשמירת הנתונים: {e}")
            QMessageBox.critical(self, "שגיאה", f"שגיאה בשמירת הנתונים: {e}")

    def go_back(self):
        self.parent().setCurrentIndex(0)
