import flet as ft
from components.modern_dialog import ModernDialog
from utils.validation import ValidationUtils
from utils.payment_utils import PaymentCalculator


class StudentEditView:
    """View for editing student information with modern React-like styling"""
    
    def __init__(self, parent, student):
        self.parent = parent
        self.page = parent.page
        self.student = student
        self.dialog = ModernDialog(self.page)
        
        self.name_field = None
        self.phone_field = None
        self.payment_field = None
        self.join_date_field = None
        self.has_sister_checkbox= None

    def render(self):
        """Render the edit form with modern styling"""
        self.parent.clear_layout()
        
        main_container = ft.Container(
            content=ft.Column([
                self._create_header(),
                self._create_form_card(),
                self._create_actions()
            ], spacing=24, scroll=ft.ScrollMode.AUTO),
            padding=ft.padding.all(24),
            bgcolor="#f8fafc",
            expand=True
        )
        
        self.parent.layout.controls.append(main_container)
        self.page.update()

    def _create_header(self):
        """Create modern header with simple border"""
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.Icons.ARROW_BACK_ROUNDED,
                        icon_color="#64748b",
                        icon_size=24,
                        on_click=lambda e: self.parent.show_students(),
                        tooltip="חזרה"
                    ),
                    bgcolor="#f1f5f9",
                    border_radius=12,
                    padding=ft.padding.all(8)
                ),
                ft.Column([
                    ft.Text(
                        "עריכת פרטי תלמידה",
                        size=28,
                        weight=ft.FontWeight.W_700,
                        color="#0f172a"
                    ),
                    ft.Text(
                        f"{self.student['name']} - {', '.join(self.student.get('groups', []))}",
                        size=16,
                        weight=ft.FontWeight.W_500,
                        color="#64748b"
                    )
                ], spacing=4, alignment=ft.CrossAxisAlignment.START)
            ], spacing=16, alignment=ft.MainAxisAlignment.START),
            padding=ft.padding.symmetric(vertical=20, horizontal=24),
            bgcolor="#ffffff",
            border_radius=16,
            border=ft.border.all(1, "#e2e8f0")
        )

    def _create_form_card(self):
        """Create modern form card with enhanced styling"""
        return ft.Container(
            content=ft.Column([
                ft.Text(
                    "פרטים אישיים",
                    size=20,
                    weight=ft.FontWeight.W_600,
                    color="#1e293b"
                ),
                ft.Container(height=16),  
                self._create_form_grid()
            ], spacing=0),
            bgcolor="#ffffff",
            border_radius=16,
            padding=ft.padding.all(32),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=25,
                color=ft.Colors.with_opacity(0.08, "#000000"),
                offset=ft.Offset(0, 4)
            ),
            border=ft.border.all(1, "#f1f5f9")
        )

    def _get_payment_display_status(self):
        """Get the display status for payment based on the logic from students_table.py"""
        payment_status = self.student.get('payment_status', '')
        student_groups = self.student.get('groups', [])
        join_date = self.student.get('join_date', '')
        student_id = self.student.get('id', '')
        
        payments = self.student.get('payments', [])
        amount_paid = 0
        for payment in payments:
            try:
                amount = payment.get('amount', 0)
                if isinstance(amount, str):
                    amount = float(amount) if amount.strip() else 0
                elif isinstance(amount, (int, float)):
                    amount = float(amount)
                else:
                    amount = 0
                amount_paid += amount
            except (ValueError, AttributeError):
                continue
        
        
        if payment_status == "שולם":
            return "שולם", ft.Colors.GREEN_600
        elif payment_status == "חוב":
            payment_calculator = PaymentCalculator()
            
            if payment_calculator:
                try:
                    if student_id:
                        total_owed_until_now = payment_calculator.get_student_payment_amount_until_now(student_id)
                    else:
                        total_owed_until_now = 0
                        for group_name in student_groups:
                            group_id = payment_calculator.get_group_id_by_name(group_name)
                            if group_id:
                                actual_join_date = payment_calculator.get_student_join_date_for_group(student_id, group_id)
                                if actual_join_date:
                                    group_payment = payment_calculator.get_payment_amount_until_now(group_id, actual_join_date)
                                    total_owed_until_now += group_payment
                    
                    if isinstance(total_owed_until_now, str):
                        total_owed_until_now = float(total_owed_until_now) if total_owed_until_now.strip() else 0
                    
                    if amount_paid >= total_owed_until_now:
                        return "שולם עד כה"
                    else:
                        return "חוב"
                        
                except Exception as e:
                    print(f"Error calculating payment status: {e}")
                    return "חוב"
            else:
                print("DEBUG: Payment calculator not found, returning 'חוב'")
                return "חוב"
        else:
            return payment_status, ft.Colors.GREY_600


    def _create_payment_status_display(self):
        """Create payment status display (read-only)"""
        display_status = self._get_payment_display_status()
        
        return ft.Container(
            content=ft.Column([
                ft.Text(
                    "סטטוס תשלום",
                    size=14,
                    weight=ft.FontWeight.W_500,
                    color="#64748b"
                ),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.PAYMENT_OUTLINED, size=20, color="#64748b"),
                        ft.Text(
                            display_status,
                            size=16,
                            weight=ft.FontWeight.W_400,
                        )
                    ], spacing=12),
                    padding=ft.padding.symmetric(horizontal=16, vertical=16),
                    bgcolor="#f8fafc",
                    border_radius=12,
                    border=ft.border.all(1, "#e1e7ef")
                )
            ], spacing=8)
        )

    def _create_form_grid(self):
        """Create form fields in a responsive grid layout"""
        self.name_field = self._create_modern_text_field(
            label="שם מלא",
            value=self.student['name'],
            icon=ft.Icons.PERSON_OUTLINE_ROUNDED,
            hint="הכנס שם מלא"
        )
        
        self.phone_field = self._create_modern_text_field(
            label="מספר טלפון",
            value=self.student['phone'],
            icon=ft.Icons.PHONE_OUTLINED,
            hint="050-1234567",
            keyboard_type=ft.KeyboardType.PHONE
        )
        
        self.join_date_field = self._create_modern_text_field(
            label="תאריך הצטרפות",
            value=self.student['join_date'],
            icon=ft.Icons.CALENDAR_TODAY_OUTLINED,
            hint="dd/mm/yyyy או dd-mm-yyyy או dd.mm.yyyy",
            suffix="📅"
        )
        
        group_display = ft.Container(
            content=ft.Column([
                ft.Text(
                    "קבוצה",
                    size=14,
                    weight=ft.FontWeight.W_500,
                    color="#64748b"
                ),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.GROUP_OUTLINED, size=20, color="#64748b"),
                        ft.Text(
                            ', '.join(self.student.get('groups', [])),
                            size=16,
                            weight=ft.FontWeight.W_400,
                            color="#0f172a"
                        )
                    ], spacing=12),
                    padding=ft.padding.symmetric(horizontal=16, vertical=16),
                    bgcolor="#f8fafc",
                    border_radius=12,
                    border=ft.border.all(1, "#e1e7ef")
                )
            ], spacing=8)
        )
        
        payment_status_display = self._create_payment_status_display()
        
        self.has_sister_checkbox = ft.Checkbox(
            label="יש אחות נוספת בחוג",
            value=self.student.get('has_sister', False),
            fill_color=ft.Colors.GREEN_600
        )
        
        return ft.Column([
            ft.Row([
                ft.Container(
                    content=self.name_field,
                    expand=True
                )
            ]),
            ft.Row([
                ft.Container(
                    content=self.phone_field,
                    expand=1
                ),
                ft.Container(width=16), 
                ft.Container(
                    content=self.join_date_field,
                    expand=1
                )
            ]),
            ft.Row([
                ft.Container(
                    content=payment_status_display,
                    expand=1
                ),
                ft.Container(width=16), 
                ft.Container(
                    content=group_display,
                    expand=1
                )
            ]),
            ft.Row([
                ft.Container(
                    content=self.has_sister_checkbox,
                    expand=True
                )
            ])
        ], spacing=20)


    def _create_modern_text_field(self, label, value, icon, hint, keyboard_type=None, suffix=None):
        """Create a modern text field component (React-like styling)"""
        return ft.TextField(
            label=label,
            value=value,
            hint_text=hint,
            prefix_icon=icon,
            suffix_text=suffix,
            keyboard_type=keyboard_type,
            border_radius=12,
            bgcolor="#fafbfc",
            border_color="#e1e7ef",
            focused_border_color="#3b82f6",
            focused_bgcolor="#ffffff",
            label_style=ft.TextStyle(
                color="#64748b", 
                size=14,
                weight=ft.FontWeight.W_500
            ),
            text_style=ft.TextStyle(
                color="#0f172a", 
                size=16,
                weight=ft.FontWeight.W_400
            ),
            hint_style=ft.TextStyle(
                color="#94a3b8",
                size=14
            ),
            content_padding=ft.padding.symmetric(horizontal=16, vertical=16),
            cursor_color="#3b82f6",
            selection_color=ft.Colors.with_opacity(0.2, "#3b82f6"),
            on_focus=self._on_field_focus,
            on_blur=self._on_field_blur
        )

    def _on_field_focus(self, e):
        """Handle field focus with animation"""
        e.control.bgcolor = "#ffffff"
        e.control.update()

    def _on_field_blur(self, e):
        """Handle field blur with animation"""
        e.control.bgcolor = "#fafbfc"
        e.control.update()

    def _create_actions(self):
        """Create clean action buttons without shadows"""
        return ft.Container(
            content=ft.Row([
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CHECK_ROUNDED, size=20, color="#ffffff"),
                        ft.Text(
                            "שמור שינויים",
                            size=16,
                            weight=ft.FontWeight.W_600,
                            color="#ffffff"
                        )
                    ], spacing=8, alignment=ft.MainAxisAlignment.CENTER),
                    on_click=self._save_student,
                    bgcolor="#10b981",
                    color="#ffffff",
                    elevation=0,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=12),
                        padding=ft.padding.symmetric(horizontal=32, vertical=16),
                        elevation={"": 0, "hovered": 0, "pressed": 0}
                    )
                ),
                
                ft.Container(width=16), 
                
                ft.OutlinedButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CLOSE_ROUNDED, size=20, color="#64748b"),
                        ft.Text(
                            "ביטול",
                            size=16,
                            weight=ft.FontWeight.W_600,
                            color="#64748b"
                        )
                    ], spacing=8, alignment=ft.MainAxisAlignment.CENTER),
                    on_click=lambda e: self.parent.show_students(),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=12),
                        padding=ft.padding.symmetric(horizontal=32, vertical=16),
                        side=ft.BorderSide(2, "#e2e8f0"),
                        bgcolor={"": "#ffffff", "hovered": "#f8fafc"},
                        elevation={"": 0, "hovered": 0, "pressed": 0}
                    )
                )
            ], spacing=0, alignment=ft.MainAxisAlignment.CENTER),
            padding=ft.padding.symmetric(vertical=32)
        )

    def _validate_and_format_date(self, date_str):
        """Validate and format date - accepts multiple formats"""
        if not date_str or not date_str.strip():
            return False, "תאריך הוא שדה חובה"
        
        date_str = date_str.strip()
        
        date_formats = [
            "%d/%m/%Y",    # 25/12/2023
            "%d-%m-%Y",    # 25-12-2023
            "%d.%m.%Y",    # 25.12.2023
            "%d/%m/%y",    # 25/12/23
            "%d-%m-%y",    # 25-12-23
            "%d.%m.%y",    # 25.12.23
            
            "%Y/%m/%d",    # 2023/12/25
            "%Y-%m-%d",    # 2023-12-25
            "%Y.%m.%d",    # 2023.12.25
            "%y/%m/%d",    # 23/12/25
            "%y-%m-%d",    # 23-12-25
            "%y.%m.%d",    # 23.12.25
            
            "%m/%d/%Y",    # 12/25/2023
            "%m-%d-%Y",    # 12-25-2023
            "%m.%d.%Y",    # 12.25.2023
            "%m/%d/%y",    # 12/25/23
            "%m-%d-%y",    # 12-25-23
            "%m.%d.%y",    # 12.25.23
        ]
        
        from datetime import datetime
        
        for date_format in date_formats:
            try:
                parsed_date = datetime.strptime(date_str, date_format)
                
                if parsed_date.year < 100:
                    if parsed_date.year < 50: 
                        parsed_date = parsed_date.replace(year=parsed_date.year + 2000)
                    else:  
                        parsed_date = parsed_date.replace(year=parsed_date.year + 1900)
                
                formatted_date = parsed_date.strftime("%d/%m/%Y")
                return True, formatted_date
                
            except ValueError:
                continue
        
        return False, "פורמט תאריך לא תקין. דוגמאות תקינות: 25/12/2023, 2023/12/25, 25-12-2023"


    def _save_student(self, e):
        """Save student changes with validation and loading state"""
        self._set_loading_state(True)
        
        form_data = {
            "name": self.name_field.value.strip() if self.name_field.value else "",
            "phone": self.phone_field.value.strip() if self.phone_field.value else "",
            "join_date": self.join_date_field.value.strip() if self.join_date_field.value else ""
        }
        
        is_valid, empty_fields = ValidationUtils.validate_required_fields(form_data)
        if not is_valid:
            self._set_loading_state(False)
            self._show_validation_error("יש למלא את כל השדות הנדרשים", empty_fields)
            return
        
        name_valid, name_error = ValidationUtils.validate_name(form_data["name"])
        if not name_valid:
            self._set_loading_state(False)
            self._show_field_error(self.name_field, name_error)
            return
        
        phone_valid, phone_error = ValidationUtils.validate_phone(form_data["phone"])
        if not phone_valid:
            self._set_loading_state(False)
            self._show_field_error(self.phone_field, phone_error)
            return
        
        date_valid, date_result = self._validate_and_format_date(form_data["join_date"])
        if not date_valid:
            self._set_loading_state(False)
            self._show_field_error(self.join_date_field, date_result)
            return
        
        new_data = {
            "id": self.student.get('id', ''),
            "name": form_data["name"],
            "phone": form_data["phone"],
            "groups": self.student.get('groups', []),
            "payment_status": self.student.get('payment_status', ''),  
            "join_date": date_result,  
            "payments": self.student.get('payments', []),
            "has_sister": self.has_sister_checkbox.value
        }
        
        success = self.parent.data_manager.update_student(
            self.student['id'], 
            new_data
        )
        
        self._set_loading_state(False)
        
        if success:
            self._show_success_message()
        else:
            self.dialog.show_error("שגיאה בשמירת התלמידה")

    def _set_loading_state(self, loading):
        """Set loading state for save button"""
        pass

    def _show_validation_error(self, message, fields):
        """Show validation error with field highlighting"""
        for field_name in fields:
            field = getattr(self, f"{field_name}_field", None)
            if field:
                field.border_color = "#ef4444"
                field.update()
        
        self.dialog.show_error(message)

    def _show_field_error(self, field, message):
        """Show error for specific field"""
        field.border_color = "#ef4444"
        field.error_text = message
        field.update()
        self.dialog.show_error(message)

    def _clear_field_errors(self):
        """Clear all field errors"""
        fields = [self.name_field, self.phone_field, self.join_date_field]
        
        for field in fields:
            if field:
                field.border_color = "#e1e7ef"
                field.error_text = ""
                field.update()

    def _show_success_message(self):
        """Show success message with animation"""
        self.dialog.show_success(
            "✅ התלמידה נשמרה בהצלחה!",
            callback=self.parent.show_students
        )
