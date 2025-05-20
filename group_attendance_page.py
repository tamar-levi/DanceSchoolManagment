import json
import os
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QListWidget, QInputDialog, QMessageBox,
    QFrame, QGraphicsDropShadowEffect, QHBoxLayout, QSpacerItem, QSizePolicy,
    QScrollArea, QListWidgetItem
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QTimer, QSize
from PyQt5.QtGui import QFont, QColor, QIcon

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

class GroupAttendancePage(QWidget):
    def __init__(self, stacked_widget, group):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.group = group
        self.attendance_data = {}
        
        # Set background color
        self.setStyleSheet("background-color: #f5f7fa;")
        
        self.load_attendance()
        self.init_ui()
        
        # Run entrance animation
        QTimer.singleShot(100, self.run_entrance_animation)

    def load_attendance(self):
        path = f"attendances/attendance_{self.group['id']}.json"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self.attendance_data = json.load(f)
        else:
            self.attendance_data = {}

    def save_attendance(self):
        os.makedirs("attendances", exist_ok=True)
        path = f"attendances/attendance_{self.group['id']}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.attendance_data, f, ensure_ascii=False, indent=2)

    def init_ui(self):
        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        self.setLayout(layout)
        
        # Store cards for animation
        self.cards = []
        
        # Header card
        header_card = AnimatedCard()
        header_layout = QVBoxLayout(header_card)
        
        title = QLabel("ניהול נוכחות")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        
        subtitle = QLabel(f"קבוצת {self.group['name']}")
        subtitle.setFont(QFont("Segoe UI", 16))
        subtitle.setStyleSheet("color: #7f8c8d;")
        subtitle.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header_card)
        self.cards.append(header_card)
        
        # Dates card
        dates_card = AnimatedCard()
        dates_layout = QVBoxLayout(dates_card)
        dates_layout.setContentsMargins(15, 15, 15, 15)
        
        dates_header = QLabel("תאריכי נוכחות")
        dates_header.setFont(QFont("Segoe UI", 14, QFont.Bold))
        dates_header.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        dates_layout.addWidget(dates_header)
        
        # Create custom list widget
        self.date_list = QListWidget()
        self.date_list.setStyleSheet("""
            QListWidget {
                background-color: #f9f9f9;
                border-radius: 6px;
                border: 1px solid #e0e0e0;
                padding: 5px;
            }
            QListWidget::item {
                background-color: #ffffff;
                border-radius: 4px;
                margin: 3px;
                padding: 8px;
                border: 1px solid #e0e0e0;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #ecf0f1;
            }
        """)
        self.date_list.setMinimumHeight(200)
        
        # Populate date list
        for date in self.attendance_data.keys():
            item = QListWidgetItem(date)
            item.setTextAlignment(Qt.AlignCenter)
            self.date_list.addItem(item)
        
        self.date_list.itemClicked.connect(self.open_date_attendance)
        dates_layout.addWidget(self.date_list)
        
        layout.addWidget(dates_card)
        self.cards.append(dates_card)
        
        # Actions card
        actions_card = AnimatedCard()
        actions_layout = QVBoxLayout(actions_card)
        actions_layout.setContentsMargins(15, 15, 15, 15)
        
        # Add date button
        add_date_btn = QPushButton("הוסף תאריך חדש")
        add_date_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        add_date_btn.setCursor(Qt.PointingHandCursor)
        add_date_btn.clicked.connect(self.add_new_date)
        actions_layout.addWidget(add_date_btn)
        
        # Back button
        back_btn = QPushButton("חזרה לקבוצות")
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
        actions_layout.addWidget(back_btn)
        
        layout.addWidget(actions_card)
        self.cards.append(actions_card)
        
        # Add spacer at the bottom
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def run_entrance_animation(self):
        for i, card in enumerate(self.cards):
            animation = QPropertyAnimation(card, b"pos")
            animation.setDuration(500)
            animation.setStartValue(card.pos() + QPoint(0, 50))
            animation.setEndValue(card.pos())
            animation.setEasingCurve(QEasingCurve.OutCubic)
            
            # Use QTimer to delay the start of animation
            QTimer.singleShot(i * 100, animation.start)

    def add_new_date(self):
        date, ok = QInputDialog.getText(
            self, 
            "הוסף תאריך", 
            "הכנס תאריך (למשל 07/05/2025):",
            text="DD/MM/YYYY"
        )
        
        if ok and date:
            if date not in self.attendance_data:
                self.attendance_data[date] = {}
                self.save_attendance()
                
                # Add with animation
                item = QListWidgetItem(date)
                item.setTextAlignment(Qt.AlignCenter)
                self.date_list.addItem(item)
                self.date_list.scrollToItem(item)
                
                # Flash animation for new item
                QTimer.singleShot(100, lambda: self.flash_item(item))

    def flash_item(self, item):
        # Get the index of the item
        index = self.date_list.row(item)
        
        # Get the item widget
        item_widget = self.date_list.item(index)
        
        # Original background
        original_bg = "background-color: #ffffff;"
        
        # Flash colors
        flash_colors = ["#d4edda", "#ffffff"]
        
        # Flash animation
        for i, color in enumerate(flash_colors * 3):
            QTimer.singleShot(i * 200, lambda c=color: item_widget.setBackground(QColor(c)))
        
        # Select the new item
        QTimer.singleShot(1200, lambda: self.date_list.setCurrentItem(item))

    def open_date_attendance(self, item):
        from attendance_table_page import AttendanceTablePage
        full_group = self.get_full_group_by_id(self.group["id"])
        if not full_group or not full_group.get("students"):
            QMessageBox.warning(self, "שגיאה", "לא נמצאה קבוצה עם תלמידות.")
            return

        page = AttendanceTablePage(self.go_back, full_group, item.text())
        self.stacked_widget.addWidget(page)
        self.stacked_widget.setCurrentWidget(page)

    def get_full_group_by_id(self, group_id):

        group = None
        if os.path.exists("data/groups.json"):
            with open("data/groups.json", "r", encoding="utf-8") as f:
                groups_data = json.load(f)
                for g in groups_data.get("groups", []):
                    if str(g["id"]) == str(group_id):
                        group = g
                        break
        else:
            print("The groups.json file does not exist")

        if not group:
            return None

        students = []
        if os.path.exists("data/students.json"):
            with open("data/students.json", "r", encoding="utf-8") as f:
                students_data = json.load(f)
                for s in students_data.get("students", []):
                    if s.get("group", "").strip() == group["name"].strip():
                        students.append({"id": s["id"], "name": s["name"]})
        else:
            print("The file students.json does not exist")

        group["students"] = students
        return group

    def go_back(self):
        self.stacked_widget.setCurrentIndex(2)
