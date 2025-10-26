import json
import flet as ft
from typing import Dict, Any
from utils.manage_json import ManageJSON

class PaymentPage:
    def __init__(self, page: ft.Page, navigation_handler=None):
        self.page = page
        self.navigation_handler = navigation_handler
        self.payments_data = []
        self.edit_dialog = None
        self.delete_dialog = None
        self.note_dialog = None
        self.table_container = None
        self.stats_section = None
        
        self.load_payments()
        
    def load_payments(self):
        """Load payments data from students.json"""
        try:
            data_dir = ManageJSON.get_appdata_path() / "data"
            students_file = data_dir / "students.json"
            
            self.payments_data = []
            
            if students_file.exists():
                with open(students_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                    for student_idx, student in enumerate(data.get("students", [])):
                        student_name = student.get("name", "")
                        student_groups = student.get("groups", [])
                        
                        for payment_idx, payment in enumerate(student.get("payments", [])):
                            payment_data = {
                                "student_name": student_name,
                                "student_idx": student_idx,
                                "payment_idx": payment_idx,
                                "amount": payment.get("amount", "0"),
                                "date": payment.get("date", ""),
                                "payment_method": payment.get("payment_method", ""),
                                "groups": student_groups,
                                "groups_display": ", ".join(student_groups),
                                "note": payment.get("note", "")
                            }
                            
                            if payment.get("check_number"):
                                payment_data["check_number"] = payment.get("check_number")
                            
                            self.payments_data.append(payment_data)
        except Exception as e:
            print(f"Error loading payments: {e}")

    def save_payment_changes(self, student_idx, payment_idx, new_amount, new_method, new_check_number=None, new_note=None):
        """Save changes to a payment (without date)"""
        try:
            data_dir = ManageJSON.get_appdata_path() / "data"
            students_file = data_dir / "students.json"
            
            with open(students_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            payment = data["students"][student_idx]["payments"][payment_idx]
            payment["amount"] = new_amount
            payment["payment_method"] = new_method
            
            if new_method == "צ'ק" and new_check_number:
                payment["check_number"] = new_check_number
            elif "check_number" in payment and new_method != "צ'ק":
                del payment["check_number"]
            
            if new_note:
                payment["note"] = new_note
            elif "note" in payment and not new_note:
                del payment["note"]
            
            with open(students_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving payment: {e}")
            return False

    def delete_payment(self, student_idx, payment_idx):
        """Delete a payment"""
        try:
            data_dir = ManageJSON.get_appdata_path() / "data"
            students_file = data_dir / "students.json"
            
            with open(students_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            del data["students"][student_idx]["payments"][payment_idx]
            
            with open(students_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Error deleting payment: {e}")
            return False

    def show_note_dialog(self, payment: Dict[str, Any]):
        """Show dialog to view payment note"""
        note_text = payment.get("note", "אין הערה")
        
        def close_dialog(e):
            self.page.close(self.note_dialog)
        
        self.note_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("הערה לתשלום", rtl=True, text_align=ft.TextAlign.RIGHT, size=18, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Column([
                            ft.Text(f"תלמידה: {payment['student_name']}", rtl=True, weight=ft.FontWeight.BOLD, size=14),
                            ft.Text(f"סכום: {payment['amount']}₪", rtl=True, size=13, color=ft.Colors.GREY_700),
                            ft.Text(f"תאריך: {payment['date']}", rtl=True, size=13, color=ft.Colors.GREY_700),
                        ], spacing=4),
                        padding=ft.padding.all(12),
                        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE_600),
                        border_radius=8
                    ),
                    ft.Divider(),
                    ft.Container(
                        content=ft.Text(
                            note_text,
                            rtl=True,
                            size=14,
                            color=ft.Colors.GREY_800,
                            text_align=ft.TextAlign.RIGHT
                        ),
                        padding=ft.padding.all(12),
                        bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.GREY_400),
                        border_radius=8,
                        border=ft.border.all(1, ft.Colors.with_opacity(0.2, ft.Colors.GREY_400))
                    ),
                ], spacing=15, tight=True),
                width=320,
                padding=ft.padding.all(10)
            ),
            actions=[
                ft.ElevatedButton("סגור", on_click=close_dialog, bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )
        
        self.page.open(self.note_dialog)

    def show_edit_dialog(self, payment: Dict[str, Any]):
        """Show dialog to edit payment"""
        amount_field = ft.TextField(
            label="סכום",
            value=payment["amount"],
            keyboard_type=ft.KeyboardType.NUMBER,
            text_align=ft.TextAlign.RIGHT,
            rtl=True,
            width=250
        )
        
        payment_method_dropdown = ft.Dropdown(
            label="אמצעי תשלום",
            value=payment["payment_method"],
            options=[
                ft.dropdown.Option("מזומן"),
                ft.dropdown.Option("העברה בנקאית"),
                ft.dropdown.Option("צ'ק"),
                ft.dropdown.Option("אשראי"),
            ],
            alignment=ft.alignment.center_right,
            width=250
        )
        
        check_number_field = ft.TextField(
            label="מספר צ'ק",
            value=payment.get("check_number", ""),
            visible=payment["payment_method"] == "צ'ק",
            text_align=ft.TextAlign.RIGHT,
            rtl=True,
            width=250
        )
        
        note_field = ft.TextField(
            label="הערה",
            value=payment.get("note", ""),
            text_align=ft.TextAlign.RIGHT,
            rtl=True,
            width=250,
            multiline=True,
            min_lines=2,
            max_lines=4
        )
        
        def on_payment_method_change(e):
            check_number_field.visible = payment_method_dropdown.value == "צ'ק"
            self.edit_dialog.update()
        
        payment_method_dropdown.on_change = on_payment_method_change
        
        def save_changes(e):
            if not amount_field.value:
                return
            
            check_num = check_number_field.value if payment_method_dropdown.value == "צ'ק" else None
            note_value = note_field.value.strip() if note_field.value else None
            
            success = self.save_payment_changes(
                payment["student_idx"],
                payment["payment_idx"],
                amount_field.value,
                payment_method_dropdown.value,
                check_num,
                note_value
            )
            
            if success:
                self.page.close(self.edit_dialog)
                
                self.load_payments()
                
                if self.table_container and self.table_container.content:
                    self.table_container.content.controls = [self.create_payments_table()]
                
                if self.stats_section:
                    self.stats_section.content = self.create_stats_section()
                
                self.page.update()
        
        def cancel_edit(e):
            self.page.close(self.edit_dialog)
        
        self.edit_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("עריכת תשלום", rtl=True, text_align=ft.TextAlign.RIGHT, size=18, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Column([
                            ft.Text(f"תלמידה: {payment['student_name']}", rtl=True, weight=ft.FontWeight.BOLD, size=14),
                            ft.Text(f"תאריך: {payment['date']}", rtl=True, size=13, color=ft.Colors.GREY_700),
                        ], spacing=4),
                        padding=ft.padding.all(12),
                        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE_600),
                        border_radius=8
                    ),
                    ft.Divider(),
                    amount_field,
                    payment_method_dropdown,
                    check_number_field,
                    note_field,
                ], spacing=15, tight=True, scroll=ft.ScrollMode.AUTO),
                width=320,
                height=450,
                padding=ft.padding.all(10)
            ),
            actions=[
                ft.TextButton("ביטול", on_click=cancel_edit),
                ft.ElevatedButton("שמור", on_click=save_changes, bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.open(self.edit_dialog)

    def show_delete_dialog(self, payment: Dict[str, Any]):
        """Show confirmation dialog to delete payment"""
        def confirm_delete(e):
            success = self.delete_payment(payment["student_idx"], payment["payment_idx"])
            
            if success:
                self.page.close(self.delete_dialog)
                
                self.load_payments()
                
                if self.table_container and self.table_container.content:
                    self.table_container.content.controls = [self.create_payments_table()]
                
                if self.stats_section:
                    self.stats_section.content = self.create_stats_section()
                
                self.page.update()
        
        def cancel_delete(e):
            self.page.close(self.delete_dialog)
        
        self.delete_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("אישור מחיקה", rtl=True, text_align=ft.TextAlign.RIGHT),
            content=ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.WARNING_AMBER, size=48, color=ft.Colors.ORANGE_600),
                    ft.Text(
                        f"האם אתה בטוח שברצונך למחוק את התשלום?",
                        rtl=True,
                        text_align=ft.TextAlign.CENTER,
                        size=16
                    ),
                    ft.Divider(),
                    ft.Text(f"תלמידה: {payment['student_name']}", rtl=True, weight=ft.FontWeight.BOLD),
                    ft.Text(f"סכום: {payment['amount']}₪", rtl=True),
                    ft.Text(f"תאריך: {payment['date']}", rtl=True),
                    ft.Text(f"אמצעי תשלום: {payment['payment_method']}", rtl=True),
                ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER, tight=True),
                width=300,
                padding=ft.padding.all(10)
            ),
            actions=[
                ft.TextButton("ביטול", on_click=cancel_delete),
                ft.ElevatedButton(
                    "מחק", 
                    on_click=confirm_delete, 
                    bgcolor=ft.Colors.RED_600, 
                    color=ft.Colors.WHITE
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            actions_padding=ft.padding.only(left=10, right=10, bottom=10, top=5),
            content_padding=ft.padding.all(20),
        )
        
        self.page.open(self.delete_dialog)

    def refresh_view(self):
        """Refresh the entire view - DEPRECATED, use direct update instead"""
        pass

    def create_stats_card(self, title, value, icon, color, subtitle=""):
        """Create a modern statistics card"""
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(icon, size=28, color=color),
                    ft.Column([
                        ft.Text(value, size=24, weight=ft.FontWeight.BOLD, color=color),
                        ft.Text(subtitle, size=10, color=ft.Colors.GREY_500) if subtitle else ft.Container(),
                    ], spacing=2)
                ], alignment=ft.MainAxisAlignment.START, spacing=12),
                ft.Text(title, size=13, color=ft.Colors.GREY_600, text_align=ft.TextAlign.LEFT, rtl=True)
            ], spacing=8),
            width=180,
            height=90,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=ft.padding.all(16),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 2)
            ),
            border=ft.border.all(1, ft.Colors.with_opacity(0.1, ft.Colors.GREY_400))
        )

    def calculate_payment_stats(self):
        """Calculate comprehensive payment statistics"""
        if not self.payments_data:
            return {
                "total_amount": "0",
                "total_payments": "0",
                "cash_payments": "0",
                "transfer_payments": "0"
            }
            
        total_amount = 0
        cash_count = 0
        transfer_count = 0
        
        for payment in self.payments_data:
            try:
                total_amount += float(payment["amount"])
            except ValueError:
                pass
                
            if payment["payment_method"] == "מזומן":
                cash_count += 1
            else:
                transfer_count += 1
        
        return {
            "total_amount": f"{total_amount:,.0f}₪",
            "total_payments": str(len(self.payments_data)),
            "cash_payments": str(cash_count),
            "transfer_payments": str(transfer_count)
        }

    def create_stats_section(self):
        """Create the statistics cards section"""
        stats = self.calculate_payment_stats()
        
        return ft.Container(
            content=ft.Row([
                self.create_stats_card(
                    "סה״כ הכנסות", 
                    stats["total_amount"], 
                    ft.Icons.ATTACH_MONEY, 
                    ft.Colors.GREEN_600
                ),
                self.create_stats_card(
                    "סה״כ תשלומים", 
                    stats["total_payments"], 
                    ft.Icons.RECEIPT_LONG, 
                    ft.Colors.BLUE_600,
                ),
                self.create_stats_card(
                    "תשלומי מזומן", 
                    stats["cash_payments"], 
                    ft.Icons.MONEY, 
                    ft.Colors.ORANGE_600,
                ),
                self.create_stats_card(
                    "תשלומים אחרים", 
                    stats["transfer_payments"], 
                    ft.Icons.ACCOUNT_BALANCE, 
                    ft.Colors.PURPLE_600,
                ),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20, wrap=True),
            alignment=ft.alignment.center
        )

    def create_table_header(self):
        """Create modern table header row"""
        header_style = {
            "bgcolor": ft.Colors.with_opacity(0.8, ft.Colors.BLUE_GREY_900),
            "padding": ft.padding.symmetric(horizontal=16, vertical=20),
            "alignment": ft.alignment.center,
        }
        
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.PERSON, size=16, color=ft.Colors.WHITE70),
                        ft.Text("שם התלמידה", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE)
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=4),
                    expand=3, **header_style
                ),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.ATTACH_MONEY, size=16, color=ft.Colors.WHITE70),
                        ft.Text("סכום", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE)
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=4),
                    expand=2, **header_style
                ),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.DATE_RANGE, size=16, color=ft.Colors.WHITE70),
                        ft.Text("תאריך", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE)
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=4),
                    expand=2, **header_style
                ),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.PAYMENT, size=16, color=ft.Colors.WHITE70),
                        ft.Text("אמצעי תשלום", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE)
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=4),
                    expand=2, **header_style
                ),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.GROUP, size=16, color=ft.Colors.WHITE70),
                        ft.Text("קבוצה", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE)
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=4),
                    expand=2, **header_style
                ),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.SETTINGS, size=16, color=ft.Colors.WHITE70),
                        ft.Text("פעולות", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE)
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=4),
                    expand=2, **header_style
                ),
            ], spacing=0),
            border_radius=ft.border_radius.only(top_left=12, top_right=12),
        )

    def create_table_row(self, payment: Dict[str, Any], index: int):
        """Create a modern table row for a payment"""
        row_color = ft.Colors.WHITE
        
        payment_method = payment["payment_method"]
        check_number = payment.get("check_number", "")
        
        if payment_method == "מזומן":
            method_color = ft.Colors.ORANGE_600
            method_bg = ft.Colors.with_opacity(0.1, ft.Colors.ORANGE_600)
            method_icon = ft.Icons.MONEY
            method_text = payment_method
        elif payment_method == "צ'ק":
            method_color = ft.Colors.PINK_600
            method_bg = ft.Colors.with_opacity(0.1, ft.Colors.PINK_600)
            method_icon = ft.Icons.RECEIPT
            method_text = f"צ'ק #{check_number}" if check_number else "צ'ק"
        elif payment_method == "העברה בנקאית" or payment_method == "העברה":
            method_color = ft.Colors.PURPLE_600
            method_bg = ft.Colors.with_opacity(0.1, ft.Colors.PURPLE_600)
            method_icon = ft.Icons.ACCOUNT_BALANCE
            method_text = payment_method
        else:
            method_color = ft.Colors.BLUE_600
            method_bg = ft.Colors.with_opacity(0.1, ft.Colors.BLUE_600)
            method_icon = ft.Icons.CREDIT_CARD
            method_text = payment_method

        cell_style = {
            "bgcolor": row_color,
            "padding": ft.padding.symmetric(horizontal=16, vertical=16),
            "alignment": ft.alignment.center,
        }
        
        action_buttons = [
            ft.IconButton(
                icon=ft.Icons.EDIT,
                icon_color=ft.Colors.BLUE_600,
                icon_size=18,
                tooltip="עריכה",
                on_click=lambda e, p=payment: self.show_edit_dialog(p)
            ),
            ft.IconButton(
                icon=ft.Icons.DELETE,
                icon_color=ft.Colors.RED_600,
                icon_size=18,
                tooltip="מחיקה",
                on_click=lambda e, p=payment: self.show_delete_dialog(p)
            ),
        ]
        
        if payment.get("note"):
            action_buttons.insert(0, ft.IconButton(
                icon=ft.Icons.NOTE_OUTLINED,
                icon_color=ft.Colors.AMBER_700,
                icon_size=18,
                tooltip="צפה בהערה",
                on_click=lambda e, p=payment: self.show_note_dialog(p)
            ))

        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Text(
                        payment["student_name"], 
                        size=14, 
                        weight=ft.FontWeight.W_500,
                        text_align=ft.TextAlign.CENTER,
                        rtl=True,
                        color=ft.Colors.BLUE_GREY_800
                    ),
                    expand=3, **cell_style
                ),
                ft.Container(
                    content=ft.Container(
                        content=ft.Text(
                            f"{payment['amount']}₪", 
                            size=14, 
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                            color=ft.Colors.GREEN_600
                        ),
                        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREEN_600),
                        padding=ft.padding.symmetric(horizontal=12, vertical=6),
                        border_radius=12,
                    ),
                    expand=2, **cell_style
                ),
                ft.Container(
                    content=ft.Text(
                        payment["date"], 
                        size=13, 
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLUE_GREY_700
                    ),
                    expand=2, **cell_style
                ),
                ft.Container(
                    content=ft.Container(
                        content=ft.Row([
                            ft.Icon(method_icon, size=14, color=method_color),
                            ft.Text(
                                method_text, 
                                size=13, 
                                weight=ft.FontWeight.W_500,
                                color=method_color,
                                rtl=True
                            )
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=4),
                        bgcolor=method_bg,
                        padding=ft.padding.symmetric(horizontal=10, vertical=6),
                        border_radius=12,
                    ),
                    expand=2, **cell_style
                ),
                ft.Container(
                    content=ft.Container(
                        content=ft.Text(
                            payment.get("groups_display", ""), 
                            size=13, 
                            weight=ft.FontWeight.W_500,
                            text_align=ft.TextAlign.CENTER,
                            rtl=True,
                            color=ft.Colors.BLUE_600
                        ),
                        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE_600),
                        padding=ft.padding.symmetric(horizontal=10, vertical=6),
                        border_radius=12,
                    ),
                    expand=2, **cell_style
                ),
                ft.Container(
                    content=ft.Row(
                        action_buttons,
                        alignment=ft.MainAxisAlignment.CENTER, 
                        spacing=0
                    ),
                    expand=2, **cell_style
                ),
            ], spacing=0),
            border=ft.border.only(bottom=ft.BorderSide(0.7, ft.Colors.with_opacity(0.1, ft.Colors.GREY_400))),
        )

    def create_empty_state(self):
        """Create empty state when no payments exist"""
        return ft.Container(
            content=ft.Column([
                ft.Icon(
                    ft.Icons.RECEIPT_LONG_OUTLINED, 
                    size=64, 
                    color=ft.Colors.GREY_400
                ),
                ft.Text(
                    "אין תשלומים להצגה",
                    size=18,
                    weight=ft.FontWeight.W_500,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER,
                    rtl=True
                ),
                ft.Text(
                    "כשיבוצעו תשלומים, הם יופיעו כאן",
                    size=14,
                    color=ft.Colors.GREY_500,
                    text_align=ft.TextAlign.CENTER,
                    rtl=True
                )
            ], 
            spacing=16, 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=ft.padding.all(60),
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.BLUE_GREY_50),
        )

    def create_payments_table(self):
        """Create the modern payments table"""
        if not self.payments_data:
            return self.create_empty_state()
        
        table_rows = [self.create_table_header()]
        
        for index, payment in enumerate(self.payments_data):
            table_rows.append(self.create_table_row(payment, index))

        return ft.Column(
            controls=table_rows,
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
        )

    def go_home(self, e):
        """Navigate back to home page"""
        if self.navigation_handler:
            self.navigation_handler(None, 0)  

    def get_view(self):
        """Get the modern main view of the payment page"""
        title_container = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.PAYMENT, size=32, color=ft.Colors.BLUE_600),
                    ft.Text(
                        "ניהול תשלומים",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_GREY_800,
                        rtl=True
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=12),
                ft.Text(
                    "מעקב אחר כל התשלומים והכנסות במערכת",
                    size=16,
                    color=ft.Colors.BLUE_GREY_500,
                    text_align=ft.TextAlign.CENTER,
                    rtl=True
                )
            ], spacing=8, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.only(bottom=32),
            alignment=ft.alignment.center
        )

        self.stats_section = ft.Container(
            content=self.create_stats_section(),
            margin=ft.margin.only(bottom=32),
            alignment=ft.alignment.center
        )

        self.table_container = ft.Container(
            content=ft.Column([
                self.create_payments_table(),
            ], scroll=ft.ScrollMode.AUTO),
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                offset=ft.Offset(0, 4)
            ),
            border=ft.border.all(1, ft.Colors.with_opacity(0.1, ft.Colors.GREY_400)),
            expand=True,
            clip_behavior=ft.ClipBehavior.HARD_EDGE
        )

        back_button = ft.Container(
            content=ft.ElevatedButton(
                content=ft.Row([
                    ft.Icon(ft.Icons.HOME, size=16, color=ft.Colors.WHITE),
                    ft.Text("חזרה לעמוד הראשי", size=12, color=ft.Colors.WHITE, rtl=True)
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=6, tight=True),
                on_click=self.go_home,
                bgcolor=ft.Colors.BLUE_600,
                color=ft.Colors.WHITE,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=6),
                    padding=ft.padding.symmetric(horizontal=16, vertical=8),
                    shadow_color=ft.Colors.with_opacity(0.3, ft.Colors.BLUE_600),
                    elevation=2
                ),
                height=36,
                width=180,
            ),
            alignment=ft.alignment.center,
            margin=ft.margin.only(top=20)
        )

        main_content = ft.Container(
            content=ft.Column([
                title_container,
                self.stats_section,
                self.table_container,
                back_button,
            ], 
            spacing=0,
            expand=True
            ),
            padding=ft.padding.all(24),
            expand=True,
            bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.BLUE_GREY_50),
        )
        
        return main_content