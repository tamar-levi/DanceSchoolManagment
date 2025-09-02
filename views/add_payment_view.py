import flet as ft
from components.modern_dialog import ModernDialog
from datetime import datetime


class AddPaymentView:
    """View for adding new payment with modern React-like styling"""
    
    def __init__(self, parent, student):
        self.parent = parent
        self.page = parent.page
        self.student = student
        self.dialog = ModernDialog(self.page)
        
        self.form_state = {
            'amount': '',
            'date': '',
            'payment_method': '',
            'check_number': ''
        }
        
        self.amount_input = None
        self.date_input = None
        self.payment_method_dropdown = None
        self.check_number_input = None

    def render(self):
        """Render add payment form with modern styling"""
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
        """Create modern header with elegant styling"""
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.Icons.ARROW_BACK_ROUNDED,
                        icon_color="#64748b",
                        icon_size=24,
                        on_click=lambda e: self.parent.show_payments(self.student),
                        tooltip="חזרה"
                    ),
                    bgcolor="#ffffff",
                    border_radius=12,
                    padding=ft.padding.all(8),
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=8,
                        color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                        offset=ft.Offset(0, 2),
                    )
                ),
                ft.Column([
                    ft.Text(
                        "תשלום חדש",
                        size=28,
                        weight=ft.FontWeight.W_700,
                        color="#0f172a"
                    ),
                    ft.Text(
                        f"{self.student['name']}",
                        size=16,
                        weight=ft.FontWeight.W_500,
                        color="#64748b"
                    )
                ], spacing=4, alignment=ft.CrossAxisAlignment.START)
            ], spacing=16, alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.symmetric(vertical=8)
        )

    def _create_form_card(self):
        """Create modern form card with React-like styling"""
        form_fields = self._create_form_fields()
        
        return ft.Container(
            content=ft.Column([
                ft.Text(
                    "פרטי התשלום",
                    size=20,
                    weight=ft.FontWeight.W_600,
                    color="#1e293b"
                ),
                ft.Container(height=8),
                *form_fields.values()
            ], spacing=20),
            bgcolor="#ffffff",
            border_radius=16,
            padding=ft.padding.all(32),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                offset=ft.Offset(0, 4),
            ),
            border=ft.border.all(1, "#f1f5f9")
        )

    def _create_form_fields(self):
        """Create styled form fields with modern React-like approach"""
        return {
            'amount': self._create_text_field(
                label="סכום התשלום",
                hint="הכנס סכום בשקלים",
                icon=ft.Icons.PAYMENTS_OUTLINED,
                suffix="₪",
                keyboard_type=ft.KeyboardType.NUMBER,
                key='amount'
            ),
            'date': self._create_text_field(
                label="תאריך התשלום",
                hint="dd/mm/yyyy",
                icon=ft.Icons.CALENDAR_TODAY_OUTLINED,
                key='date',
                value=datetime.now().strftime("%d/%m/%Y") 
            ),
            'payment_method': self._create_payment_method_dropdown(),
            'check_number': self._create_check_number_field()
        }

    def _create_text_field(self, label, hint, icon, key, suffix=None, keyboard_type=None, value=""):
        """Create modern text field component"""
        field = ft.TextField(
            label=label,
            hint_text=hint,
            value=value,
            keyboard_type=keyboard_type,
            prefix_icon=icon,
            suffix_text=suffix,
            border_radius=12,
            bgcolor="#f8fafc",
            border_color="#e2e8f0",
            focused_border_color="#3b82f6",
            content_padding=ft.padding.symmetric(horizontal=16, vertical=16),
            text_style=ft.TextStyle(size=15, color="#1e293b"),
            label_style=ft.TextStyle(size=14, color="#64748b"),
            hint_style=ft.TextStyle(size=14, color="#94a3b8"),
            on_change=lambda e: self._handle_field_change(key, e.control.value)
        )
        
        if key == 'amount':
            self.amount_input = field
        elif key == 'date':
            self.date_input = field
            
        return field

    def _create_payment_method_dropdown(self):
        """Create modern payment method dropdown with check number support"""
        self.payment_method_dropdown = ft.Dropdown(
            label="אופן תשלום",
            hint_text="בחר אופן תשלום",
            border_radius=12,
            bgcolor="#f8fafc",
            border_color="#e2e8f0",
            focused_border_color="#3b82f6",
            content_padding=ft.padding.symmetric(horizontal=16, vertical=16),
            text_style=ft.TextStyle(size=15, color="#1e293b"),
            label_style=ft.TextStyle(size=14, color="#64748b"),
            options=[
                ft.dropdown.Option("מזומן", "מזומן"),
                ft.dropdown.Option("אשראי", "אשראי"),
                ft.dropdown.Option("העברה בנקאית", "העברה בנקאית"),
                ft.dropdown.Option("ביט", "ביט"),
                ft.dropdown.Option("צ'ק", "צ'ק"),
                ft.dropdown.Option("פייבוקס", "פייבוקס")
            ],
            on_change=self._handle_payment_method_change
        )
        
        return self.payment_method_dropdown

    def _create_check_number_field(self):
        """Create check number field (initially hidden)"""
        self.check_number_input = ft.TextField(
            label="מספר צ'ק",
            hint_text="הכנס מספר צ'ק",
            prefix_icon=ft.Icons.RECEIPT_OUTLINED,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_radius=12,
            bgcolor="#f8fafc",
            border_color="#e2e8f0",
            focused_border_color="#3b82f6",
            content_padding=ft.padding.symmetric(horizontal=16, vertical=16),
            text_style=ft.TextStyle(size=15, color="#1e293b"),
            label_style=ft.TextStyle(size=14, color="#64748b"),
            hint_style=ft.TextStyle(size=14, color="#94a3b8"),
            visible=False,
            on_change=lambda e: self._handle_field_change('check_number', e.control.value)
        )
        
        return self.check_number_input

    def _handle_field_change(self, key, value):
        """Handle field changes (React-like state management)"""
        self.form_state[key] = value

    def _handle_payment_method_change(self, e):
        """Handle payment method change and show/hide check number field"""
        payment_method = e.control.value
        self.form_state['payment_method'] = payment_method
        
        if payment_method == "צ'ק":
            self.check_number_input.visible = True
        else:
            self.check_number_input.visible = False
            self.check_number_input.value = ""
            self.form_state['check_number'] = ""
        
        self.page.update()

    def _create_actions(self):
        """Create modern action buttons"""
        return ft.Container(
            content=ft.Row([
                self._render_save_button(),
                self._render_cancel_button()
            ], spacing=16, alignment=ft.MainAxisAlignment.CENTER),
            padding=ft.padding.symmetric(vertical=16)
        )

    def _render_save_button(self):
        """Render elegant save button component"""
        return ft.Container(
            content=ft.ElevatedButton(
                content=ft.Row([
                    ft.Icon(ft.Icons.CHECK_ROUNDED, size=18, color="#ffffff"),
                    ft.Text("שמור תשלום", color="#ffffff", size=15, weight=ft.FontWeight.W_600)
                ], spacing=10, tight=True),
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=14),
                    padding=ft.padding.symmetric(horizontal=32, vertical=16),
                    bgcolor={
                        ft.ControlState.DEFAULT: "#10b981",
                        ft.ControlState.HOVERED: "#059669",
                        ft.ControlState.PRESSED: "#047857",
                    },
                    overlay_color="transparent",
                    elevation=0
                ),
                on_click=self._save_payment
            ),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=12,
                color=ft.Colors.with_opacity(0.25, "#10b981"),
                offset=ft.Offset(0, 4),
            ),
        )

    def _render_cancel_button(self):
        """Render elegant cancel button component"""
        return ft.Container(
            content=ft.TextButton(
                content=ft.Row([
                    ft.Icon(ft.Icons.CLOSE_ROUNDED, size=18, color="#64748b"),
                    ft.Text("ביטול", color="#64748b", size=15, weight=ft.FontWeight.W_600)
                ], spacing=10, tight=True),
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=14),
                    padding=ft.padding.symmetric(horizontal=32, vertical=16),
                    bgcolor={
                        ft.ControlState.DEFAULT: "#ffffff",
                        ft.ControlState.HOVERED: "#f8fafc",
                        ft.ControlState.PRESSED: "#f1f5f9",
                    },
                    overlay_color="transparent",
                    side={
                        ft.ControlState.DEFAULT: ft.BorderSide(1, "#e2e8f0"),
                        ft.ControlState.HOVERED: ft.BorderSide(1, "#cbd5e1"),
                    }
                ),
                on_click=lambda e: self.parent.show_payments(self.student)
            ),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.04, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
        )

    def _validate_form(self):
        """Validate form data"""
        errors = []
        
        if not self.form_state['amount'].strip():
            errors.append("יש להזין סכום")
        else:
            try:
                amount = float(self.form_state['amount'])
                if amount <= 0:
                    errors.append("הסכום חייב להיות חיובי")
            except ValueError:
                errors.append("יש להזין סכום תקין (מספר בלבד)")
        
        if not self.form_state['date'].strip():
            errors.append("יש להזין תאריך")
        
        if not self.form_state['payment_method']:
            errors.append("יש לבחור אופן תשלום")
        
        if self.form_state['payment_method'] == "צ'ק" and not self.form_state['check_number'].strip():
            errors.append("יש להזין מספר צ'ק")
        
        return errors

    def _save_payment(self, e):
        """Save new payment with validation"""
        self.form_state['amount'] = self.amount_input.value.strip() if self.amount_input.value else ""
        self.form_state['date'] = self.date_input.value.strip() if self.date_input.value else ""
        self.form_state['payment_method'] = self.payment_method_dropdown.value if self.payment_method_dropdown.value else ""
        if self.check_number_input.visible:
            self.form_state['check_number'] = self.check_number_input.value.strip() if self.check_number_input.value else ""
        
        errors = self._validate_form()
        if errors:
            self.dialog.show_error("\n".join(errors))
            return

        payment_data = {
            "amount": self.form_state['amount'],
            "date": self.form_state['date'],
            "payment_method": self.form_state['payment_method']
        }
        
        if self.form_state['payment_method'] == "צ'ק" and self.form_state['check_number']:
            payment_data["check_number"] = self.form_state['check_number']

        success = self.parent.data_manager.add_payment(self.student['id'],  payment_data)
        
        if success:
            self.dialog.show_success(
                "התשלום נשמר בהצלחה!",
                callback=lambda: self.parent.show_payments(self.student)
            )
        else:
            self.dialog.show_error("שגיאה בשמירת התשלום")



    def _create_date_picker_button(self):
        """Create date picker button for better UX"""
        return ft.Container(
            content=ft.IconButton(
                icon=ft.Icons.CALENDAR_TODAY_OUTLINED,
                icon_color="#64748b",
                icon_size=20,
                tooltip="בחר תאריך",
                on_click=self._show_date_picker
            ),
            bgcolor="#f8fafc",
            border_radius=8,
            padding=ft.padding.all(4)
        )

    def _show_date_picker(self, e):
        """Show date picker dialog"""
        def on_date_change(e):
            if e.control.value:
                selected_date = e.control.value
                formatted_date = selected_date.strftime("%d/%m/%Y")
                self.date_input.value = formatted_date
                self.form_state['date'] = formatted_date
                self.page.update()

        date_picker = ft.DatePicker(
            first_date=datetime(2020, 1, 1),
            last_date=datetime(2030, 12, 31),
            on_change=on_date_change
        )
        
        self.page.overlay.append(date_picker)
        date_picker.pick_date()
        self.page.update()

    def _create_payment_summary(self):
        """Create payment summary card for better UX"""
        if not all([self.form_state['amount'], self.form_state['payment_method']]):
            return ft.Container()
        
        try:
            amount = float(self.form_state['amount'])
            summary_items = [
                ft.Row([
                    ft.Text("סכום:", size=14, color="#64748b", weight=ft.FontWeight.W_500),
                    ft.Text(f"{amount:,.0f} ₪", size=16, color="#0f172a", weight=ft.FontWeight.W_600)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("אופן תשלום:", size=14, color="#64748b", weight=ft.FontWeight.W_500),
                    ft.Text(self.form_state['payment_method'], size=14, color="#0f172a", weight=ft.FontWeight.W_500)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ]
            
            if self.form_state['payment_method'] == "צ'ק" and self.form_state['check_number']:
                summary_items.append(
                    ft.Row([
                        ft.Text("מספר צ'ק:", size=14, color="#64748b", weight=ft.FontWeight.W_500),
                        ft.Text(self.form_state['check_number'], size=14, color="#0f172a", weight=ft.FontWeight.W_500)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                )
            
            return ft.Container(
                content=ft.Column([
                    ft.Text(
                        "סיכום התשלום",
                        size=16,
                        weight=ft.FontWeight.W_600,
                        color="#1e293b"
                    ),
                    ft.Divider(color="#e2e8f0", height=1),
                    *summary_items
                ], spacing=12),
                bgcolor="#f8fafc",
                border_radius=12,
                padding=ft.padding.all(16),
                border=ft.border.all(1, "#e2e8f0"),
                margin=ft.margin.only(top=16)
            )
        except ValueError:
            return ft.Container()

