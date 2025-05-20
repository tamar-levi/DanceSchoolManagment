import json
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from students_page import StudentsPage
from add_group_page import AddGroupPage

class GroupsPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.add_group_page = None
        self.build_group_buttons()

    def build_group_buttons(self):
        self.clear_layout()
        
        title_label = QLabel("עמוד קבוצות")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #333; margin-bottom: 10px;")
        self.layout.addWidget(title_label)
        
        self.layout.addWidget(QLabel("בחרי קבוצה:"))

        try:
            with open("data/groups.json", encoding="utf-8") as f:
                data = json.load(f)
                groups = data.get("groups", [])
        except Exception as e:
            groups = []
            self.layout.addWidget(QLabel("שגיאה בטעינת קבוצות"))
            print("Error reading JSON file:", e)

        for group in groups:
            btn = QPushButton(group["name"])
            btn.setStyleSheet("""
                QPushButton {
                    background-color: grey; 
                    padding: 10px; 
                    font-size: 14px;
                    border-radius: 4px;
                    margin: 3px 0;
                }
                QPushButton:hover {
                    background-color: grey;
                }
            """)
            btn.clicked.connect(lambda _, name=group["name"]: self.show_students(name))
            self.layout.addWidget(btn)

        add_group_button = QPushButton("➕ הוסף קבוצה")
        add_group_button.setStyleSheet("""
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
        add_group_button.clicked.connect(self.add_group_page_func)
        self.layout.addWidget(add_group_button)

        back_btn = QPushButton("⬅ חזרה לעמוד הראשי")
        back_btn.setStyleSheet("""
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
        back_btn.clicked.connect(self.go_home)
        self.layout.addWidget(back_btn)

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
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
