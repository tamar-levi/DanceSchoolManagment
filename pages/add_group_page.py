import flet as ft
from utils.groups_data_manager import GroupsDataManager
from utils.add_group_validator import AddGroupValidator
from components.add_group_components import AddGroupComponents

class AddGroupPage:
    
    def __init__(self, page, navigation_callback, groups_page):
        self.page = page
        self.navigation_callback = navigation_callback
        self.groups_page = groups_page
        self.data_manager = GroupsDataManager()

        self.form_state = {
            'name': '', 'location': '', 'price': '', 'age': '',
            'teacher': '', 'start_date': '', 'end_date': '', 'day_of_week': '',
            'phone': '', 'email': '',
        }

        self.required_fields = {
            'name': 'שם הקבוצה', 'location': 'מיקום', 'price': 'מחיר לחודש',
            'age': 'קבוצת גיל', 'teacher': 'מורה/מדריך',
            'start_date': 'תאריך התחלה', 'end_date': 'תאריך סיום', 'day_of_week': 'יום בשבוע'
        }

        self.validation_errors = {}
        self.form_fields = self._create_form_fields()
        self.main_layout = self._render()

    def _create_form_fields(self):
        """Create form fields"""
        return {
            'name': AddGroupComponents.create_text_field(
                "שם הקבוצה *", "הכנס שם קבוצה", ft.Icons.BADGE_OUTLINED,
                'name', required=True, on_change=self._handle_field_change, on_blur=self._validate_field
            ),
            'location': AddGroupComponents.create_text_field(
                "מיקום *", "מיקום הקבוצה", ft.Icons.LOCATION_ON_OUTLINED,
                'location', required=True, on_change=self._handle_field_change, on_blur=self._validate_field
            ),
            'price': AddGroupComponents.create_text_field(
                "מחיר לחודש *", "מחיר לחודש", ft.Icons.PAYMENTS_OUTLINED,
                'price', suffix="₪", keyboard_type=ft.KeyboardType.NUMBER, required=True,
                on_change=self._handle_field_change, on_blur=self._validate_field
            ),
            'age': AddGroupComponents.create_text_field(
                "קבוצת גיל *", "טווח גילאים (לדוג' 6-8)", ft.Icons.GROUPS_OUTLINED,
                'age', required=True, on_change=self._handle_field_change, on_blur=self._validate_field
            ),
            'teacher': AddGroupComponents.create_text_field(
                "מורה/מדריך *", "שם המורה או המדריך", ft.Icons.PERSON_OUTLINE,
                'teacher', required=True, on_change=self._handle_field_change, on_blur=self._validate_field
            ),
            'start_date': AddGroupComponents.create_text_field(
                "תאריך התחלה *", "dd/mm/yyyy", ft.Icons.DATE_RANGE_OUTLINED,
                'start_date', required=True, on_change=self._handle_field_change, on_blur=self._validate_field
            ),
            'end_date': AddGroupComponents.create_text_field(
                "תאריך סיום *", "dd/mm/yyyy", ft.Icons.EVENT_OUTLINED,
                'end_date', required=True, on_change=self._handle_field_change, on_blur=self._validate_field
            ),
            'day_of_week': AddGroupComponents.create_text_field(
                "יום בשבוע *", "לדוג' ראשון, שני, שלישי...", ft.Icons.CALENDAR_VIEW_WEEK,
                'day_of_week', required=True, on_change=self._handle_field_change, on_blur=self._validate_field
            ),
            'phone': AddGroupComponents.create_text_field(
                "טלפון המורה", "מספר טלפון של המורה", ft.Icons.PHONE,
                'phone', keyboard_type=ft.KeyboardType.PHONE, on_change=self._handle_field_change
            ),
            'email': AddGroupComponents.create_text_field(
                "אימייל המורה", "כתובת אימייל של המורה", ft.Icons.EMAIL_OUTLINED,
                'email', keyboard_type=ft.KeyboardType.EMAIL, on_change=self._handle_field_change
            ),
        }

    def _handle_field_change(self, key, value):
        """Handle field changes"""
        self.form_state[key] = value
        if key in self.validation_errors:
            del self.validation_errors[key]
            self._update_field_style(key)

    def _validate_field(self, key, value):
        """Validate individual field"""
        error = AddGroupValidator.validate_field(key, value, self.required_fields)
        
        if key == 'name' and not error and value and value.strip():
            if self._check_group_name_exists(value.strip()):
                error = "קבוצה בשם זה כבר קיימת במערכת"
        
        if error:
            self.validation_errors[key] = error
        elif key in self.validation_errors:
            del self.validation_errors[key]
        
        self._update_field_style(key)
        return error is None

    def _check_group_name_exists(self, group_name):
        """Check if group name already exists"""
        try:
            groups_data = self.data_manager.load_groups()
            existing_groups = groups_data.get("groups", [])
            return any(group.get('name', '').strip().lower() == group_name.lower() 
                      for group in existing_groups)
        except Exception as e:
            print(f"Error checking group name existence: {e}")
            return False

    def _update_field_style(self, key):
        """Update field style based on validation state"""
        field = self.form_fields.get(key)
        if not field:
            return
        
        if key in self.validation_errors:
            field.border_color = "#ef4444"
            field.focused_border_color = "#dc2626"
            field.error_text = self.validation_errors[key]
        else:
            field.border_color = "#e1e7ef"
            field.focused_border_color = "#3b82f6"
            field.error_text = None
        
        try:
            field.update()
        except:
            pass

    def _validate_all_fields(self):
        """Validate all form fields"""
        self.validation_errors.clear()
        all_valid = True
        
        for key, value in self.form_state.items():
            field_value = value.strip() if value else ""
            if not self._validate_field(key, field_value):
                all_valid = False
        
        return all_valid

    def _render(self):
        """Main render method"""
        return ft.Column(
            controls=[
                self._render_header(),
                self._render_form_section(),
                self._render_footer()
            ],
            expand=True,
            spacing=0,
            scroll=ft.ScrollMode.AUTO
        )

    def _render_header(self):
        """Render header component"""
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.ADD_CIRCLE_OUTLINE, size=36, color="#3b82f6"),
                        bgcolor=ft.Colors.with_opacity(0.1, "#3b82f6"),
                        border_radius=12,
                        padding=ft.padding.all(12)
                    ),
                    ft.Container(width=16),
                    ft.Column([
                        ft.Text(
                            "הוספת קבוצה חדשה",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color="#0f172a"
                        ),
                        ft.Text(
                            "מלא את הפרטים הנדרשים ליצירת קבוצה חדשה במערכת. שדות עם * הם חובה",
                            size=16,
                            color="#64748b",
                            weight=ft.FontWeight.W_400
                        ),
                    ], spacing=4, expand=True),
                ], alignment=ft.MainAxisAlignment.START),
                ft.Container(height=24),
                ft.Divider(color="#e2e8f0", height=1, thickness=1),
            ], spacing=16),
            padding=ft.padding.all(32),
            bgcolor="#ffffff",
            border=ft.border.only(bottom=ft.BorderSide(1, "#f1f5f9"))
        )

    def _render_form_section(self):
        """Render form section component"""
        return ft.Container(
            content=ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Container(
                                content=ft.Icon(ft.Icons.EDIT_OUTLINED, color="#3b82f6", size=20),
                                bgcolor=ft.Colors.with_opacity(0.1, "#3b82f6"),
                                border_radius=8,
                                padding=ft.padding.all(8)
                            ),
                            ft.Container(width=12),
                            ft.Text("פרטי הקבוצה", size=20, weight=ft.FontWeight.BOLD, color="#0f172a"),
                        ]),
                        ft.Container(height=28),
                        self._render_form_grid(),
                    ], spacing=0),
                    padding=ft.padding.all(32)
                ),
                elevation=1,
                shadow_color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
                surface_tint_color="#ffffff",
                margin=ft.margin.all(0)
            ),
            padding=ft.padding.symmetric(horizontal=32, vertical=24),
            expand=True,
            bgcolor="#f8fafc"
        )

    def _render_form_grid(self):
        """Render form fields in a responsive grid"""
        return ft.Column([
            ft.ResponsiveRow([
                ft.Container(
                    content=self.form_fields['name'],
                    col={"xs": 12, "sm": 12, "md": 6},
                    padding=ft.padding.only(bottom=20, right=12)
                ),
                ft.Container(
                    content=self.form_fields['location'],
                    col={"xs": 12, "sm": 12, "md": 6},
                    padding=ft.padding.only(bottom=20, left=12)
                ),
            ]),
            ft.ResponsiveRow([
                ft.Container(
                    content=self.form_fields['price'],
                    col={"xs": 12, "sm": 12, "md": 6},
                    padding=ft.padding.only(bottom=20, right=12)
                ),
                ft.Container(
                    content=self.form_fields['age'],
                    col={"xs": 12, "sm": 12, "md": 6},
                    padding=ft.padding.only(bottom=20, left=12)
                ),
            ]),
            ft.ResponsiveRow([
                ft.Container(
                    content=self.form_fields['start_date'],
                    col={"xs": 12, "sm": 12, "md": 6},
                    padding=ft.padding.only(bottom=20, right=12)
                ),
                ft.Container(
                    content=self.form_fields['end_date'],
                    col={"xs": 12, "sm": 12, "md": 6},
                    padding=ft.padding.only(bottom=20, left=12)
                ),
            ]),
            ft.ResponsiveRow([
                ft.Container(
                    content=self.form_fields['day_of_week'],
                    col={"xs": 12, "sm": 12, "md": 12},
                    padding=ft.padding.only(bottom=20, right=12, left=12) 
                ),
            ]),
            ft.ResponsiveRow([
                ft.Container(
                    content=self.form_fields['teacher'],
                    col={"xs": 12, "sm": 12, "md": 12},
                    padding=ft.padding.only(bottom=20, right=12, left=12) 
                ),
            ]),
            ft.ResponsiveRow([
                ft.Container(
                    content=self.form_fields['phone'],
                    col={"xs": 12, "sm": 12, "md": 6},
                    padding=ft.padding.only(bottom=20, right=12)
                ),
                ft.Container(
                    content=self.form_fields['email'],
                    col={"xs": 12, "sm": 12, "md": 6},
                    padding=ft.padding.only(bottom=20, left=12)
                ),
            ]),
        ], spacing=0)

    def _render_footer(self):
        """Render footer with action buttons"""
        return ft.Container(
            content=ft.Column([
                ft.Divider(color="#e2e8f0", height=1),
                ft.Container(height=16),
                ft.Row([
                    AddGroupComponents.create_cancel_button(self._handle_cancel),
                    ft.Container(width=20),
                    AddGroupComponents.create_save_button(self._handle_save),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=0),
            ], spacing=0),
            padding=ft.padding.symmetric(horizontal=32, vertical=24),
            bgcolor="#fafbfc",
        )

    def _handle_save(self, e):
        """Handle save button click"""
        for key, field in self.form_fields.items():
            self.form_state[key] = field.value or ""
        
        group_name = self.form_state['name'].strip()
        if group_name and self._check_group_name_exists(group_name):
            self.validation_errors['name'] = "קבוצה בשם זה כבר קיימת במערכת"
            self._update_field_style('name')
            AddGroupComponents.show_error_dialog(self.page, "קבוצה בשם זה כבר קיימת במערכת")
            return
        
        if not self._validate_all_fields():
            AddGroupComponents.show_error_dialog(self.page, "ישנם ערכים חסרים או שגויים. בדוק את הטופס ותקן בהתאם")
            return
        
        price_value = self.form_state['price'].strip()
        try:
            price_int = int(price_value) if price_value and price_value.isdigit() else 0
        except (ValueError, TypeError):
            price_int = 0
        
        group_data = {
            "name": self.form_state['name'].strip(),
            "location": self.form_state['location'].strip(),
            "price": price_int,
            "age_group": self.form_state['age'].strip(),
            "teacher": self.form_state['teacher'].strip(),
            "group_start_date": self.form_state['start_date'].strip(),
            "group_end_date": self.form_state['end_date'].strip(),
            "day_of_week": self.form_state['day_of_week'].strip(),
            "teacher_phone": self.form_state['phone'].strip(),
            "teacher_email": self.form_state['email'].strip(),
        }
        
        is_valid, error_message = self.data_manager.validate_group_data(group_data)
        if not is_valid:
            AddGroupComponents.show_error_dialog(self.page, f"שגיאה בוולידציה: {error_message}")
            return
        
        success, message = self.data_manager.save_group(group_data)
        
        if success:
            AddGroupComponents.show_success_dialog(self.page, self._on_success)
        else:
            AddGroupComponents.show_error_dialog(self.page, f"שגיאה בשמירה: {message}")

    def _handle_cancel(self, e):
        """Handle cancel button click"""
        self._navigate_to_groups()

    def _on_success(self):
        """Called after successful save"""
        self._reset_form()
        self._navigate_to_groups()

    def _navigate_to_groups(self):
        """Navigate to groups page"""
        if self.groups_page:
            self.groups_page.refresh()
        self.navigation_callback(None, 1)

    def _reset_form(self):
        """Reset form to initial state"""
        for key in self.form_state:
            self.form_state[key] = ''
            if key in self.form_fields:
                self.form_fields[key].value = ""
                self.form_fields[key].error_text = None
                self.form_fields[key].border_color = "#e1e7ef"
                self.form_fields[key].focused_border_color = "#3b82f6"
                try:
                    self.form_fields[key].update()
                except:
                    pass
        self.validation_errors.clear()

    def get_view(self):
        return self.main_layout

    def save_group(self, e):
        self._handle_save(e)

    def go_back(self, e):
        self._handle_cancel(e)