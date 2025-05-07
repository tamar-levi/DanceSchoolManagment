import json
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QFrame,
    QLineEdit, QHBoxLayout, QMessageBox, QFormLayout, QScrollArea
)
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
        add_student_btn.clicked.connect(self.show_add_student_form)
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
        payments_btn: QPushButton = QPushButton("💳 תשלומים")
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addWidget(payments_btn)
        layout.addLayout(button_layout)

        edit_btn.clicked.connect(lambda: self.edit_single_student(student))
        delete_btn.clicked.connect(lambda: self.confirm_delete(student['name']))
        payments_btn.clicked.connect(lambda: self.show_payments(student))

        return card

    def show_add_student_form(self):
        self.clear_layout()
        self.layout.addWidget(QLabel("➕ הוספת תלמידה חדשה"))

        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.payment_input = QLineEdit()
        self.join_input = QLineEdit()

        form_layout.addRow("שם:", self.name_input)
        form_layout.addRow("טלפון:", self.phone_input)
        form_layout.addRow("סטטוס תשלום:", self.payment_input)
        form_layout.addRow("תאריך הצטרפות", self.join_input)

        self.layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        save_btn: QPushButton = QPushButton("שמור")
        cancel_btn: QPushButton = QPushButton("ביטול")
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        self.layout.addLayout(button_layout)

        save_btn.clicked.connect(self.save_new_student)
        cancel_btn.clicked.connect(self.show_students)

    def save_new_student(self):
        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        payment_status = self.payment_input.text().strip()
        join_date = self.join_input.text().strip()

        if not name or not phone or not payment_status or not join_date:
            QMessageBox.warning(self, "שגיאה", "יש למלא את כל השדות.")
            return

        new_student = {
            "name": name,
            "phone": phone,
            "group": self.group_name,
            "payment_status": payment_status,
            "join_date": join_date
        }

        try:
            with open("data/students.json", encoding="utf-8") as f:
                data = json.load(f)
                students = data.get("students", [])
        except Exception:
            students = []

        students.append(new_student)

        try:
            with open("data/students.json", 'w', encoding="utf-8") as f:
                json.dump({"students": students}, f, ensure_ascii=False, indent=4)

            self.show_students()
        except Exception as e:
            print("Error saving new student:", e)

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

    def show_payments(self, student):
        self.clear_layout()

        self.layout.addWidget(QLabel(f"💳 תשלומים עבור {student['name']}"))

        try:
            payments = student.get('payments', [])
        except KeyError:
            payments = []

        if not payments:
            self.layout.addWidget(QLabel("לא נמצאו תשלומים לתלמידה זו"))

        for payment in payments:
            payment_info = f"סכום: {payment['amount']} | תאריך: {payment['date']} | אופן תשלום: {payment['payment_method']}"
            self.layout.addWidget(QLabel(payment_info))

        button_layout = QHBoxLayout()
        add_payment_btn: QPushButton = QPushButton("הוסף תשלום")
        back_btn: QPushButton = QPushButton("חזרה לתלמידות")
        button_layout.addWidget(add_payment_btn)
        button_layout.addWidget(back_btn)
        self.layout.addLayout(button_layout)

        add_payment_btn.clicked.connect(lambda: self.show_add_payment_form(student))
        back_btn.clicked.connect(self.show_students)

    def show_add_payment_form(self, student):
        self.clear_layout()

        self.layout.addWidget(QLabel(f"💳 הוספת תשלום עבור {student['name']}"))

        form_layout = QFormLayout()

        self.amount_input = QLineEdit()
        self.date_input = QLineEdit()
        self.payment_method_input = QLineEdit()

        form_layout.addRow("סכום:", self.amount_input)
        form_layout.addRow("תאריך:", self.date_input)
        form_layout.addRow("אופן תשלום:", self.payment_method_input)

        self.layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        save_btn: QPushButton = QPushButton("שמור")
        cancel_btn: QPushButton = QPushButton("ביטול")
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        self.layout.addLayout(button_layout)

        save_btn.clicked.connect(lambda: self.save_payment(student, {
            "amount": self.amount_input.text().strip(),
            "date": self.date_input.text().strip(),
            "payment_method": self.payment_method_input.text().strip()
        }))
        cancel_btn.clicked.connect(self.show_students)

    def save_payment(self, student, payment_data):
        if not all(payment_data.values()):
            QMessageBox.warning(self, "שגיאה", "יש למלא את כל השדות.")
            return

        try:
            # טען את תלמידות
            with open("data/students.json", encoding="utf-8") as f:
                data = json.load(f)
                students = data.get("students", [])

            # טען את הקבוצות (שבהן יש את המחירים)
            with open("data/groups.json", encoding="utf-8") as f:
                group_data = json.load(f)
                groups = group_data.get("groups", [])

            for s in students:
                if s['name'] == student['name']:
                    s.setdefault("payments", []).append(payment_data)

                    # סכום כולל ששולם
                    total_paid = sum(
                        float(p['amount']) for p in s['payments']
                        if p['amount'].replace('.', '', 1).isdigit()
                    )

                    # קבל שם קבוצה וחפש את המחיר שלה
                    group_name = s.get("group")
                    group = next((g for g in groups if g['name'] == group_name), None)

                    if group:
                        group_price = float(group.get("price", "0"))
                        if total_paid >= group_price:
                            s['payment_status'] = "שולם"
                        else:
                            s['payment_status'] = f"חוב: {group_price - total_paid}₪"
                    else:
                        s['payment_status'] = "לא נמצא מחיר קבוצה"

                    break

            # שמור את הקובץ
            with open("data/students.json", 'w', encoding="utf-8") as f:
                json.dump({"students": students}, f, ensure_ascii=False, indent=4)

            self.show_students()

        except Exception as e:
            print(f"שגיאה בשמירת תשלום: {e}")

    def go_back(self):
        self.stacked_widget.setCurrentIndex(1)

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
