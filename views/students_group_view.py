import flet as ft
from components.modern_card import ModernCard
from components.clean_button import CleanButton

class StudentsGroupView:
    """View for displaying students list"""
    
    def __init__(self, parent):
        self.parent = parent
        self.page = parent.page
        self.group_name = parent.group_name
        self.data_manager = parent.data_manager

    def render(self):
        """Render the students list view"""
        header = self._create_header()
        self.parent.layout.controls.append(header)
        
        students = self.data_manager.get_students_by_group(self.group_name)
        
        if not students:
            self._render_empty_state()
        else:
            self._render_students_grid(students)
        
        actions = self._create_action_buttons()
        self.parent.layout.controls.append(actions)
        
        self.page.update()

    def _create_header(self):
        """Create page header"""
        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.PEOPLE_ALT_OUTLINED, size=24, color=ft.Colors.GREY_800),
                ft.Text(
                    f"תלמידות - {self.group_name}",
                    size=24,
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.GREY_800,
                ),
            ], spacing=12),
            padding=ft.padding.symmetric(vertical=16)
        )

    def _render_empty_state(self):
        """Render empty state when no students"""
        empty_state = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.PERSON_ADD_ALT_1_OUTLINED, size=48, color=ft.Colors.GREY_400),
                ft.Text(
                    "אין תלמידות בקבוצה זו",
                    size=18,
                    weight=ft.FontWeight.W_500,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "הוסיפו את התלמידה הראשונה",
                    size=14,
                    color=ft.Colors.GREY_500,
                    text_align=ft.TextAlign.CENTER
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
            padding=ft.padding.all(48),
            alignment=ft.alignment.center
        )
        self.parent.layout.controls.append(empty_state)

    def _render_students_grid(self, students):
        """Render students in a responsive grid"""
        count_text = ft.Container(
            content=ft.Text(
                f"{len(students)} תלמידות",
                size=14,
                color=ft.Colors.GREY_600
            ),
            padding=ft.padding.only(bottom=16)
        )
        self.parent.layout.controls.append(count_text)
        
        students_grid = ft.Container(
            content=ft.Column([
                ft.ResponsiveRow([
                    ft.Container(
                        content=self._create_student_card(student),
                        col={"xs": 12, "sm": 6, "md": 4, "lg": 3}
                    )
                    for student in students
                ], spacing=16, run_spacing=16)
            ], scroll=ft.ScrollMode.AUTO),
        )
        self.parent.layout.controls.append(students_grid)

    def _is_student_in_multiple_groups(self, student_id):
        """Check if student is in multiple groups"""
        try:
            all_students = self.data_manager.get_all_students()
            
            if all_students:
                for student in all_students:
                    if isinstance(student, dict) and student.get('id') == student_id:
                        student_groups = self._get_student_groups(student)
                        return len(student_groups) > 1
            return False
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return False

    def _get_student_groups(self, student):
        """Get student groups - supports both old and new format"""
        if "groups" in student:
            return student["groups"]
        elif "group" in student:
            return [student["group"]]
        else:
            return []

    def _get_payment_display_status(self, student):
        """Get payment status for display with 'paid until now' logic"""
        from utils.payment_utils import PaymentCalculator        
        payment_calculator = PaymentCalculator()

        payments = student.get('payments', [])
        total_paid = 0.0
        for payment in payments:
            try:
                amount = payment.get('amount', 0)
                if isinstance(amount, str):
                    amount = float(amount) if amount.strip() else 0
                elif isinstance(amount, (int, float)):
                    amount = float(amount)
                else:
                    amount = 0
                total_paid += amount
            except (ValueError, AttributeError):
                continue

        student_id = student.get('id', '')
        if student_id:
            total_owed_until_now = payment_calculator.get_student_payment_amount_until_now(student_id)
        else:
            student_groups = student.get('groups', [])
            total_owed_until_now = 0
            for group_name in student_groups:
                group_id = payment_calculator.get_group_id_by_name(group_name)
                if group_id:
                    join_date = payment_calculator.get_student_join_date_for_group(student_id, group_id)
                    if join_date:
                        group_payment = payment_calculator.get_payment_amount_until_now(group_id, join_date)
                        total_owed_until_now += group_payment

        total_course_payment = 0
        try:
            groups_with_dates = payment_calculator.get_student_groups_with_join_dates(student_id)
            latest_end_date = None
            from datetime import datetime
            for g in groups_with_dates:
                end = g.get("end_date")
                if end:
                    try:
                        dt = datetime.strptime(end, "%d/%m/%Y")
                        if latest_end_date is None or dt > latest_end_date:
                            latest_end_date = dt
                    except Exception:
                        continue

            if latest_end_date:
                periods = payment_calculator.create_discount_periods_for_student(student_id, latest_end_date)
                for period in periods:
                    pr = payment_calculator.calculate_period_payment_with_discount_rules(student_id, period)
                    if pr.get("success"):
                        total_course_payment += pr.get("total_payment", 0)
        except Exception:
            total_course_payment = 0

        try:
            total_owed_until_now = float(total_owed_until_now)
        except Exception:
            total_owed_until_now = 0

        if total_course_payment and total_paid >= total_course_payment:
            if total_paid == total_course_payment:
                return "שולם במלואו"
            else:
                return "שילם יותר (זיכוי)"
        else:
            if total_paid >= total_owed_until_now and total_owed_until_now > 0:
                return "שולם חלקית"
            else:
                return "חוב"



    def _create_student_card(self, student):
        """Create a student card"""
        is_multi_group = self._is_student_in_multiple_groups(student['id'])
        
        avatar = ft.Container(
            content=ft.Text(
                student['name'][0] if student['name'] else "?",
                color=ft.Colors.WHITE,
                size=16,
                weight=ft.FontWeight.W_600,
                text_align=ft.TextAlign.CENTER
            ),
            bgcolor=ft.Colors.BLUE_600,
            border_radius=20,
            width=36,
            height=36,
            alignment=ft.alignment.center,
        )
        
        display_payment_status = self._get_payment_display_status(student)
        status_color = self._get_payment_status_color(display_payment_status)
        
        status_dot = ft.Container(
            width=8,
            height=8,
            bgcolor=status_color,
            border_radius=4
        )
        
        name_controls = [
            ft.Text(
                student['name'],
                size=16,
                weight=ft.FontWeight.W_600,
                color=ft.Colors.GREY_800,
                overflow=ft.TextOverflow.ELLIPSIS
            )
        ]
        
        if is_multi_group:
            name_controls.append(
                ft.Icon(
                    ft.Icons.STAR,
                    size=20,
                    color=ft.Colors.AMBER_600,
                    tooltip="תלמידה במספר קבוצות"
                )
            )
        
        name_row = ft.Row(name_controls, spacing=8)
        
        card_content = ft.Column([
            ft.Row([
                avatar,
                ft.Column([
                    name_row,
                    ft.Row([
                        status_dot,
                        ft.Text(
                            display_payment_status, 
                            size=12,
                            color=ft.Colors.GREY_600,
                            overflow=ft.TextOverflow.ELLIPSIS
                        )
                    ], spacing=6)
                ], spacing=2, expand=True)
            ], spacing=12),
            
            self._create_contact_info(student),
            
            self._create_card_actions(student)
        ], spacing=12)
        
        return ModernCard(
            content=ft.Container(
                content=card_content,
                padding=ft.padding.all(16)
            ),
            hover_effect=True
        )

    def _create_contact_info(self, student):
        """Create contact information section"""
        from utils.payment_utils import PaymentCalculator
        
        display_join_date = student.get('join_date', 'לא ידוע') 
        
        try:
            payment_calculator = PaymentCalculator()
            group_id = payment_calculator.get_group_id_by_name(self.group_name)
            student_id = student.get('id', '')
            
            if group_id and student_id:
                join_date_for_group = payment_calculator.get_student_join_date_for_group(student_id, group_id)
                if join_date_for_group:
                    display_join_date = join_date_for_group
        except Exception as e:
            print(f"Error getting join date for group: {e}")
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.PHONE, size=14, color=ft.Colors.GREY_500),
                    ft.Text(
                        student.get('phone', 'לא צוין'),
                        size=12,
                        color=ft.Colors.GREY_600,
                        overflow=ft.TextOverflow.ELLIPSIS
                    )
                ], spacing=6),
                ft.Row([
                    ft.Icon(ft.Icons.CALENDAR_TODAY, size=14, color=ft.Colors.GREY_500),
                    ft.Text(
                        display_join_date,  
                        size=12,
                        color=ft.Colors.GREY_600,
                        overflow=ft.TextOverflow.ELLIPSIS
                    )
                ], spacing=6)
            ], spacing=4),
            padding=ft.padding.symmetric(vertical=8)
        )

    def _create_card_actions(self, student):
        """Create action buttons for student card"""
        return ft.Row([
            CleanButton.create_icon_button(
                ft.Icons.EDIT_OUTLINED,
                ft.Colors.GREY_600,
                "עריכה",
                lambda e: self.parent.edit_student(student)
            ),
            CleanButton.create_icon_button(
                ft.Icons.PAYMENT_OUTLINED,
                ft.Colors.GREY_600,
                "תשלומים",
                lambda e: self.parent.show_payments(student)
            ),
            CleanButton.create_icon_button(
                ft.Icons.DELETE_OUTLINE,
                ft.Colors.RED_400,
                "מחיקה",
                lambda e: self.parent.delete_student(student),
                ft.Colors.RED_50
            )
        ], spacing=4, alignment=ft.MainAxisAlignment.END)

    def _create_action_buttons(self):
        """Create main action buttons"""
        return ft.Container(
            content=ft.Row([
                CleanButton.create(
                    "הוסף תלמידה",
                    ft.Icons.ADD,
                    ft.Colors.BLUE_600,
                    self.parent.go_to_add_student_page
                ),
                CleanButton.create(
                    "חזרה",
                    ft.Icons.ARROW_BACK,
                    ft.Colors.GREY_600,
                    self.parent.go_back,
                    variant="outlined"
                )
            ], spacing=16, alignment=ft.MainAxisAlignment.CENTER),
            padding=ft.padding.symmetric(vertical=24)
        )

    def _get_payment_status_color(self, payment_status):
        """Get color for payment status"""
        if payment_status in ("שולם במלואו", "שילם יותר (זיכוי)"):
            return ft.Colors.GREEN_600
        elif payment_status in ("שולם חלקית",):
            return ft.Colors.ORANGE_500
        elif payment_status == "חוב":
            return ft.Colors.RED_500
        else:
            return ft.Colors.GREY_600
