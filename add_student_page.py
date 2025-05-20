import json
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QDateEdit, QMessageBox, QComboBox,
    QHBoxLayout, QFrame, QGraphicsDropShadowEffect, QSizePolicy
)
from PyQt5.QtCore import Qt, QDate, QPropertyAnimation, QEasingCurve, QPoint, QTimer
from PyQt5.QtGui import QColor, QFont


class AnimatedCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.NoFrame)

        # Add shadow effect
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QColor(0, 0, 0, 30))
        self.shadow.setOffset(0, 4)
        self.setGraphicsEffect(self.shadow)

        self.setStyleSheet("""
            AnimatedCard {
                background-color: #ffffff;
                border-radius: 8px;
                border: none;
            }
        """)


class AddStudentPage(QWidget):
    def __init__(self, stacked_widget, group_name):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.group_name = group_name

        # Set background color
        self.setStyleSheet("background-color: #f5f7fa;")

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        self.setLayout(main_layout)

        # Title card
        title_card = AnimatedCard()
        title_layout = QVBoxLayout(title_card)

        title_label = QLabel("הוספת תלמידה חדשה")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        title_label.setAlignment(Qt.AlignCenter)

        subtitle_label = QLabel(f"לקבוצת {group_name}")
        subtitle_label.setStyleSheet("font-size: 16px; color: #7f8c8d;")
        subtitle_label.setAlignment(Qt.AlignCenter)

        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)

        main_layout.addWidget(title_card)

        # Form card
        form_card = AnimatedCard()
        form_layout = QVBoxLayout(form_card)
        form_layout.setSpacing(15)

        # Input fields style
        input_style = """
            QLineEdit, QComboBox, QDateEdit {
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #e0e0e0;
                background-color: #f9f9f9;
                font-size: 14px;
                min-height: 20px;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border: 1px solid #3498db;
                background-color: #ffffff;
            }
        """

        # Name input
        name_label = QLabel("שם התלמידה:")
        name_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("הכנס שם תלמידה")
        self.name_input.setStyleSheet(input_style)
        self.name_input.setAlignment(Qt.AlignRight)
        form_layout.addWidget(name_label)
        form_layout.addWidget(self.name_input)

        # Phone input
        phone_label = QLabel("מספר טלפון:")
        phone_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("הכנס מספר פלאפון")
        self.phone_input.setStyleSheet(input_style)
        self.phone_input.setAlignment(Qt.AlignRight)
        form_layout.addWidget(phone_label)
        form_layout.addWidget(self.phone_input)

        # ID input
        id_label = QLabel("תעודת זהות:")
        id_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("הכנס מספר תעודת זהות")
        self.id_input.setStyleSheet(input_style)
        self.id_input.setAlignment(Qt.AlignRight)
        form_layout.addWidget(id_label)
        form_layout.addWidget(self.id_input)

        # Group input
        group_label = QLabel("קבוצה:")
        group_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        self.group_input = QComboBox()
        self.group_input.setStyleSheet(input_style)
        self.load_groups()
        form_layout.addWidget(group_label)
        form_layout.addWidget(self.group_input)

        # Payment status
        payment_label = QLabel("סטטוס תשלום:")
        payment_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        self.payment_status_input = QComboBox()
        self.payment_status_input.addItems(["חוב", "יתרת זכות", "שולם"])
        self.payment_status_input.setStyleSheet(input_style)
        form_layout.addWidget(payment_label)
        form_layout.addWidget(self.payment_status_input)

        # Join date
        date_label = QLabel("תאריך הצטרפות:")
        date_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        self.join_date_input = QDateEdit()
        self.join_date_input.setDate(QDate.currentDate())
        self.join_date_input.setDisplayFormat("dd/MM/yyyy")
        self.join_date_input.setStyleSheet(input_style)
        self.join_date_input.setCalendarPopup(True)
        form_layout.addWidget(date_label)
        form_layout.addWidget(self.join_date_input)

        main_layout.addWidget(form_card)

        # Buttons card
        buttons_card = AnimatedCard()
        buttons_layout = QHBoxLayout(buttons_card)
        buttons_layout.setSpacing(15)

        # Add button
        add_button = QPushButton("הוסף תלמידה")
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        add_button.setCursor(Qt.PointingHandCursor)
        add_button.clicked.connect(self.add_student)

        # Back button
        back_btn = QPushButton("⬅ חזרה לעמוד הקבוצות")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.clicked.connect(self.go_back)

        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(back_btn)

        main_layout.addWidget(buttons_card)

        # Run entrance animation
        self.run_entrance_animation(title_card, form_card, buttons_card)

    def run_entrance_animation(self, *widgets):
        for i, widget in enumerate(widgets):
            # Create animation for position
            animation = QPropertyAnimation(widget, b"pos")
            animation.setDuration(500)
            animation.setStartValue(widget.pos() + QPoint(0, 50))
            animation.setEndValue(widget.pos())
            animation.setEasingCurve(QEasingCurve.OutCubic)

            # Use QTimer to delay the start of animation
            QTimer.singleShot(i * 100, animation.start)

    def load_groups(self):
        try:
            with open("data/groups.json", encoding="utf-8") as f:
                data = json.load(f)
                groups = data.get("groups", [])
                for group in groups:
                    self.group_input.addItem(group["name"])

                # Set current group
                index = self.group_input.findText(self.group_name)
                if index >= 0:
                    self.group_input.setCurrentIndex(index)
        except Exception as e:
            print(f"Error loading groups: {e}")

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
            "group": self.group_input.currentText(),
            "payment_status": payment_status,
            "join_date": join_date
        }

        students_data["students"].append(new_student)

        try:
            with open("data/students.json", 'w', encoding="utf-8") as f:
                json.dump(students_data, f, ensure_ascii=False, indent=4)
            QMessageBox.information(self, "הצלחה", "התלמידה נוספה בהצלחה!")
            self.go_back()
        except Exception as e:
            QMessageBox.critical(self, "שגיאה", f"שגיאה בשמירה: {e}")

    def go_back(self):
        self.stacked_widget.setCurrentIndex(0)