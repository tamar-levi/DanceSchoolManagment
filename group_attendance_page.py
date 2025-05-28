import json
import os
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QInputDialog, QMessageBox,
    QFrame, QGraphicsDropShadowEffect, QHBoxLayout, QSpacerItem, QSizePolicy,
    QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QAbstractItemView,
    QMenu, QAction
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QTimer, QSize, QRect
from PyQt5.QtGui import QFont, QColor, QIcon, QPainter, QPen

class AttendanceCheckBox(QCheckBox):
    def __init__(self, date, student_id, parent_page):
        super().__init__()
        self.date = date
        self.student_id = student_id
        self.parent_page = parent_page
        self.setFixedSize(35, 35)  # Fixed size for the checkbox
        self.setStyleSheet("""
            QCheckBox {
                spacing: 0px;
                background-color: transparent;
            }
        """)
        
        self.stateChanged.connect(self.on_state_changed)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Get the full widget rect
        rect = self.rect()
        
        # Draw the circle background
        circle_rect = QRect(2, 2, 31, 31)  # Slightly smaller than widget
        
        if self.isChecked():
            # Green background for checked
            painter.setBrush(QColor(39, 174, 96))  # #27ae60
            painter.setPen(QPen(QColor(34, 153, 84), 2))  # #229954
        else:
            # Red background for unchecked
            painter.setBrush(QColor(231, 76, 60))  # #e74c3c
            painter.setPen(QPen(QColor(192, 57, 43), 2))  # #c0392b
        
        painter.drawEllipse(circle_rect)
        
        # Draw the symbol in white
        pen = QPen(QColor(255, 255, 255))  # White color
        pen.setWidth(3)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        
        center_x = circle_rect.center().x()
        center_y = circle_rect.center().y()
        
        if self.isChecked():
            # Draw checkmark (✓)
            painter.drawLine(center_x - 8, center_y, center_x - 3, center_y + 5)
            painter.drawLine(center_x - 3, center_y + 5, center_x + 8, center_y - 5)
        else:
            # Draw X
            painter.drawLine(center_x - 6, center_y - 6, center_x + 6, center_y + 6)
            painter.drawLine(center_x - 6, center_y + 6, center_x + 6, center_y - 6)
    
    def on_state_changed(self):
        self.update()  # Trigger repaint
        self.parent_page.update_attendance(self.date, self.student_id, self.isChecked())

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
        self.students = []
        
        # Set background color
        self.setStyleSheet("background-color: #f5f7fa;")
        
        self.load_attendance()
        self.load_students()
        self.init_ui()
        
        # Run entrance animation
        # QTimer.singleShot(100, self.run_entrance_animation)

    def load_attendance(self):
        path = f"attendances/attendance_{self.group['id']}.json"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self.attendance_data = json.load(f)
        else:
            self.attendance_data = {}

    def load_students(self):
        if os.path.exists("data/students.json"):
            with open("data/students.json", "r", encoding="utf-8") as f:
                students_data = json.load(f)
                for s in students_data.get("students", []):
                    if s.get("group", "").strip() == self.group["name"].strip():
                        self.students.append({"id": s["id"], "name": s["name"]})

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
        
        # Table card
        table_card = AnimatedCard()
        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(15, 15, 15, 15)
        
        table_header = QLabel("טבלת נוכחות")
        table_header.setFont(QFont("Segoe UI", 14, QFont.Bold))
        table_header.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        table_layout.addWidget(table_header)
        
        # Create attendance table
        self.attendance_table = QTableWidget()
        self.setup_table()
        table_layout.addWidget(self.attendance_table)
        
        layout.addWidget(table_card)
        self.cards.append(table_card)
        
        # Actions card
        actions_card = AnimatedCard()
        actions_layout = QHBoxLayout(actions_card)
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

    def setup_table(self):
        dates = list(self.attendance_data.keys())
        
        # Set table dimensions
        self.attendance_table.setRowCount(len(dates))
        self.attendance_table.setColumnCount(len(self.students) + 1)  # +1 for date column
        
        # Set headers
        headers = ["תאריך"] + [student["name"] for student in self.students]
        self.attendance_table.setHorizontalHeaderLabels(headers)
        
        # Style the table
        self.attendance_table.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                gridline-color: #e0e0e0;
                selection-background-color: transparent;
            }
            QTableWidget::item {
                padding: 8px;
                border: none;
                background-color: #ffffff;
            }
            QTableWidget::item:selected {
                background-color: #ecf0f1;
                color: #2c3e50;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
        """)
        
        # Set table properties
        self.attendance_table.setAlternatingRowColors(True)
        self.attendance_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        # הסר את השורה הבעייתית:
        # self.attendance_table.horizontalHeader().setStretchLastSection(True)
        
        # במקום זה, השתמש ב-ResizeToContents לכל העמודות:
        self.attendance_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        
        self.attendance_table.verticalHeader().setVisible(False)
        
        # Enable context menu for date cells
        self.attendance_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.attendance_table.customContextMenuRequested.connect(self.show_context_menu)
        
        # Populate table
        for row, date in enumerate(dates):
            # Date column
            date_item = QTableWidgetItem(date)
            date_item.setTextAlignment(Qt.AlignCenter)
            date_item.setFlags(date_item.flags() & ~Qt.ItemIsEditable)
            date_item.setBackground(QColor(255, 255, 255))  # Force white background
            self.attendance_table.setItem(row, 0, date_item)
            
            # Student attendance columns
            for col, student in enumerate(self.students):
                checkbox = AttendanceCheckBox(date, student["id"], self)
                
                # Set checkbox state based on saved data
                if date in self.attendance_data:
                    if str(student["id"]) in self.attendance_data[date]:
                        checkbox.setChecked(self.attendance_data[date][str(student["id"])])
                    else:
                        checkbox.setChecked(False)
                else:
                    checkbox.setChecked(False)
                
                # Center the checkbox in the cell
                self.attendance_table.setCellWidget(row, col + 1, checkbox)
        
        # Set row height to accommodate checkboxes
        for row in range(self.attendance_table.rowCount()):
            self.attendance_table.setRowHeight(row, 45)
        
        # הסר את השורה הזו כי היא כבר לא נחוצה:
        # self.attendance_table.resizeColumnsToContents()
        self.attendance_table.setMinimumHeight(400)

    def show_context_menu(self, position):
        item = self.attendance_table.itemAt(position)
        if item and item.column() == 0:  # Only for date column
            menu = QMenu(self)
            menu.setStyleSheet("""
                QMenu {
                    background-color: #ffffff;
                    border: 1px solid #bdc3c7;
                    border-radius: 5px;
                    padding: 5px;
                }
                QMenu::item {
                    background-color: transparent;
                    color: #2c3e50;
                    padding: 8px 16px;
                    border-radius: 3px;
                }
                QMenu::item:selected {
                    background-color: #3498db;
                    color: white;
                }
            """)
            
            edit_action = QAction("ערוך תאריך", self)
            edit_action.triggered.connect(lambda: self.edit_date(item.row()))
            menu.addAction(edit_action)
            
            delete_action = QAction("מחק תאריך", self)
            delete_action.triggered.connect(lambda: self.delete_date(item.row()))
            menu.addAction(delete_action)
            
            menu.exec_(self.attendance_table.mapToGlobal(position))

    def edit_date(self, row):
        current_date = self.attendance_table.item(row, 0).text()
        new_date, ok = QInputDialog.getText(
            self, 
            "ערוך תאריך", 
            "הכנס תאריך חדש:",
            text=current_date
        )
        
        if ok and new_date and new_date != current_date:
            if new_date not in self.attendance_data:
                # Update attendance data
                self.attendance_data[new_date] = self.attendance_data.pop(current_date)
                self.save_attendance()
                
                # Refresh table
                self.setup_table()
                
                QMessageBox.information(self, "הצלחה", f"התאריך עודכן ל-{new_date}")
            else:
                QMessageBox.warning(self, "שגיאה", "התאריך הזה כבר קיים!")

    def delete_date(self, row):
        current_date = self.attendance_table.item(row, 0).text()
        reply = QMessageBox.question(
            self, 
            "מחיקת תאריך", 
            f"האם אתה בטוח שברצונך למחוק את התאריך {current_date}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            del self.attendance_data[current_date]
            self.save_attendance()
            self.setup_table()
            QMessageBox.information(self, "הצלחה", "התאריך נמחק בהצלחה!")

    def update_attendance(self, date, student_id, is_present):
        if date not in self.attendance_data:
            self.attendance_data[date] = {}
        
        self.attendance_data[date][str(student_id)] = is_present
        self.save_attendance()

    def add_new_date(self):
        date, ok = QInputDialog.getText(
            self, 
            "הוסף תאריך", 
            "הכנס תאריך (למשל 07/05/2025):",
            text="DD/MM/YYYY"
        )
        
        if ok and date:
            if date not in self.attendance_data:
                # Initialize new date with all students as False (absent)
                self.attendance_data[date] = {}
                for student in self.students:
                    self.attendance_data[date][str(student["id"])] = False
                
                self.save_attendance()
                
                # Refresh the table
                self.setup_table()
                
                QMessageBox.information(self, "הצלחה", f"התאריך {date} נוסף בהצלחה!")
            else:
                QMessageBox.warning(self, "שגיאה", "התאריך הזה כבר קיים!")

    def run_entrance_animation(self):
        # Only run animation once when page loads
        for i, card in enumerate(self.cards):
            animation = QPropertyAnimation(card, b"pos")
            animation.setDuration(500)
            animation.setStartValue(card.pos() + QPoint(0, 50))
            animation.setEndValue(card.pos())
            animation.setEasingCurve(QEasingCurve.OutCubic)
            
            # Use QTimer to delay the start of animation
            QTimer.singleShot(i * 100, animation.start)

    def go_back(self):
        self.stacked_widget.setCurrentIndex(2)
