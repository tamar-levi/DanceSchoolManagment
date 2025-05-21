import json
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QLabel,
    QHeaderView, QLineEdit, QMessageBox, QSizePolicy, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor, QBrush

class StudentsListPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.all_students = self.load_students()

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Title
        title = QLabel("📋 רשימת התלמידות")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            margin: 12px;
            color: #2c3e50;
        """)
        main_layout.addWidget(title)

        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 חיפוש לפי שם, קבוצה, טלפון או כל דבר אחר...")
        self.search_input.setStyleSheet("""
            padding: 6px;
            font-size: 14px;
            border: 2px solid #3498db;
            border-radius: 8px;
        """)
        self.search_input.setMaximumWidth(600)
        self.search_input.textChanged.connect(self.filter_table)

        search_layout = QHBoxLayout()
        search_layout.setAlignment(Qt.AlignCenter)
        search_layout.addWidget(self.search_input)
        main_layout.addLayout(search_layout)

        # Table setup
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "🆔 ת.ז", "📱 טלפון", "👥 קבוצה", "💰 סטטוס תשלום", "📅 תאריך הצטרפות", "📄 תשלומים"
        ])
        self.table.setLayoutDirection(Qt.RightToLeft)
        
        # Fixed column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        self.table.verticalHeader().setDefaultAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.table.setWordWrap(True)
        self.table.setAlternatingRowColors(True)
        
        # Force table to take all available space
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #bdc3c7;
                font-size: 13px;
                background-color: #ecf0f1;
                alternate-background-color: #dfe6e9;
                border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #2980b9;
                color: white;
                font-weight: bold;
                padding: 6px;
                border: none;
            }
        """)

        # Add table to main layout with stretch factor
        main_layout.addWidget(self.table, 1)
        
        self.populate_table(self.all_students)

    def load_students(self):
        try:
            base_dir = os.path.dirname(__file__)
            json_path = os.path.abspath(os.path.join(base_dir, 'data', 'students.json'))
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("students", [])
        except Exception as e:
            print(f"שגיאה בטעינת students.json: {e}")
            return []

    def populate_table(self, students):
        # Block signals temporarily to prevent layout changes
        self.table.blockSignals(True)
        
        self.table.clearContents()
        if not students:
            self.table.setRowCount(0)

            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("אין תוצאות")
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText(" לא נמצאה אף תלמידה התואמת לדרישות החיפוש❗")
            msg_box.setStyleSheet("""
                QMessageBox {
                    font-size: 16px;
                }
                QLabel {
                    color: #c0392b;
                    font-weight: bold;
                    font-size: 18px;
                }
            """)
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
            
            self.table.blockSignals(False)
            return

        self.table.setRowCount(len(students))
        self.table.setVerticalHeaderLabels([s['name'] for s in students])

        for row, student in enumerate(students):
            data = [
                student.get("id", ""),
                student.get("phone", ""),
                student.get("group", ""),
                student.get("payment_status", ""),
                student.get("join_date", "")
            ]

            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, col, item)

            payments = student.get("payments", [])
            payments_str = "\n".join(
                f"{p['amount']}₪ ב־{p['date']} ({p['payment_method']})"
                for p in payments
            )
            payments_item = QTableWidgetItem(payments_str)
            payments_item.setFlags(payments_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 5, payments_item)
        
        # Only adjust row heights for content
        self.table.resizeRowsToContents()
        
        # Unblock signals
        self.table.blockSignals(False)

    def filter_table(self):
        query = self.search_input.text().lower()
        filtered = [
            s for s in self.all_students
            if query in json.dumps(s, ensure_ascii=False).lower()
        ]
        self.populate_table(filtered)
