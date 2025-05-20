import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QFrame, QSizePolicy, QGraphicsDropShadowEffect, QMainWindow,
    QToolButton, QScrollArea
)
from PyQt5.QtCore import (
    Qt, QPropertyAnimation, QPoint, QSize, QEasingCurve, QRect, 
    QParallelAnimationGroup,  QTimer, QEvent, pyqtProperty as Property
)

from PyQt5.QtGui import (
    QIcon, QFont, QColor, QPixmap, QPainter, QPen, QBrush,QFontDatabase
)

from groups_page import GroupsPage
from attendance_page import AttendancePage
from payment_page import PaymentPage


# Load custom fonts
def load_fonts():
    font_dir = "fonts"
    if os.path.exists(font_dir):
        for font_file in os.listdir(font_dir):
            if font_file.endswith(('.ttf', '.otf')):
                QFontDatabase.addApplicationFont(os.path.join(font_dir, font_file))

# Animated toggle button (like in Docker Desktop)
class AnimatedToggle(QToolButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self._bg_color = QColor("#777")
        self._bg_color_checked = QColor("#0078d7")
        self._circle_color = QColor("#ffffff")
        self._circle_position = 0
        self.animation = QPropertyAnimation(self, b"circle_position")
        self.animation.setDuration(150)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.toggled.connect(self.start_animation)
        self.setFixedSize(50, 26)

    def start_animation(self, checked):
        self.animation.stop()
        self.animation.setStartValue(0 if checked else 1)
        self.animation.setEndValue(1 if checked else 0)
        self.animation.start()

    def get_circle_position(self):
        return self._circle_position

    def set_circle_position(self, pos):
        self._circle_position = pos
        self.update()

    circle_position = Property(float, get_circle_position, set_circle_position)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        
        # Draw background
        track_opacity = 0.8
        track_brush = QBrush(self._bg_color_checked if self.isChecked() else self._bg_color)
        p.setOpacity(track_opacity)
        track_pen = QPen(Qt.NoPen)
        p.setPen(track_pen)
        p.setBrush(track_brush)
        track_height = 16
        p.drawRoundedRect(0, (self.height() - track_height) // 2, 
        self.width(), track_height, 8, 8)
        
        # Draw circle/handle
        p.setOpacity(1.0)
        p.setBrush(QBrush(self._circle_color))
        circle_radius = 11
        circle_x = self._circle_position * (self.width() - 2 * circle_radius) + circle_radius
        p.drawEllipse(QPoint(int(circle_x), self.height() // 2), circle_radius, circle_radius)

# Animated sidebar button with hover effects
class AnimatedSidebarButton(QToolButton):
    def __init__(self, text, icon_name=None, parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.setCheckable(True)
        self.setAutoExclusive(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(50)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Set icon if provided
        if icon_name:
            icon_path = f"icons/{icon_name}.png"
            if os.path.exists(icon_path):
                self.setIcon(QIcon(icon_path))
            else:
                self.setIcon(QIcon.fromTheme(icon_name))
            
            self.setIconSize(QSize(22, 22))
        
        # Hover animation properties
        self._hover_progress = 0.0
        self._animation = QPropertyAnimation(self, b"hover_progress")
        self._animation.setDuration(200)
        self._animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        # Install event filter for hover events
        self.installEventFilter(self)
        
        # Apply style
        self.setStyleSheet("""
            AnimatedSidebarButton {
                background-color: transparent;
                color: #b3b8c3;
                font-size: 14px;
                font-weight: normal;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                text-align: left;
            }
            AnimatedSidebarButton:checked {
                color: #ffffff;
                font-weight: bold;
            }
        """)

    def eventFilter(self, obj, event):
        if obj == self:
            if event.type() == QEvent.Enter:
                self.start_hover_animation(True)
            elif event.type() == QEvent.Leave:
                self.start_hover_animation(False)
        return super().eventFilter(obj, event)

    def start_hover_animation(self, hover):
        self._animation.stop()
        self._animation.setStartValue(self._hover_progress)
        self._animation.setEndValue(1.0 if hover else 0.0)
        self._animation.start()

    def get_hover_progress(self):
        return self._hover_progress

    def set_hover_progress(self, progress):
        self._hover_progress = progress
        self.update()

    hover_progress = Property(float, get_hover_progress, set_hover_progress)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw background based on hover state and checked state
        if self.isChecked():
            bg_color = QColor(255, 255, 255, 40)
            painter.setBrush(QBrush(bg_color))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(self.rect(), 4, 4)
        elif self._hover_progress > 0:
            bg_color = QColor(255, 255, 255, int(30 * self._hover_progress))
            painter.setBrush(QBrush(bg_color))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(self.rect(), 4, 4)
        
        # Draw left indicator for selected item
        if self.isChecked():
            indicator_color = QColor("#0078d7")
            painter.setBrush(QBrush(indicator_color))
            painter.setPen(Qt.NoPen)
            indicator_rect = QRect(0, 10, 4, self.height() - 20)
            painter.drawRoundedRect(indicator_rect, 2, 2)
        
        # Let the QToolButton draw the icon and text
        # painter.end()
        super().paintEvent(event)

# Card widget with hover effects and animations
class AnimatedCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.NoFrame)
        self.setCursor(Qt.PointingHandCursor)
        
        # Shadow effect
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QColor(0, 0, 0, 30))
        self.shadow.setOffset(0, 4)
        self.setGraphicsEffect(self.shadow)
        
        # Hover animation properties
        self._hover = False
        self._animation = QPropertyAnimation(self.shadow, b"blurRadius")
        self._animation.setDuration(200)
        
        # הוספת אנימציית התזוזה כאן במקום ליצור אותה בכל פעם מחדש
        self.move_animation = QPropertyAnimation(self, b"pos")
        self.move_animation.setDuration(200)
        self.move_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # Install event filter for hover events
        self.installEventFilter(self)
        
        # Style
        self.setStyleSheet("""
            AnimatedCard {
                background-color: #ffffff;
                border-radius: 8px;
                border: none;
            }
        """)


    def eventFilter(self, obj, event):
        if obj == self:
            if event.type() == QEvent.Enter:
                self.start_hover_animation(True)
            elif event.type() == QEvent.Leave:
                self.start_hover_animation(False)
        return super().eventFilter(obj, event)

    def start_hover_animation(self, hover):
        self._hover = hover
        self._animation.stop()
        
        if hover:
            self._animation.setStartValue(15)
            self._animation.setEndValue(25)
            self.shadow.setColor(QColor(0, 0, 0, 60))
            
            # Create translation animation for slight "lift" effect
            self.move_animation.stop()
            self.move_animation.setStartValue(self.pos())
            self.move_animation.setEndValue(self.pos() - QPoint(0, 5))
            self.move_animation.start()
        else:
            self._animation.setStartValue(25)
            self._animation.setEndValue(15)
            self.shadow.setColor(QColor(0, 0, 0, 30))
            
            # Create translation animation to return to original position
            self.move_animation.stop()
            self.move_animation.setStartValue(self.pos())
            self.move_animation.setEndValue(self.pos() + QPoint(0, 5))
            self.move_animation.start()

        self._animation.start()

# Circular progress indicator
class CircularProgress(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(120, 120)
        self._progress = 75  # Default value
        self._color = QColor("#0078d7")
        
        # Animation
        self._animation = QPropertyAnimation(self, b"progress")
        self._animation.setDuration(1000)
        self._animation.setEasingCurve(QEasingCurve.OutCubic)

    def get_progress(self):
        return self._progress

    def set_progress(self, value):
        self._progress = value
        self.update()

    progress = Property(int, get_progress, set_progress)

    def animate_progress(self, start, end):
        self._animation.stop()
        self._animation.setStartValue(start)
        self._animation.setEndValue(end)
        self._animation.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Calculate sizes
        width = min(self.width(), self.height())
        outer_radius = width / 2
        inner_radius = outer_radius * 0.75
        center = self.rect().center()
        
        # Draw background circle
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#e0e0e0"))
        painter.drawEllipse(center, outer_radius, outer_radius)
        
        # Draw progress arc
        pen = QPen(self._color)
        pen.setWidth(int(outer_radius - inner_radius))
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        
        # Calculate span angle for progress
        span_angle = -self._progress * 360 / 100
        
        # Draw arc
        rect = QRect(
            int(center.x() - outer_radius),
            int(center.y() - outer_radius),
            int(outer_radius * 2),
            int(outer_radius * 2)
        )
        painter.drawArc(rect, 90 * 16, int(span_angle * 16))
        
        # Draw text
        painter.setPen(QColor("#333333"))
        font = painter.font()
        font.setPointSize(14)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignCenter, f"{self._progress}%")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()        
        load_fonts()        
        self.setWindowTitle('זה הריקוד שלך')
        self.resize(1200, 800)
        self.setMinimumSize(1000, 700)
        app_font = QFont("Segoe UI", 10)
        QApplication.setFont(app_font)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar)
        
        self.content_area = QScrollArea()
        self.content_area.setWidgetResizable(True)
        self.content_area.setFrameShape(QFrame.NoFrame)
        self.content_area.setStyleSheet("""
        QScrollArea {
            border: none;
            background-color: #f5f7fa;
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

    # Create content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)
        self.content_area.setWidget(content_widget)
        
        # Create stacked widget for different pages
        self.stack = QStackedWidget()
        content_layout.addWidget(self.stack)
        
        # Create pages
        self.home_page = self.create_home_page()
        self.groups_page = GroupsPage(self.stack)
        self.attendance_page = AttendancePage(self.stack)
        self.payment_page = PaymentPage(self.stack)

    def create_home_page(self):
        
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(30)
        
        # Add welcome section
        welcome_card = AnimatedCard()
        welcome_layout = QVBoxLayout(welcome_card)
        
        welcome_title = QLabel("ברוכים הבאים לזה הריקוד שלך")
        welcome_title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        welcome_title.setAlignment(Qt.AlignCenter)
        
        welcome_subtitle = QLabel("הבית המקצועי לבלט")
        welcome_subtitle.setStyleSheet("font-size: 16px; color: #7f8c8d;")
        welcome_subtitle.setAlignment(Qt.AlignCenter)
        
        welcome_layout.addWidget(welcome_title)
        welcome_layout.addWidget(welcome_subtitle)
        
        # Add welcome image
        image_label = QLabel()
        logo_path = "icons/logo.png"
        if os.path.exists(logo_path):
            logo_pixmap = QPixmap(logo_path).scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label.setPixmap(logo_pixmap)
            image_label.setAlignment(Qt.AlignCenter)
            welcome_layout.addWidget(image_label)
        
        layout.addWidget(welcome_card)
        
        # Add stats section
        stats_container = QWidget()
        stats_layout = QHBoxLayout(stats_container)
        stats_layout.setSpacing(20)
        
        # Students card
        students_card = AnimatedCard()
        students_layout = QVBoxLayout(students_card)
        
        students_title = QLabel("תלמידות")
        students_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        
        students_count = QLabel("42")
        students_count.setStyleSheet("font-size: 36px; font-weight: bold; color: #e74c3c;")
        
        students_layout.addWidget(students_title)
        students_layout.addWidget(students_count)
        
        # Groups card
        groups_card = AnimatedCard()
        groups_layout = QVBoxLayout(groups_card)
        
        groups_title = QLabel("קבוצות")
        groups_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        
        groups_count = QLabel("8")
        groups_count.setStyleSheet("font-size: 36px; font-weight: bold; color: #3498db;")
        
        groups_layout.addWidget(groups_title)
        groups_layout.addWidget(groups_count)
        
        # Payments card
        payments_card = AnimatedCard()
        payments_layout = QVBoxLayout(payments_card)
        
        payments_title = QLabel("תשלומים החודש")
        payments_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        
        payments_amount = QLabel("₪ 12,450")
        payments_amount.setStyleSheet("font-size: 36px; font-weight: bold; color: #2ecc71;")
        
        payments_layout.addWidget(payments_title)
        payments_layout.addWidget(payments_amount)
        
        stats_layout.addWidget(students_card)
        stats_layout.addWidget(groups_card)
        stats_layout.addWidget(payments_card)
        
        layout.addWidget(stats_container)
        
        # Add attendance progress
        progress_card = AnimatedCard()
        progress_layout = QHBoxLayout(progress_card)
        
        progress_info = QVBoxLayout()
        progress_title = QLabel("נוכחות חודשית")
        progress_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        progress_subtitle = QLabel("ממוצע נוכחות בכל הקבוצות")
        progress_subtitle.setStyleSheet("font-size: 14px; color: #7f8c8d;")
        
        progress_info.addWidget(progress_title)
        progress_info.addWidget(progress_subtitle)
        progress_info.addStretch()
        
        progress_circle = CircularProgress()
        # Animate progress on page load
        QTimer.singleShot(500, lambda: progress_circle.animate_progress(0, 75))
        
        progress_layout.addLayout(progress_info)
        progress_layout.addWidget(progress_circle)
        
        layout.addWidget(progress_card)
        
        # Add quick actions
        actions_card = AnimatedCard()
        actions_layout = QVBoxLayout(actions_card)
        
        actions_title = QLabel("פעולות מהירות")
        actions_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        actions_layout.addWidget(actions_title)
        
        buttons_layout = QHBoxLayout()
        
        add_student_btn = QPushButton("הוספת תלמידה")
        add_student_btn.setStyleSheet("""
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
        add_student_btn.setCursor(Qt.PointingHandCursor)
        add_student_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        
        add_group_btn = QPushButton("הוספת קבוצה")
        add_group_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        add_group_btn.setCursor(Qt.PointingHandCursor)
        add_group_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))

        record_payment_btn = QPushButton("רישום תשלום")
        record_payment_btn.setStyleSheet("""
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
        record_payment_btn.setCursor(Qt.PointingHandCursor)
        add_group_btn.clicked.connect(lambda: self.stack.setCurrentIndex(3))

        buttons_layout.addWidget(add_student_btn)
        buttons_layout.addWidget(add_group_btn)
        buttons_layout.addWidget(record_payment_btn)
        
        actions_layout.addLayout(buttons_layout)
        
        layout.addWidget(actions_card)
        
        # Add stretcher to push content to the top
        layout.addStretch()
        
        return page
    def run_entrance_animation(self):
    # Animate sidebar entrance
        sidebar_animation = QPropertyAnimation(self.sidebar, b"pos")
        sidebar_animation.setDuration(500)
        sidebar_animation.setStartValue(QPoint(-self.sidebar.width(), 0))
        sidebar_animation.setEndValue(QPoint(0, 0))
        sidebar_animation.setEasingCurve(QEasingCurve.OutCubic)

        # Run animations in parallel
        animation_group = QParallelAnimationGroup()
        animation_group.addAnimation(sidebar_animation)
        animation_group.start()


    def toggle_dark_mode(self, enabled):
        if enabled:
            # Apply dark theme
            self.content_area.setStyleSheet("""
                QWidget {
                    background-color: #1e1e1e;
                    color: #ffffff;
                }
                QLabel {
                    color: #ffffff;
                }
                QScrollArea {
                    border: none;
                    background-color: transparent;
                }
                QScrollBar:vertical {
                    border: none;
                    background: #2d2d2d;
                    width: 10px;
                    margin: 0px;
                }
                QScrollBar::handle:vertical {
                    background: #3d3d3d;
                    min-height: 20px;
                    border-radius: 5px;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    border: none;
                    background: none;
                }
            """)
            
            # Update card styles
            for card in self.findChildren(AnimatedCard):
                card.setStyleSheet("""
                    AnimatedCard {
                        background-color: #2d2d2d;
                        border-radius: 8px;
                        border: none;
                    }
                """)
                
            # Update labels in cards
            for card in self.findChildren(AnimatedCard):
                for label in card.findChildren(QLabel):
                    if "font-weight: bold" in label.styleSheet():
                        label.setStyleSheet(label.styleSheet().replace("color: #2c3e50", "color: #ecf0f1"))
                    elif "color: #7f8c8d" in label.styleSheet():
                        label.setStyleSheet(label.styleSheet().replace("color: #7f8c8d", "color: #bdc3c7"))
        else:
            # Apply light theme
            self.content_area.setStyleSheet("""
                QWidget {
                    background-color: #f5f7fa;
                    color: #2c3e50;
                }
                QLabel {
                    color: #2c3e50;
                }
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
            
            # Update card styles
            for card in self.findChildren(AnimatedCard):
                card.setStyleSheet("""
                    AnimatedCard {
                        background-color: #ffffff;
                        border-radius: 8px;
                        border: none;
                    }
                """)
                
            # Update labels in cards
            for card in self.findChildren(AnimatedCard):
                for label in card.findChildren(QLabel):
                    if "font-weight: bold" in label.styleSheet():
                        label.setStyleSheet(label.styleSheet().replace("color: #ecf0f1", "color: #2c3e50"))
                    elif "color: #bdc3c7" in label.styleSheet():
                        label.setStyleSheet(label.styleSheet().replace("color: #bdc3c7", "color: #7f8c8d"))

if __name__ == '__main__':
    # Create application
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Set RTL layout direction for Hebrew
    app.setLayoutDirection(Qt.RightToLeft)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec_())
