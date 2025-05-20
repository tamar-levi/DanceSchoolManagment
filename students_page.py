import json
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QFrame,
    QLineEdit, QHBoxLayout, QMessageBox, QFormLayout, QScrollArea,
    QGraphicsDropShadowEffect, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QTimer, QSize
from add_student_page import AddStudentPage


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


class StudentsPage(QWidget):
    def __init__(self, stacked_widget, group_name):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.group_name = group_name
        
        # Set background color
        self.setStyleSheet("background-color: #f5f7fa;")
        
        # Main layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)
        self.setLayout(self.layout)
        
        # Store cards for animation
        self.cards = []
        
        self.show_students()

    def show_students(self):
        self.clear_layout()
        self.cards = []
        
        # Header card
        header_card = AnimatedCard()
        header_layout = QVBoxLayout(header_card)
        
        title = QLabel("רשימת תלמידות")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        
        subtitle = QLabel(f"קבוצת {self.group_name}")
        subtitle.setFont(QFont("Segoe UI", 16))
        subtitle.setStyleSheet("color: #7f8c8d;")
        subtitle.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitle)
        
        self.layout.addWidget(header_card)
        self.cards.append(header_card)
        
        # Students card
        students_card = AnimatedCard()
        students_layout = QVBoxLayout(students_card)
        students_layout.setContentsMargins(15, 15, 15, 15)
        
        # Create scroll area for students
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        container_widget = QWidget()
        container_layout = QVBoxLayout(container_widget)
        container_layout.setContentsMargins(5, 5, 5, 5)
        container_layout.setSpacing(15)
        
        try:
            with open("data/students.json", encoding="utf-8") as f:
                students = json.load(f).get("students", [])
        except Exception as e:
            error_label = QLabel("שגיאה בטעינת התלמידות")
            error_label.setStyleSheet("color: #e74c3c; font-size: 14px;")
            error_label.setAlignment(Qt.AlignCenter)
            container_layout.addWidget(error_label)
            print("Error:", e)
            students = []

        self.current_students = [s for s in students if s.get("group") == self.group_name]

        if not self.current_students:
            empty_label = QLabel("אין תלמידות בקבוצה זו")
            empty_label.setStyleSheet("color: #7f8c8d; font-size: 14px;")
            empty_label.setAlignment(Qt.AlignCenter)
            container_layout.addWidget(empty_label)
        else:
            for student in self.current_students:
                card = self.create_student_card(student)
                container_layout.addWidget(card)
                
                # Add to animation list
                self.cards.append(card)

        scroll_area.setWidget(container_widget)
        students_layout.addWidget(scroll_area)
        
        self.layout.addWidget(students_card)
        self.cards.append(students_card)
        
        # Actions card
        actions_card = AnimatedCard()
        actions_layout = QHBoxLayout(actions_card)
        actions_layout.setContentsMargins(15, 15, 15, 15)
        actions_layout.setSpacing(15)
        
        # Add student button
        add_student_btn = QPushButton("➕ הוסף תלמידה")
        add_student_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        add_student_btn.setCursor(Qt.PointingHandCursor)
        add_student_btn.clicked.connect(self.go_to_add_student_page)
        
        # Back button
        back_btn = QPushButton("⬅ חזרה לרשימת הקבוצות")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.clicked.connect(self.go_back)
        
        actions_layout.addWidget(add_student_btn)
        actions_layout.addWidget(back_btn)
        
        self.layout.addWidget(actions_card)
        self.cards.append(actions_card)
        
        # Run entrance animation
        QTimer.singleShot(100, self.run_entrance_animation)

    def run_entrance_animation(self):
        for i, card in enumerate(self.cards):
            animation = QPropertyAnimation(card, b"pos")
            animation.setDuration(500)
            animation.setStartValue(card.pos() + QPoint(0, 50))
            animation.setEndValue(card.pos())
            animation.setEasingCurve(QEasingCurve.OutCubic)
            
            # Use QTimer to delay the start of animation
            QTimer.singleShot(i * 100, animation.start)

    def create_student_card(self, student):
        card = AnimatedCard()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)
        
        # Header with icon and name
        header_layout = QHBoxLayout()
        
        # Student icon
        icon_label = QLabel()
        pixmap = QPixmap("icons/student.png")  # Ensure this path exists or use a default icon
        if not pixmap.isNull():
            icon_label.setPixmap(pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            # Create a placeholder with student initials
            icon_label.setText(student['name'][0] if student['name'] else "?")
            icon_label.setStyleSheet("""
                QLabel {
                    background-color: #3498db;
                    color: white;
                    border-radius: 20px;
                    font-size: 18px;
                    font-weight: bold;
                    min-width: 40px;
                    min-height: 40px;
                    max-width: 40px;
                    max-height: 40px;
                    qproperty-alignment: AlignCenter;
                }
            """)
        
        # Student name
        name_label = QLabel(student['name'])
        name_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        name_label.setStyleSheet("color: #2c3e50;")
        
        header_layout.addWidget(icon_label)
        header_layout.addWidget(name_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Student details
        details_layout = QFormLayout()
        details_layout.setContentsMargins(10, 10, 10, 10)
        details_layout.setSpacing(8)
        details_layout.setLabelAlignment(Qt.AlignRight)
        details_layout.setFormAlignment(Qt.AlignRight)
        
        # Style for labels
        label_style = "font-weight: bold; color: #7f8c8d;"
        value_style = "color: #2c3e50;"
        
        # Phone
        phone_label = QLabel("📞 טלפון:")
        phone_label.setStyleSheet(label_style)
        phone_value = QLabel(student['phone'])
        phone_value.setStyleSheet(value_style)
        details_layout.addRow(phone_label, phone_value)
        
        # Group
        group_label = QLabel("👥 קבוצה:")
        group_label.setStyleSheet(label_style)
        group_value = QLabel(student['group'])
        group_value.setStyleSheet(value_style)
        details_layout.addRow(group_label, group_value)
        
        # Payment status
        payment_label = QLabel("💰 סטטוס תשלום:")
        payment_label.setStyleSheet(label_style)
        payment_value = QLabel(student['payment_status'])
        
        # Color-code payment status
        if student['payment_status'] == "שולם":
            payment_value.setStyleSheet("color: #2ecc71; font-weight: bold;")
        elif student['payment_status'] == "חוב" or "חוב:" in student['payment_status']:
            payment_value.setStyleSheet("color: #e74c3c; font-weight: bold;")
        else:
            payment_value.setStyleSheet("color: #f39c12; font-weight: bold;")
            
        details_layout.addRow(payment_label, payment_value)
        
        # Join date
        date_label = QLabel("📅 תאריך הצטרפות:")
        date_label.setStyleSheet(label_style)
        date_value = QLabel(student['join_date'])
        date_value.setStyleSheet(value_style)
        details_layout.addRow(date_label, date_value)
        
        layout.addLayout(details_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        edit_btn = QPushButton("עריכה")
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        edit_btn.setCursor(Qt.PointingHandCursor)
        
        delete_btn = QPushButton("מחיקה")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        delete_btn.setCursor(Qt.PointingHandCursor)
        
        # Add payments button
        payments_btn = QPushButton("💳 תשלומים")
        payments_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        payments_btn.setCursor(Qt.PointingHandCursor)
        
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addWidget(payments_btn)
        
        layout.addLayout(button_layout)
        
        edit_btn.clicked.connect(lambda: self.edit_single_student(student))
        delete_btn.clicked.connect(lambda: self.confirm_delete(student['name']))
        payments_btn.clicked.connect(lambda: self.show_payments(student))
        
        return card

    def confirm_delete(self, student_name):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("אישור מחיקה")
        msg_box.setText(f"האם למחוק את התלמידה '{student_name}'?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #f5f7fa;
            }
            QLabel {
                color: #2
            QMessageBox {
                background-color: #f5f7fa;
            }
            QLabel {
                color: #2c3e50;
                font-size: 14px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton[text="לא"] {
                background-color: #e74c3c;
            }
            QPushButton[text="לא"]:hover {
                background-color: #c0392b;
            }
        """)
        
        reply = msg_box.exec_()
        if reply == QMessageBox.Yes:
            self.delete_student(student_name)

    def edit_single_student(self, student):
        self.clear_layout()
        self.cards = []
        
        # Header card
        header_card = AnimatedCard()
        header_layout = QVBoxLayout(header_card)
        
        title = QLabel("עריכת תלמידה")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        
        subtitle = QLabel(student['name'])
        subtitle.setFont(QFont("Segoe UI", 16))
        subtitle.setStyleSheet("color: #7f8c8d;")
        subtitle.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitle)
        
        self.layout.addWidget(header_card)
        self.cards.append(header_card)
        
        # Form card
        form_card = AnimatedCard()
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create form
        edit_form = QFormLayout()
        edit_form.setLabelAlignment(Qt.AlignRight)
        edit_form.setFormAlignment(Qt.AlignRight)
        edit_form.setSpacing(15)
        
        # Style for form inputs
        input_style = """
            QLineEdit {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 8px;
                background-color: #f9f9f9;
                color: #2c3e50;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
                background-color: white;
            }
        """
        
        # Create form fields
        name_edit = QLineEdit(student['name'])
        name_edit.setStyleSheet(input_style)
        name_edit.setMinimumHeight(35)
        
        phone_edit = QLineEdit(student['phone'])
        phone_edit.setStyleSheet(input_style)
        phone_edit.setMinimumHeight(35)
        
        group_edit = QLineEdit(student['group'])
        group_edit.setStyleSheet(input_style)
        group_edit.setMinimumHeight(35)
        
        payment_edit = QLineEdit(student['payment_status'])
        payment_edit.setStyleSheet(input_style)
        payment_edit.setMinimumHeight(35)
        
        join_edit = QLineEdit(student['join_date'])
        join_edit.setStyleSheet(input_style)
        join_edit.setMinimumHeight(35)
        
        # Add fields to form
        edit_form.addRow("שם:", name_edit)
        edit_form.addRow("טלפון:", phone_edit)
        edit_form.addRow("קבוצה:", group_edit)
        edit_form.addRow("סטטוס תשלום:", payment_edit)
        edit_form.addRow("תאריך הצטרפות:", join_edit)
        
        form_layout.addLayout(edit_form)
        self.layout.addWidget(form_card)
        self.cards.append(form_card)
        
        # Buttons card
        buttons_card = AnimatedCard()
        buttons_layout = QHBoxLayout(buttons_card)
        buttons_layout.setContentsMargins(15, 15, 15, 15)
        buttons_layout.setSpacing(15)
        
        # Save button
        save_btn = QPushButton("שמור")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        save_btn.setCursor(Qt.PointingHandCursor)
        
        # Cancel button
        cancel_btn = QPushButton("ביטול")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        cancel_btn.setCursor(Qt.PointingHandCursor)
        
        buttons_layout.addWidget(save_btn)
        buttons_layout.addWidget(cancel_btn)
        
        self.layout.addWidget(buttons_card)
        self.cards.append(buttons_card)
        
        # Connect buttons
        save_btn.clicked.connect(lambda: self.save_student(
            original_name=student['name'],
            new_data={
                "id": student.get('id', ''),
                "name": name_edit.text().strip(),
                "phone": phone_edit.text().strip(),
                "group": group_edit.text().strip(),
                "payment_status": payment_edit.text().strip(),
                "join_date": join_edit.text().strip(),
                "payments": student.get('payments', [])  # שמירת התשלומים הקיימים
            }
        ))
        cancel_btn.clicked.connect(self.show_students)
        
        # Run entrance animation
        QTimer.singleShot(100, self.run_entrance_animation)

    def save_student(self, original_name, new_data):
        if not all([new_data['name'], new_data['phone'], new_data['group'], new_data['payment_status'], new_data['join_date']]):
            msg_box = QMessageBox()
            msg_box.setWindowTitle("שגיאה")
            msg_box.setText("יש למלא את כל השדות.")
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #f5f7fa;
                }
                QLabel {
                    color: #2c3e50;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    padding: 8px 15px;
                    border-radius: 4px;
                    font-weight: bold;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            msg_box.exec_()
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

            # Success message
            msg_box = QMessageBox()
            msg_box.setWindowTitle("הצלחה")
            msg_box.setText("פרטי התלמידה נשמרו בהצלחה!")
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #f5f7fa;
                }
                QLabel {
                    color: #2c3e50;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #2ecc71;
                    color: white;
                    border: none;
                    padding: 8px 15px;
                    border-radius: 4px;
                    font-weight: bold;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #27ae60;
                }
            """)
            msg_box.exec_()
            
            self.show_students()
        except Exception as e:
            # Error message
            msg_box = QMessageBox()
            msg_box.setWindowTitle("שגיאה")
            msg_box.setText(f"שגיאה בשמירה: {e}")
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #f5f7fa;
                }
                QLabel {
                    color: #2c3e50;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    border: none;
                    padding: 8px 15px;
                    border-radius: 4px;
                    font-weight: bold;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
            """)
            msg_box.exec_()
            print(f"שגיאה בשמירה: {e}")

    def delete_student(self, student_name):
        try:
            with open("data/students.json", encoding="utf-8") as f:
                data = json.load(f)
                students = data.get("students", [])

            updated_students = [s for s in students if s['name'] != student_name]

            with open("data/students.json", 'w', encoding="utf-8") as f:
                json.dump({"students": updated_students}, f, ensure_ascii=False, indent=4)

            # Success message
            msg_box = QMessageBox()
            msg_box.setWindowTitle("הצלחה")
            msg_box.setText(f"התלמידה {student_name} נמחקה בהצלחה!")
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #f5f7fa;
                }
                QLabel {
                    color: #2c3e50;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #2ecc71;
                    color: white;
                    border: none;
                    padding: 8px 15px;
                    border-radius: 4px;
                    font-weight: bold;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #27ae60;
                }
            """)
            msg_box.exec_()
            
            self.show_students()
        except Exception as e:
            # Error message
            msg_box = QMessageBox()
            msg_box.setWindowTitle("שגיאה")
            msg_box.setText(f"שגיאה במחיקה: {e}")
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #f5f7fa;
                }
                QLabel {
                    color: #2c3e50;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    border: none;
                    padding: 8px 15px;
                    border-radius: 4px;
                    font-weight: bold;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
            """)
            msg_box.exec_()
            print(f"שגיאה במחיקה: {e}")

    # פונקציות חדשות לניהול תשלומים
    def show_payments(self, student):
        self.clear_layout()
        self.cards = []
        
        # Header card
        header_card = AnimatedCard()
        header_layout = QVBoxLayout(header_card)
        
        title = QLabel("💳 תשלומים")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        
        subtitle = QLabel(f"עבור {student['name']}")
        subtitle.setFont(QFont("Segoe UI", 16))
        subtitle.setStyleSheet("color: #7f8c8d;")
        subtitle.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitle)
        
        self.layout.addWidget(header_card)
        self.cards.append(header_card)
        
        # Payments card
        payments_card = AnimatedCard()
        payments_layout = QVBoxLayout(payments_card)
        payments_layout.setContentsMargins(20, 20, 20, 20)
        
        try:
            payments = student.get('payments', [])
        except KeyError:
            payments = []
            
        if not payments:
            empty_label = QLabel("לא נמצאו תשלומים לתלמידה זו")
            empty_label.setStyleSheet("color: #7f8c8d; font-size: 16px;")
            empty_label.setAlignment(Qt.AlignCenter)
            payments_layout.addWidget(empty_label)
        else:
            for payment in payments:
                payment_card = QFrame()
                payment_card.setStyleSheet("""
                    QFrame {
                        background-color: #f8f9fa;
                        border-radius: 6px;
                        padding: 10px;
                        margin: 5px 0;
                    }
                """)
                payment_card_layout = QVBoxLayout(payment_card)
                payment_card = QFrame()
                payment_card.setStyleSheet("""
                    QFrame {
                        background-color: #f8f9fa;
                        border-radius: 6px;
                        padding: 10px;
                        margin: 5px 0;
                    }
                """)
                payment_card_layout = QVBoxLayout(payment_card)
                
                amount_label = QLabel(f"💵 סכום: {payment['amount']}₪")
                amount_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
                
                date_label = QLabel(f"📅 תאריך: {payment['date']}")
                date_label.setStyleSheet("font-size: 14px; color: #7f8c8d;")
                
                method_label = QLabel(f"💳 אופן תשלום: {payment['payment_method']}")
                method_label.setStyleSheet("font-size: 14px; color: #7f8c8d;")
                
                payment_card_layout.addWidget(amount_label)
                payment_card_layout.addWidget(date_label)
                payment_card_layout.addWidget(method_label)
                
                payments_layout.addWidget(payment_card)
        
        self.layout.addWidget(payments_card)
        self.cards.append(payments_card)
        
        # Actions card
        actions_card = AnimatedCard()
        actions_layout = QHBoxLayout(actions_card)
        actions_layout.setContentsMargins(15, 15, 15, 15)
        actions_layout.setSpacing(15)
        
        # Add payment button
        add_payment_btn = QPushButton("➕ הוסף תשלום")
        add_payment_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        add_payment_btn.setCursor(Qt.PointingHandCursor)
        add_payment_btn.clicked.connect(lambda: self.show_add_payment_form(student))
        
        # Back button
        back_btn = QPushButton("⬅ חזרה לרשימת התלמידות")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.clicked.connect(self.show_students)
        
        actions_layout.addWidget(add_payment_btn)
        actions_layout.addWidget(back_btn)
        
        self.layout.addWidget(actions_card)
        self.cards.append(actions_card)
        
        # Run entrance animation
        QTimer.singleShot(100, self.run_entrance_animation)

    def show_add_payment_form(self, student):
        self.clear_layout()
        self.cards = []
        
        # Header card
        header_card = AnimatedCard()
        header_layout = QVBoxLayout(header_card)
        
        title = QLabel("💳 הוספת תשלום")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        
        subtitle = QLabel(f"עבור {student['name']}")
        subtitle.setFont(QFont("Segoe UI", 16))
        subtitle.setStyleSheet("color: #7f8c8d;")
        subtitle.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitle)
        
        self.layout.addWidget(header_card)
        self.cards.append(header_card)
        
        # Form card
        form_card = AnimatedCard()
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create form
        payment_form = QFormLayout()
        payment_form.setLabelAlignment(Qt.AlignRight)
        payment_form.setFormAlignment(Qt.AlignRight)
        payment_form.setSpacing(15)
        
        # Style for form inputs
        input_style = """
            QLineEdit {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 8px;
                background-color: #f9f9f9;
                color: #2c3e50;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
                background-color: white;
            }
        """
        
        # Create form fields
        self.amount_input = QLineEdit()
        self.amount_input.setStyleSheet(input_style)
        self.amount_input.setMinimumHeight(35)
        self.amount_input.setPlaceholderText("הכנס סכום (מספר בלבד)")
        
        self.date_input = QLineEdit()
        self.date_input.setStyleSheet(input_style)
        self.date_input.setMinimumHeight(35)
        self.date_input.setPlaceholderText("הכנס תאריך (לדוגמה: 01/01/2023)")
        
        self.payment_method_input = QLineEdit()
        self.payment_method_input.setStyleSheet(input_style)
        self.payment_method_input.setMinimumHeight(35)
        self.payment_method_input.setPlaceholderText("הכנס אופן תשלום (לדוגמה: מזומן, אשראי)")
        
        # Add fields to form
        payment_form.addRow("סכום:", self.amount_input)
        payment_form.addRow("תאריך:", self.date_input)
        payment_form.addRow("אופן תשלום:", self.payment_method_input)
        
        form_layout.addLayout(payment_form)
        self.layout.addWidget(form_card)
        self.cards.append(form_card)
        
        # Buttons card
        buttons_card = AnimatedCard()
        buttons_layout = QHBoxLayout(buttons_card)
        buttons_layout.setContentsMargins(15, 15, 15, 15)
        buttons_layout.setSpacing(15)
        
        # Save button
        save_btn = QPushButton("שמור תשלום")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        save_btn.setCursor(Qt.PointingHandCursor)
        
        # Cancel button
        cancel_btn = QPushButton("ביטול")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        cancel_btn.setCursor(Qt.PointingHandCursor)
        
        buttons_layout.addWidget(save_btn)
        buttons_layout.addWidget(cancel_btn)
        
        self.layout.addWidget(buttons_card)
        self.cards.append(buttons_card)
        
        # Connect buttons
        save_btn.clicked.connect(lambda: self.save_payment(student, {
            "amount": self.amount_input.text().strip(),
            "date": self.date_input.text().strip(),
            "payment_method": self.payment_method_input.text().strip()
        }))
        cancel_btn.clicked.connect(lambda: self.show_payments(student))
        
        # Run entrance animation
        QTimer.singleShot(100, self.run_entrance_animation)

    def save_payment(self, student, payment_data):
        if not all(payment_data.values()):
            msg_box = QMessageBox()
            msg_box.setWindowTitle("שגיאה")
            msg_box.setText("יש למלא את כל השדות.")
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #f5f7fa;
                }
                QLabel {
                    color: #2c3e50;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    padding: 8px 15px;
                    border-radius: 4px;
                    font-weight: bold;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            msg_box.exec_()
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
            
            # Success message
            msg_box = QMessageBox()
            msg_box.setWindowTitle("הצלחה")
            msg_box.setText("התשלום נשמר בהצלחה!")
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #f5f7fa;
                }
                QLabel {
                    color: #2c3e50;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #2ecc71;
                    color: white;
                    border: none;
                    padding: 8px 15px;
                    border-radius: 4px;
                    font-weight: bold;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #27ae60;
                }
            """)
            msg_box.exec_()
            
            # חזרה לעמוד התשלומים
            self.show_payments(student)
            
        except Exception as e:
            # Error message
            msg_box = QMessageBox()
            msg_box.setWindowTitle("שגיאה")
            msg_box.setText(f"שגיאה בשמירת תשלום: {e}")
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #f5f7fa;
                }
                QLabel {
                    color: #2c3e50;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    border: none;
                    padding: 8px 15px;
                    border-radius: 4px;
                    font-weight: bold;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
            """)
            msg_box.exec_()
            print(f"שגיאה בשמירת תשלום: {e}")

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
