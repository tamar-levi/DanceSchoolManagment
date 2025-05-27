import json
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QGridLayout, QScrollArea
from PyQt5.QtCore import Qt
from students_page import StudentsPage
from add_group_page import AddGroupPage

class GroupsPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        
        # שימוש בלייאאוט ראשי אנכי
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # # תווית משנה
        subtitle_label = QLabel("כל הקבוצות:")
        subtitle_label.setStyleSheet("font-size: 16px; color: #555; margin-bottom: 10px;")
        subtitle_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle_label)
        
        # אזור גלילה לקבוצות
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none;")
        
        # מיכל לכפתורי הקבוצות
        groups_container = QWidget()
        self.groups_layout = QGridLayout(groups_container)
        self.groups_layout.setAlignment(Qt.AlignCenter)
        self.groups_layout.setSpacing(10)
        
        scroll_area.setWidget(groups_container)
        main_layout.addWidget(scroll_area, 1)  # הוספת מקדם מתיחה
        
        # אזור כפתורי פעולה בתחתית המסך
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        # כפתור הוספת קבוצה
        add_group_button = QPushButton("➕ הוסף קבוצה")
        add_group_button.setStyleSheet("""
             QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        add_group_button.clicked.connect(self.add_group_page_func)
        
        # הוספת הכפתורים ללייאאוט התחתון
        buttons_layout.addWidget(add_group_button)
        # buttons_layout.addWidget(back_btn)
        
        # הוספת לייאאוט הכפתורים ללייאאוט הראשי
        main_layout.addLayout(buttons_layout)
        
        self.add_group_page = None
        self.build_group_buttons()

    def build_group_buttons(self):
        # ניקוי הלייאאוט הקיים של הקבוצות
        while self.groups_layout.count():
            item = self.groups_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        try:
            with open("data/groups.json", encoding="utf-8") as f:
                data = json.load(f)
                groups = data.get("groups", [])
        except Exception as e:
            groups = []
            error_label = QLabel("שגיאה בטעינת קבוצות")
            error_label.setStyleSheet("color: red; font-weight: bold;")
            self.groups_layout.addWidget(error_label, 0, 0)
            print("Error reading JSON file:", e)
            return

        # סידור הקבוצות ברשת (גריד)
        row, col = 0, 0
        max_cols = 3  # מספר העמודות ברשת
        
        for group in groups:
            btn = QPushButton(group["name"])
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db; 
                    color: white;
                    padding: 15px; 
                    font-size: 16px;
                    border-radius: 8px;
                    min-width: 150px;
                    min-height: 60px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            btn.clicked.connect(lambda _, name=group["name"]: self.show_students(name))
            
            self.groups_layout.addWidget(btn, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

    def show_students(self, group_name):
        students_page = StudentsPage(self.stacked_widget, group_name)
        self.stacked_widget.addWidget(students_page)
        self.stacked_widget.setCurrentWidget(students_page)

    def go_home(self):
        self.stacked_widget.setCurrentIndex(0)

    def add_group_page_func(self):
        if self.add_group_page is None:
            self.add_group_page = AddGroupPage(self.stacked_widget, self)
            self.stacked_widget.addWidget(self.add_group_page)
        self.stacked_widget.setCurrentWidget(self.add_group_page)

    def refresh(self):
        self.build_group_buttons()

    def clear_layout(self):
        pass
