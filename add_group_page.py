import json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QLabel,
    QFrame, QGraphicsDropShadowEffect, QFormLayout, QHBoxLayout
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QTimer
from PyQt5.QtGui import QFont, QColor
from attendance_page import AttendancePage

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

class AddGroupPage(QWidget):
    def __init__(self, stacked_widget, groups_page):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.groups_page = groups_page

        # Set background color
        self.setStyleSheet("background-color: #f5f7fa;")
        
        # Main layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)
        self.setLayout(self.layout)
        
        # Store cards for animation
        self.cards = []
        
        self.init_ui()
        
    def init_ui(self):
        # Header card
        header_card = AnimatedCard()
        header_layout = QVBoxLayout(header_card)
        
        title_label = QLabel("הוספת קבוצה חדשה")
        title_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)
        
        subtitle = QLabel("מלא את הפרטים ליצירת קבוצה חדשה")
        subtitle.setFont(QFont("Segoe UI", 14))
        subtitle.setStyleSheet("color: #7f8c8d;")
        subtitle.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitle)
        
        self.layout.addWidget(header_card)
        self.cards.append(header_card)
        
        # Form card
        form_card = AnimatedCard()
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(20, 20, 20, 20)
        
        # Style for form inputs
        input_style = """
            QLineEdit {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 12px;
                background-color: #f9f9f9;
                color: #2c3e50;
                font-size: 14px;
                margin-bottom: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
                background-color: white;
            }
        """
        
        # Create form
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.setFormAlignment(Qt.AlignRight)
        form.setSpacing(15)
        
        # Group name input
        self.group_name_input = QLineEdit()
        self.group_name_input.setPlaceholderText("שם הקבוצה")
        self.group_name_input.setStyleSheet(input_style)
        self.group_name_input.setMinimumHeight(40)
        
        # Group location input
        self.group_location_input = QLineEdit()
        self.group_location_input.setPlaceholderText("מיקום הקבוצה")
        self.group_location_input.setStyleSheet(input_style)
        self.group_location_input.setMinimumHeight(40)
        
        # Group price input
        self.group_price_input = QLineEdit()
        self.group_price_input.setPlaceholderText("עלות הקבוצה")
        self.group_price_input.setStyleSheet(input_style)
        self.group_price_input.setMinimumHeight(40)
        
        # Group age input
        self.group_age_input = QLineEdit()
        self.group_age_input.setPlaceholderText("קבוצת גילאים")
        self.group_age_input.setStyleSheet(input_style)
        self.group_age_input.setMinimumHeight(40)
        
        # Group teacher input
        self.group_teacher_input = QLineEdit()
        self.group_teacher_input.setPlaceholderText("שם המורה")
        self.group_teacher_input.setStyleSheet(input_style)
        self.group_teacher_input.setMinimumHeight(40)
        
        # Add fields to form with labels
        form.addRow("שם הקבוצה:", self.group_name_input)
        form.addRow("מיקום:", self.group_location_input)
        form.addRow("עלות:", self.group_price_input)
        form.addRow("קבוצת גילאים:", self.group_age_input)
        form.addRow("מורה:", self.group_teacher_input)
        
        form_layout.addLayout(form)
        self.layout.addWidget(form_card)
        self.cards.append(form_card)
        
        # Buttons card
        buttons_card = AnimatedCard()
        buttons_layout = QHBoxLayout(buttons_card)
        buttons_layout.setContentsMargins(15, 15, 15, 15)
        buttons_layout.setSpacing(15)
        
        # Save button
        self.save_button = QPushButton("שמור קבוצה")
        self.save_button.setStyleSheet("""
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
        self.save_button.setCursor(Qt.PointingHandCursor)
        self.save_button.clicked.connect(self.save_group)
        
        # Back button
        self.back_button = QPushButton("⬅ חזרה לעמוד הקבוצות")
        self.back_button.setStyleSheet("""
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
        self.back_button.setCursor(Qt.PointingHandCursor)
        self.back_button.clicked.connect(self.go_back)
        
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.back_button)
        
        self.layout.addWidget(buttons_card)
        self.cards.append(buttons_card)
        
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

    def save_group(self):
        name = self.group_name_input.text().strip()
        location = self.group_location_input.text().strip()
        price = self.group_price_input.text().strip()
        age_group = self.group_age_input.text().strip()
        teacher = self.group_teacher_input.text().strip()

        if not name or not location or not price or not age_group or not teacher:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("שגיאה")
            msg_box.setText("נא למלא את כל השדות.")
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
            with open("data/groups.json", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {"groups": []}

        existing_ids = [group.get("id", 0) for group in data.get("groups", [])]
        new_id = max(existing_ids) + 1 if existing_ids else 1

        new_group = {
            "id": new_id,
            "name": name,
            "location": location,
            "price": price,
            "age_group": age_group,
            "teacher": teacher
        }

        data["groups"].append(new_group)

        try:
            with open("data/groups.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            msg_box = QMessageBox()
            msg_box.setWindowTitle("הצלחה")
            msg_box.setText("הקבוצה נוספה בהצלחה!")
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
            
            self.group_name_input.clear()
            self.group_location_input.clear()
            self.group_price_input.clear()
            self.group_age_input.clear()
            self.group_teacher_input.clear()
            self.go_back()

            attendance_page = AttendancePage(self.stacked_widget)
            attendance_page.refresh()
            self.stacked_widget.setCurrentWidget(attendance_page)

        except Exception as e:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("שגיאה")
            msg_box.setText(f"שגיאה בשמירת הקובץ: {e}")
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

    def go_back(self):
        groups_widget = self.stacked_widget.widget(1)
        if hasattr(groups_widget, 'build_group_buttons'):
            groups_widget.build_group_buttons()
        
        self.stacked_widget.setCurrentIndex(1)
