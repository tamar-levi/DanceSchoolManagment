import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox

class AddGroupPage(QWidget):
    def __init__(self, stacked_widget, groups_page):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.groups_page = groups_page  # קבלת הפניה לעמוד הקבוצות

        self.layout = QVBoxLayout()
        self.layout.setSpacing(6)  # צמצום רווחים בין שדות
        self.setLayout(self.layout)

        self.group_name_input = QLineEdit()
        self.group_name_input.setPlaceholderText("שם הקבוצה")
        self.layout.addWidget(self.group_name_input)

        self.group_location_input = QLineEdit()
        self.group_location_input.setPlaceholderText("מיקום הקבוצה")
        self.layout.addWidget(self.group_location_input)

        self.group_price_input = QLineEdit()
        self.group_price_input.setPlaceholderText("עלות הקבוצה")
        self.layout.addWidget(self.group_price_input)

        self.group_price_input = QLineEdit()
        self.group_price_input.setPlaceholderText("קבוצת גילאים")
        self.layout.addWidget(self.group_price_input)

        self.group_price_input = QLineEdit()
        self.group_price_input.setPlaceholderText("שם המורה")
        self.layout.addWidget(self.group_price_input)

        self.save_button = QPushButton("שמור קבוצה")
        self.save_button.clicked.connect(self.save_group)
        self.layout.addWidget(self.save_button)

        self.back_button = QPushButton("⬅ חזרה לעמוד הקבוצות")
        self.back_button.clicked.connect(self.go_back)
        self.layout.addWidget(self.back_button)

    def save_group(self):
        name = self.group_name_input.text().strip()
        location = self.group_location_input.text().strip()
        price = self.group_price_input.text().strip()

        if not name or not location or not price:
            QMessageBox.warning(self, "שגיאה", "נא למלא את כל השדות.")
            return

        try:
            with open("data/groups.json", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {"groups": []}

        # יצירת ID חדש
        existing_ids = [group.get("id", 0) for group in data.get("groups", [])]
        new_id = max(existing_ids) + 1 if existing_ids else 1

        new_group = {
            "name": name,
            "location": location,
            "price": price,
            "id": new_id
        }

        data["groups"].append(new_group)

        try:
            with open("data/groups.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            QMessageBox.information(self, "הצלחה", "הקבוצה נוספה בהצלחה!")
            self.group_name_input.clear()
            self.group_location_input.clear()
            self.group_price_input.clear()
            self.go_back()
        except Exception as e:
            QMessageBox.critical(self, "שגיאה", f"שגיאה בשמירת הקובץ: {e}")

    def go_back(self):
        self.groups_page.build_group_buttons()  # רענון הקבוצות
        self.stacked_widget.setCurrentWidget(self.groups_page)
