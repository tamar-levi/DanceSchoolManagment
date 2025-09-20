import flet as ft
import json
import os
from components.modern_dialog import ModernDialog
from components.form_fields import FormFields
from views.add_student_view import AddStudentView
from utils.students_data_manager import StudentsDataManager
from utils.manage_json import ManageJSON
import re
from datetime import datetime

class AddStudentPage:
    def __init__(self, page, navigation_callback, group_name):
        self.page = page
        self.navigation_callback = navigation_callback
        self.group_name = group_name

        self.dialog = ModernDialog(page)
        self.data_manager = StudentsDataManager()
        self.view = AddStudentView(self)
        
        base_dir = ManageJSON.get_appdata_path()
        data_dir = base_dir / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        self.joining_dates_file = data_dir / "joining_dates.json"

        self.layout = ft.Column(
            spacing=24,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            animate_opacity=300,
        )

        self.create_form_fields()
        self.show_add_student_form()
    
    def get_view(self):
        return ft.Container(
            content=self.layout,
            bgcolor=ft.Colors.WHITE,
            padding=ft.padding.all(32),
            expand=True
        )

    def create_form_fields(self):
        """Create all form input fields using FormFields factory"""
        self.name_input = FormFields.create_text_field(
            "שם התלמידה", "הכנסי שם מלא", ft.Icons.PERSON
        )

        self.id_input = FormFields.create_text_field(
            "תעודת זהות", "הכנסי מספר תעודת זהות",
            ft.Icons.BADGE, ft.KeyboardType.NUMBER
        )

        self.phone_input = FormFields.create_text_field(
            "מספר טלפון", "הכנסי מספר טלפון",
            ft.Icons.PHONE, ft.KeyboardType.PHONE
        )

        self.payment_status_dropdown = FormFields.create_dropdown(
            "סטטוס תשלום", ft.Icons.PAYMENT,
            ["חוב", "יתרת זכות", "שולם"], "חוב"
        )

        self.join_date_input = FormFields.create_date_field(
            "תאריך הצטרפות", ft.Icons.CALENDAR_TODAY
        )

        self.group_dropdown = FormFields.create_dropdown(
            "קבוצה", ft.Icons.GROUP, []
        )

        self.has_sister_checkbox = ft.Checkbox(label="יש לה אחות בחוג", value=False)

        self.load_groups()

    def load_groups(self):
        """Load groups and populate dropdown"""
        groups_data = self.data_manager.load_groups()
        
        if isinstance(groups_data, dict):
            groups = groups_data.get("groups", [])
        elif isinstance(groups_data, list):
            groups = groups_data
        else:
            groups = []
        
        group_names = [group["name"] for group in groups if isinstance(group, dict) and "name" in group]
        self.group_dropdown.options = [ft.dropdown.Option(name) for name in group_names]

        if self.group_name:
            self.group_dropdown.value = self.group_name

    def get_group_id_by_name(self, group_name):
        """Get group ID by group name"""
        try:
            groups_data = self.data_manager.load_groups()
            
            if isinstance(groups_data, dict):
                groups = groups_data.get("groups", [])
            elif isinstance(groups_data, list):
                groups = groups_data
            else:
                print("Groups data is neither dict nor list")
                return None
            
            for i, group in enumerate(groups):
                if not isinstance(group, dict):
                    continue
                    
                group_name_in_data = group.get("name", "")
                
                if group_name_in_data == group_name:
                    group_id = group.get("id")
                    if not group_id:
                        group_id = group_name.replace(" ", "_").replace("-", "_")
                    return group_id
            
            print(f"Group '{group_name}' not found") 
            return None
            
        except Exception as e:
            print(f"Error getting group ID: {e}")
            import traceback
            traceback.print_exc()
            return None

    def load_joining_dates(self):
        """Load joining dates from JSON file"""
        try:
            if not os.path.exists(self.joining_dates_file):
                os.makedirs(os.path.dirname(self.joining_dates_file), exist_ok=True)
                with open(self.joining_dates_file, 'w', encoding='utf-8') as f:
                    json.dump({}, f, ensure_ascii=False, indent=2)
                return {}
            
            with open(self.joining_dates_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading joining dates: {e}")
            return {}

    def save_joining_dates(self, joining_dates_data):
        """Save joining dates to JSON file"""
        try:
            os.makedirs(os.path.dirname(self.joining_dates_file), exist_ok=True)
            with open(self.joining_dates_file, 'w', encoding='utf-8') as f:
                json.dump(joining_dates_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving joining dates: {e}")
            return False

    def add_joining_date_record(self, group_id, student_name, student_id, join_date):
        """Add joining date record for student in specific group"""
        try:
            joining_dates_data = self.load_joining_dates()
            
            group_id_str = str(group_id)
            
            if group_id_str not in joining_dates_data:
                joining_dates_data[group_id_str] = []
            
            existing_student = None
            for student in joining_dates_data[group_id_str]:
                if student.get("student_id") == student_id:
                    existing_student = student
                    break
            
            if existing_student:
                existing_student["join_date"] = join_date
                existing_student["student_name"] = student_name
            else:
                joining_dates_data[group_id_str].append({
                    "student_id": student_id,
                    "student_name": student_name,
                    "join_date": join_date
                })
            
            success = self.save_joining_dates(joining_dates_data)
            return success
            
        except Exception as e:
            print(f"Error adding joining date record: {e}")
            import traceback
            traceback.print_exc()
            return False


    def show_add_student_form(self):
        """Show the add student form"""
        self.clear_layout()
        self.view.render()

    def add_student(self, e=None):
        """Add new student with validation"""
        form_data = self.get_form_data()

        if not self.validate_form(form_data):
            return

        if self.data_manager.student_exists_in_this_group(form_data["id"], form_data["group"]):
            self.dialog.show_error(f"תלמידה עם ת.ז. {form_data['id']} כבר קיימת במערכת")
            return

        group_id = self.get_group_id_by_name(form_data["group"])
        
        if not group_id:
            self.dialog.show_error(f"שגיאה בזיהוי הקבוצה '{form_data['group']}'. אנא בדקי שהקבוצה קיימת במערכת.")
            return

        if self.data_manager.add_student(form_data):
            joining_success = self.add_joining_date_record(
                group_id, 
                form_data["name"], 
                form_data["id"], 
                form_data["join_date"]
            )
            
            if joining_success:
                self.dialog.show_success(
                    "התלמידה נוספה בהצלחה למערכת!",
                    callback=self.go_back
                )
            else:
                self.dialog.show_success(
                    "התלמידה נוספה למערכת, אך הייתה בעיה בשמירת תאריך ההצטרפות",
                    callback=self.go_back
                )
        else:
            self.dialog.show_error("שגיאה בשמירת התלמידה")

    def get_form_data(self):
        """Get data from form fields"""
        return {
            "id": self.id_input.value.strip() if self.id_input.value else "",
            "name": self.name_input.value.strip() if self.name_input.value else "",
            "phone": self.phone_input.value.strip() if self.phone_input.value else "",
            "group": self.group_dropdown.value if self.group_dropdown.value else "",
            "payment_status": self.payment_status_dropdown.value if self.payment_status_dropdown.value else "",
            "join_date": self.join_date_input.value.strip() if self.join_date_input.value else "",
            "has_sister": self.has_sister_checkbox.value if self.has_sister_checkbox.value else False,
            "payments": []
        }


    def validate_form(self, form_data):
        """Validate form data"""
        required_fields = ["id", "name", "phone", "group", "payment_status", "join_date"]
        if not all(form_data.get(field) for field in required_fields):
            self.dialog.show_error("יש למלא את כל השדות הנדרשים")
            return False

        # תעודת זהות
        if not form_data["id"].isdigit() or len(form_data["id"]) != 9:
            self.dialog.show_error("מספר תעודת זהות חייב להכיל 9 ספרות בלבד")
            return False

        # תאריך הצטרפות
        join_date = form_data["join_date"].strip()
        try:
            datetime.strptime(join_date, "%d/%m/%Y")
        except ValueError:
            # נבדוק אם בכלל הפורמט לא נכון
            date_pattern = r'^\d{2}/\d{2}/\d{4}$'
            if not re.match(date_pattern, join_date):
                self.dialog.show_error("פורמט תאריך הצטרפות לא תקין — השתמשי ב־dd/mm/yyyy")
            else:
                self.dialog.show_error("תאריך הצטרפות לא קיים (בדקי יום/חודש/שנה)")
            return False

        return True


    def go_back(self, e=None):
        """Navigate back to students page"""
        from pages.students_page import StudentsPage
        students_page = StudentsPage(self.page, self.navigation_callback, self.group_name)
        self.navigation_callback(students_page)

    def clear_layout(self):
        """Clear the layout"""
        self.layout.controls.clear()