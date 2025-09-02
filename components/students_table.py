import flet as ft
from typing import List, Dict, Any
from utils.payment_utils import PaymentCalculator

class StudentsTable:
    """Students table component"""

    def __init__(self):
        self.table_container = ft.Column(controls=[], spacing=0, scroll=ft.ScrollMode.AUTO)
        self.payment_calculator = PaymentCalculator()

    def create_header(self) -> ft.Container:
        """Create table header row"""
        header_style = {
            "bgcolor": ft.Colors.with_opacity(0.8, ft.Colors.BLUE_GREY_900),
            "padding": ft.padding.symmetric(horizontal=16, vertical=20),
            "alignment": ft.alignment.center,
        }

        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Text("שם התלמידה", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE),
                    expand=2, **header_style
                ),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.BADGE, size=16, color=ft.Colors.WHITE70),
                        ft.Text("ת.ז", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE)
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=4),
                    expand=2, **header_style
                ),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.PHONE, size=16, color=ft.Colors.WHITE70),
                        ft.Text("טלפון", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE)
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
                        ft.Icon(ft.Icons.PAYMENT, size=16, color=ft.Colors.WHITE70),
                        ft.Text("סטטוס תשלום", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE)
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=4),
                    expand=2, **header_style
                ),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.DATE_RANGE, size=16, color=ft.Colors.WHITE70),
                        ft.Text("תאריך הצטרפות", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE)
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=4),
                    expand=2, **header_style
                ),

                ft.Container(
                    content=ft.Text("אחות", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE),
                    expand=1,
                    **header_style
                ),
            ], spacing=0),
            border_radius=ft.border_radius.only(top_left=12, top_right=12),
        )

    def create_row(self, student: Dict[str, Any], index: int) -> ft.Container:
        """Create a table row for a student"""
        row_color =  ft.Colors.WHITE
        student_id = student.get("id") 
        payment_status = student.get("payment_status", "")
        amount = self.calculate_total_paid_advanced(student.get("payments", []))
        payment_color, payment_bg, payment_icon, display_text = self._get_payment_style(
            payment_status, amount, student.get('groups', []), student.get("join_date"), student_id
        )

        cell_style = {
            "bgcolor": row_color,
            "padding": ft.padding.symmetric(horizontal=16, vertical=16),
            "alignment": ft.alignment.center,
        }

        has_sister = student.get("has_sister", False)
        sister_mark = "✔" if has_sister else "✘"
        sister_color = ft.Colors.GREEN_700 if has_sister else ft.Colors.RED_700

        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Text(
                        student.get("name", ""),
                        size=14,
                        weight=ft.FontWeight.W_500,
                        text_align=ft.TextAlign.CENTER,
                        rtl=True,
                        color=ft.Colors.BLUE_GREY_800
                    ),
                    expand=2, **cell_style
                ),
                ft.Container(
                    content=ft.Text(
                        student.get("id", ""),
                        size=13,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLUE_GREY_700,
                        font_family="monospace"
                    ),
                    expand=2, **cell_style
                ),
                ft.Container(
                    content=ft.Text(
                        student.get("phone", ""),
                        size=13,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLUE_GREY_700,
                        font_family="monospace"
                    ),
                    expand=2, **cell_style
                ),
                ft.Container(
                    content=ft.Container(
                        content=ft.Text(
                            ", ".join(student.get("groups", [])),
                            size=13,
                            weight=ft.FontWeight.W_500,
                            text_align=ft.TextAlign.CENTER,
                            rtl=True,
                            color=ft.Colors.BLUE_600
                        ),
                        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE_600),
                        padding=ft.padding.symmetric(horizontal=12, vertical=6),
                        border_radius=16,
                    ),
                    expand=2, **cell_style
                ),
                ft.Container(
                    content=ft.Container(
                        content=ft.Row([
                            ft.Icon(payment_icon, size=16, color=payment_color),
                            ft.Text(
                                display_text,  
                                size=13,
                                weight=ft.FontWeight.W_500,
                                color=payment_color,
                                rtl=True
                            )
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=4),
                        bgcolor=payment_bg,
                        padding=ft.padding.symmetric(horizontal=12, vertical=6),
                        border_radius=16,
                    ),
                    expand=2, **cell_style
                ),
                ft.Container(
                    content=ft.Text(
                        student.get("join_date", ""),
                        size=13,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLUE_GREY_700
                    ),
                    expand=2, **cell_style
                ),
                ft.Container(
                    content=ft.Text(
                        sister_mark,
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=sister_color,
                        text_align=ft.TextAlign.CENTER
                    ),
                    expand=1,
                    **cell_style
                ),
            ], spacing=0),
            border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.with_opacity(0.1, ft.Colors.GREY_400))),
        )

    def _get_payment_style(self, payment_status: str, amount, student_groups, join_date, student_id=None):
        """Get payment status styling"""
        if payment_status == "שולם":
            return ft.Colors.GREEN_600, ft.Colors.with_opacity(0.1, ft.Colors.GREEN_600), ft.Icons.CHECK_CIRCLE, "שולם"
        elif payment_status == "חוב":
            if student_id:
                total_owed_until_now = self.payment_calculator.get_student_payment_amount_until_now(student_id)
                
                latest_end_date = ""
                for group_name in student_groups:
                    group_id = self.payment_calculator.get_group_id_by_name(group_name)
                    if group_id:
                        group = self.payment_calculator.get_group_by_id(group_id)
                        group_end_date = group.get("group_end_date", "") if group else ""
                        if group_end_date > latest_end_date:
                            latest_end_date = group_end_date
                
                if latest_end_date:
                    first_group_name = student_groups[0] if student_groups else None
                    if first_group_name:
                        first_group_id = self.payment_calculator.get_group_id_by_name(first_group_name)
                        if first_group_id:
                            actual_join_date = self.payment_calculator.get_student_join_date_for_group(student_id, first_group_id)
                            if actual_join_date:
                                all_course_payment = self.payment_calculator.get_student_payment_amount_for_period(
                                    student_id, first_group_id, actual_join_date, latest_end_date
                                )
                            else:
                                all_course_payment = 0
                        else:
                            all_course_payment = 0
                    else:
                        all_course_payment = 0
                else:
                    all_course_payment = 0
            else:
                total_owed_until_now = 0
                all_course_payment = 0
                for group_name in student_groups:
                    group_id = self.payment_calculator.get_group_id_by_name(group_name)
                    if group_id:
                        actual_join_date = self.payment_calculator.get_student_join_date_for_group(student_id, group_id) if student_id else join_date
                        if actual_join_date:
                            group_payment = self.payment_calculator.get_payment_amount_until_now(group_id, actual_join_date)
                            group = self.payment_calculator.get_group_by_id(group_id)
                            group_end_date = group.get("group_end_date", "") if group else ""
                            if group_end_date:
                                group_course_payment = self.payment_calculator.get_payment_amount_for_period(group_id, actual_join_date, group_end_date)
                            else:
                                group_course_payment = 0
                            total_owed_until_now += group_payment
                            all_course_payment += group_course_payment
            
            
            if amount >= total_owed_until_now:
                return ft.Colors.ORANGE_600, ft.Colors.with_opacity(0.1, ft.Colors.ORANGE_600), ft.Icons.PENDING, "שולם עד כה"
            else:
                return ft.Colors.RED_600, ft.Colors.with_opacity(0.1, ft.Colors.RED_600), ft.Icons.ERROR, "חוב"
        else:
            return ft.Colors.GREY_600, ft.Colors.with_opacity(0.1, ft.Colors.GREY_600), ft.Icons.HELP, payment_status


    def update(self, students: List[Dict[str, Any]]):
        """Update table with students data"""
        self.table_container.controls = [self.create_header()]

        if students:
            for index, student in enumerate(students):
                self.table_container.controls.append(self.create_row(student, index))

    def get_container(self) -> ft.Container:
        """Get the table container"""
        return ft.Container(
            content=ft.Column([self.table_container], scroll=ft.ScrollMode.AUTO),
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            border=ft.border.all(1, ft.Colors.with_opacity(0.1, ft.Colors.GREY_400)),
            expand=True,
            clip_behavior=ft.ClipBehavior.HARD_EDGE
        )
    

    def calculate_total_paid_advanced(self, payments_array):
        total_paid = 0.0
        
        if not payments_array or not isinstance(payments_array, list):
            return 0.0
        
        for payment in payments_array:
            if isinstance(payment, dict) and 'amount' in payment:
                amount_str = payment.get('amount', '0')
                
                try:
                    clean_amount = str(amount_str).replace(',', '.')
                    amount = float(clean_amount)
                    total_paid += amount
                except (ValueError, TypeError):
                    continue
        
        return total_paid

