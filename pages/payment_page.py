import json
import flet as ft
from typing import Dict, Any
from utils.manage_json import ManageJSON

class PaymentPage:
    def __init__(self, page: ft.Page, navigation_handler=None):
        self.page = page
        self.navigation_handler = navigation_handler
        self.payments_data = []
        
        self.load_payments()
        
    def load_payments(self):
        """Load payments data from students.json"""
        try:
            data_dir = ManageJSON.get_appdata_path() / "data"
            students_file = data_dir / "students.json"
            
            if students_file.exists():
                with open(students_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                    for student in data.get("students", []):
                        student_name = student.get("name", "")
                        student_groups = student.get("groups", [])
                        
                        for payment in student.get("payments", []):
                            payment_data = {
                                "student_name": student_name,
                                "amount": payment.get("amount", "0"),
                                "date": payment.get("date", ""),
                                "payment_method": payment.get("payment_method", ""),
                                "groups": student_groups,
                                "groups_display": ", ".join(student_groups)
                            }
                            
                            if payment.get("check_number"):
                                payment_data["check_number"] = payment.get("check_number")
                            
                            self.payments_data.append(payment_data)
        except Exception as e:
            print(f"Error loading payments: {e}")


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
            ], spacing=0),
            border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.with_opacity(0.1, ft.Colors.GREY_400))),
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

        stats_section = ft.Container(
            content=self.create_stats_section(),
            margin=ft.margin.only(bottom=32),
            alignment=ft.alignment.center
        )

        table_container = ft.Container(
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
                stats_section,
                table_container,
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