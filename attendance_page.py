import json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QFrame, QGraphicsDropShadowEffect, QSpacerItem, QSizePolicy,
    QScrollArea
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QTimer
from PyQt5.QtGui import QFont, QColor
from group_attendance_page import GroupAttendancePage

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

def load_groups():
    try:
        with open("data/groups.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("groups", [])
    except Exception as e:
        print("שגיאה בטעינת קבוצות:", e)
        return []

class AttendancePage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        
        # Set background color
        self.setStyleSheet("background-color: #f5f7fa;")
        
        # Main layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)
        self.setLayout(self.layout)
        
        # Store cards for animation
        self.cards = []

    def showEvent(self, event):
        super().showEvent(event)
        self.refresh()
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

    def refresh(self):
        self.clear_layout()
        self.cards = []
        groups = load_groups()
        
        # Header card
        header_card = AnimatedCard()
        header_layout = QVBoxLayout(header_card)
        
        title = QLabel("ניהול נוכחות")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        
        subtitle = QLabel("בחר קבוצה לניהול נוכחות")
        subtitle.setFont(QFont("Segoe UI", 16))
        subtitle.setStyleSheet("color: #7f8c8d;")
        subtitle.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitle)
        
        self.layout.addWidget(header_card)
        self.cards.append(header_card)
        
        # Groups card
        groups_card = AnimatedCard()
        groups_layout = QVBoxLayout(groups_card)
        groups_layout.setContentsMargins(15, 15, 15, 15)
        groups_layout.setSpacing(10)
        
        # Create scroll area for groups
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
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(5, 5, 5, 5)
        scroll_layout.setSpacing(10)
        
        for group in groups:
            btn = QPushButton(group["name"])
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #bbdefb;
                    color: #2c3e50;
                    border: none;
                    padding: 12px;
                    font-size: 14px;
                    font-weight: bold;
                    border-radius: 6px;
                    text-align: right;
                }
                QPushButton:hover {
                    background-color: #90caf9;
                }
            """)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _, g=group: self.show_group_attendance(g))
            scroll_layout.addWidget(btn)
        
        scroll_area.setWidget(scroll_content)
        groups_layout.addWidget(scroll_area)
        
        self.layout.addWidget(groups_card)
        self.cards.append(groups_card)
        
        # Navigation card
        nav_card = AnimatedCard()
        nav_layout = QHBoxLayout(nav_card)
        
        back_btn = QPushButton("⬅ חזרה לעמוד הראשי")
        back_btn.setStyleSheet("""
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
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.clicked.connect(self.go_home)
        
        nav_layout.addStretch()
        nav_layout.addWidget(back_btn)
        nav_layout.addStretch()
        
        self.layout.addWidget(nav_card)
        self.cards.append(nav_card)
        
        # Add spacer at the bottom
        self.layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def clear_layout(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def show_group_attendance(self, group):
        page = GroupAttendancePage(self.stacked_widget, group)
        self.stacked_widget.addWidget(page)
        self.stacked_widget.setCurrentWidget(page)

    def go_home(self):
        self.stacked_widget.setCurrentIndex(0)
