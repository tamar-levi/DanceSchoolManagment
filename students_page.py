import json
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QFrame,
    QLineEdit, QHBoxLayout, QMessageBox, QFormLayout, QScrollArea
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from add_student_page import AddStudentPage


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

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        container_widget = QWidget()
        scroll_area.setWidget(container_widget)

        container_layout = QVBoxLayout()
        container_widget.setLayout(container_layout)

        container_layout.addWidget(QLabel(f"📚 תלמידות בקבוצה: {self.group_name}"))

        try:
            with open("data/students.json", encoding="utf-8") as f:
                students = json.load(f).get("students", [])
        except Exception as e:
            container_layout.addWidget(QLabel("שגיאה בטעינת התלמידות"))
            print("Error:", e)
            return

        self.current_students = [s for s in students if s.get("group") == self.group_name]

        if not self.current_students:
            container_layout.addWidget(QLabel("אין תלמידות בקבוצה זו"))
        else:
            for student in self.current_students:
                card = self.create_student_card(student)
                container_layout.addWidget(card)

        self.layout.addWidget(scroll_area)

        add_student_btn: QPushButton = QPushButton("➕ הוסף תלמידה")
        add_student_btn.clicked.connect(self.go_to_add_student_page)
        self.layout.addWidget(add_student_btn)

        back_btn: QPushButton = QPushButton("⬅ חזרה לרשימת הקבוצות")
        back_btn.clicked.connect(self.go_back)
        self.layout.addWidget(back_btn)

    def create_student_card(self, student):
        card = QFrame()
        card.setStyleSheet("""
            background-color: #ffffff;
            border-radius: 12px;
            margin: 10px;
            padding: 15px;
        """)
        card.setFrameShape(QFrame.StyledPanel)

        layout = QVBoxLayout()
        card.setLayout(layout)

        icon_label = QLabel()
        pixmap = QPixmap("path_to_icon.png")
        if not pixmap.isNull():
            icon_label.setPixmap(pixmap.scaled(50, 50, Qt.KeepAspectRatio))
            layout.addWidget(icon_label, alignment=Qt.AlignCenter)

        layout.addWidget(QLabel(f"👤 שם: {student['name']}"))
        layout.addWidget(QLabel(f"📞 טלפון: {student['phone']}"))
        layout.addWidget(QLabel(f"👥 קבוצה: {student['group']}"))
        layout.addWidget(QLabel(f"💰 סטטוס תשלום: {student['payment_status']}"))
        layout.addWidget(QLabel(f"📅 תאריך הצטרפות: {student['join_date']}"))

        button_layout = QHBoxLayout()
        edit_btn: QPushButton = QPushButton("עריכה")
        delete_btn: QPushButton = QPushButton("מחיקה")
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        layout.addLayout(button_layout)

        edit_btn.clicked.connect(lambda: self.edit_single_student(student))
        delete_btn.clicked.connect(lambda: self.confirm_delete(student['name']))

        return card

    def confirm_delete(self, student_name):
        reply = QMessageBox.question(
            self,
            "אישור מחיקה",
            f"האם למחוק את התלמידה '{student_name}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.delete_student(student_name)

    def edit_single_student(self, student):
        self.clear_layout()

        form_layout = QFormLayout()

        name_edit = QLineEdit(student['name'])
        phone_edit = QLineEdit(student['phone'])
        group_edit = QLineEdit(student['group'])
        payment_edit = QLineEdit(student['payment_status'])
        join_edit = QLineEdit(student['join_date'])

        form_layout.addRow("שם:", name_edit)
        form_layout.addRow("טלפון:", phone_edit)
        form_layout.addRow("קבוצה:", group_edit)
        form_layout.addRow("סטטוס תשלום:", payment_edit)
        form_layout.addRow("תאריך הצטרפות:", join_edit)

        self.layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        save_btn: QPushButton = QPushButton("שמור")
        cancel_btn: QPushButton = QPushButton("ביטול")
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        self.layout.addLayout(btn_layout)

        save_btn.clicked.connect(lambda: self.save_student(
            original_name=student['name'],
            new_data={
                "name": name_edit.text().strip(),
                "phone": phone_edit.text().strip(),
                "group": group_edit.text().strip(),
                "payment_status": payment_edit.text().strip(),
                "join_date": join_edit.text().strip()
            }
        ))
        cancel_btn.clicked.connect(self.show_students)

    def save_student(self, original_name, new_data):
        if not all(new_data.values()):
            QMessageBox.warning(self, "שגיאה", "יש למלא את כל השדות.")
            return

        try:
            with open("data/students.json", encoding="utf-8") as f:
                data = json.load(f)
                students = data.get("students", [])

            for i, student in enumerate(students):
                if student['name'] == original_name:
                    students[i] = new_data
                    break

            with open("data/students.json", 'w', encoding="utf-8") as f:
                json.dump({"students": students}, f, ensure_ascii=False, indent=4)

            self.show_students()
        except Exception as e:
            print(f"שגיאה בשמירה: {e}")

    def delete_student(self, student_name):
        try:
            with open("data/students.json", encoding="utf-8") as f:
                data = json.load(f)
                students = data.get("students", [])

            updated_students = [s for s in students if s['name'] != student_name]

            with open("data/students.json", 'w', encoding="utf-8") as f:
                json.dump({"students": updated_students}, f, ensure_ascii=False, indent=4)

            self.show_students()
        except Exception as e:
            print(f"שגיאה במחיקה: {e}")

    def go_back(self):
        self.stacked_widget.setCurrentIndex(1)

    def go_to_add_student_page(self):
        add_page = AddStudentPage(self.stacked_widget, self.group_name)
        self.stacked_widget.insertWidget(4, add_page)
        self.stacked_widget.setCurrentWidget(add_page)

    def clear_layout(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            elif item.layout():
                self.clear_inner_layout(item.layout())

    def clear_inner_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            elif item.layout():
                self.clear_inner_layout(item.layout())
