import json
import os
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QPushButton, 
    QHBoxLayout, QFrame, QTableWidget, 
    QTableWidgetItem, QHeaderView, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint, QTimer, QEasingCurve
from PyQt5.QtGui import QFont, QColor, QBrush

class AnimatedCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.NoFrame)
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

class PaymentPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.cards = []
        self.payments_data = []
        
        self.init_ui()
        self.load_payments()
        self.display_payments()
        QTimer.singleShot(100, self.run_entrance_animation)

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        self.setLayout(main_layout)
        
        # Header card
        header_card = AnimatedCard()
        header_layout = QVBoxLayout(header_card)
        
        title = QLabel("ניהול תשלומים")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        
        subtitle = QLabel("רשימת כל התשלומים במערכת")
        subtitle.setFont(QFont("Segoe UI", 16))
        subtitle.setStyleSheet("color: #7f8c8d;")
        subtitle.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitle)
        
        main_layout.addWidget(header_card)
        self.cards.append(header_card)
        
        # Payments table card
        payments_card = AnimatedCard()
        payments_layout = QVBoxLayout(payments_card)
        payments_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create table for payments with MongoDB/Docker Desktop inspired style
        self.payments_table = QTableWidget()
        self.payments_table.setColumnCount(5)
        self.payments_table.setHorizontalHeaderLabels(["שם התלמיד", "סכום", "תאריך", "אמצעי תשלום", "קבוצה"])
        self.payments_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.payments_table.setAlternatingRowColors(True)
        self.payments_table.setShowGrid(False)
        self.payments_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.payments_table.verticalHeader().setVisible(False)
        self.payments_table.setSelectionMode(QTableWidget.NoSelection)
        self.payments_table.setFocusPolicy(Qt.NoFocus)
        self.payments_table.setLayoutDirection(Qt.RightToLeft)

        # MongoDB/Docker Desktop inspired style
        self.payments_table.setStyleSheet("""
           QTableWidget {
                background-color: #f8f9fa;
                border-radius: 8px;
                border: none;
                padding: 5px;
                gridline-color: transparent;
            }

            QTableWidget::item {
                padding: 12px 8px;
                border-bottom: 1px solid #eceff1;
                border-radius: 4px;
            }

            QTableWidget::item:selected {
                background-color: transparent;
                color: black;
            }

            QTableWidget::item:hover {
                background-color: transparent;
            }

            QHeaderView::section {
                background-color: #3498db;
                color: white;
                font-weight: bold;
                padding: 12px 8px;
                border: none;
                border-radius: 0px;
                border-right: 1px solid #2980b9;
            }

            QHeaderView::section:first {
                border-top-left-radius: 8px;
            }

            QHeaderView::section:last {
                border-top-right-radius: 8px;
                border-right: none;
            }

            QTableWidget QTableCornerButton::section {
                background-color: #3498db;
                border: none;
            }

            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 8px;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical {
                background: #bdc3c7;
                min-height: 20px;
                border-radius: 4px;
            }

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
            }

            QScrollBar:horizontal {
                border: none;
                background: #f0f0f0;
                height: 8px;
                border-radius: 4px;
            }

            QScrollBar::handle:horizontal {
                background: #bdc3c7;
                min-width: 20px;
                border-radius: 4px;
            }

            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                border: none;
                background: none;
                width: 0px;
            }
        """)
        
        payments_layout.addWidget(self.payments_table)
        
        # Add summary label
        self.summary_label = QLabel()
        self.summary_label.setFont(QFont("Segoe UI", 12))
        self.summary_label.setStyleSheet("color: #7f8c8d; margin-top: 10px;")
        self.summary_label.setAlignment(Qt.AlignCenter)
        payments_layout.addWidget(self.summary_label)
        
        main_layout.addWidget(payments_card)
        self.cards.append(payments_card)
        
        # Bottom buttons card
        buttons_card = AnimatedCard()
        buttons_layout = QHBoxLayout(buttons_card)
        
        buttons_layout.addStretch()
        
        back_btn = QPushButton("חזרה לעמוד הראשי")
        back_btn.clicked.connect(self.go_home)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        buttons_layout.addWidget(back_btn)
        
        main_layout.addWidget(buttons_card)
        self.cards.append(buttons_card)

    def load_payments(self):
        try:
            if os.path.exists("data/students.json"):
                with open("data/students.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                    # Extract all payments
                    for student in data.get("students", []):
                        student_name = student.get("name", "")
                        group_name = student.get("group", "")
                        
                        for payment in student.get("payments", []):
                            self.payments_data.append({
                                "student_name": student_name,
                                "amount": payment.get("amount", "0"),
                                "date": payment.get("date", ""),
                                "payment_method": payment.get("payment_method", ""),
                                "group": group_name
                            })
        except Exception as e:
            print(f"Error loading payments: {e}")

    def display_payments(self):
        # Clear existing table
        self.payments_table.setRowCount(0)
        
        # Add payments to table
        if not self.payments_data:
            return
            
        total_amount = 0
        payment_methods = {}
        
        for i, payment in enumerate(self.payments_data):
            self.payments_table.insertRow(i)
            
            self.payments_table.setItem(i, 0, QTableWidgetItem(payment["student_name"]))
            
            amount_item = QTableWidgetItem(f"{payment['amount']}₪")
            amount_item.setForeground(QBrush(QColor("#2ecc71")))
            self.payments_table.setItem(i, 1, amount_item)
            try:
                total_amount += float(payment["amount"])
            except ValueError:
                pass
                
            method = payment["payment_method"]
            payment_methods[method] = payment_methods.get(method, 0) + 1
            
            self.payments_table.setItem(i, 2, QTableWidgetItem(payment["date"]))
            
            # Style payment method based on type
            method_item = QTableWidgetItem(payment["payment_method"])
            if payment["payment_method"] == "מזומן":
                method_item.setForeground(QBrush(QColor("#3498db")))  # Blue for cash
            elif payment["payment_method"] == "אשראי":
                method_item.setForeground(QBrush(QColor("#9b59b6")))  # Purple for credit
            self.payments_table.setItem(i, 3, method_item)
            
            self.payments_table.setItem(i, 4, QTableWidgetItem(payment["group"]))
            
            # Right align text in cells
            for j in range(5):
                item = self.payments_table.item(i, j)
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                
        # Update summary label
        methods_summary = ", ".join([f"{count} {method}" for method, count in payment_methods.items()])
        self.summary_label.setText(f"סה״כ: {total_amount}₪ ({len(self.payments_data)} תשלומים, {methods_summary})")

    def run_entrance_animation(self):
        for i, card in enumerate(self.cards):
            animation = QPropertyAnimation(card, b"pos")
            animation.setDuration(500)
            animation.setStartValue(card.pos() + QPoint(0, 50))
            animation.setEndValue(card.pos())
            animation.setEasingCurve(QEasingCurve.OutCubic)
            
            # Use QTimer to delay the start of animation
            QTimer.singleShot(i * 100, animation.start)

    def go_home(self):
        self.stacked_widget.setCurrentIndex(0)
