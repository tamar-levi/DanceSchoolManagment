import flet as ft
import json
from utils.manage_json import ManageJSON  
from components.modern_card import ModernCard
from components.clean_button import CleanButton
from components.modern_dialog import ModernDialog
from utils.payment_utils import PaymentCalculator

class PaymentsView:
    """View for managing student payments"""
    
    def __init__(self, parent, student):
        self.parent = parent
        self.page = parent.page
        self.student_id = student.get('id') 
        self.student = None  
        self.dialog = ModernDialog(self.page)
        self.payment_calculator = PaymentCalculator()
        self.load_student_data()

    def load_student_data(self):
        """Load fresh student data from file"""
        try:
            data_dir = ManageJSON.get_appdata_path() / "data"
            students_file = data_dir / "students.json"
            
            if students_file.exists():
                with open(students_file, "r", encoding="utf-8") as f:
                    students_data = json.load(f)
                    
                for student in students_data.get("students", []):
                    if student.get("id") == self.student_id:
                        self.student = student
                        break
                
                if not self.student:
                    self.student = {"id": self.student_id, "name": "התלמידה לא נמצאה", "payments": []}
            else:
                self.student = {"id": self.student_id, "name": "קובץ לא נמצא", "payments": []}
                
        except Exception as e:
            self.student = {"id": self.student_id, "name": "שגיאה בטעינה", "payments": []}

    def refresh_student_data(self):
        """Refresh student data from file"""
        self.load_student_data()

    def render(self):
        """Render payments view"""
        self.refresh_student_data()
        
        self.parent.clear_layout()
        
        header = self._create_header()
        self.parent.layout.controls.append(header)
        
        payment_explanation = self._create_payment_explanation()
        if payment_explanation:
            self.parent.layout.controls.append(payment_explanation)
        
        payments = self.student.get('payments', [])
        
        if not payments:
            self._render_empty_state()
        else:
            self._render_payments_list()
        
        actions = self._create_actions()
        self.parent.layout.controls.append(actions)
        
        self.page.update()

    def _create_header(self):
        """Create payments header"""
        return ft.Container(
            content=ft.Row([
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color=ft.Colors.GREY_600,
                    on_click=lambda e: self.parent.show_students(),
                    tooltip="חזרה"
                ),
                ft.Text(
                    f"תשלומים - {self.student['name']}",
                    size=20,
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.GREY_800
                )
            ], spacing=8),
            padding=ft.padding.symmetric(vertical=16)
        )

    def _create_payment_explanation(self):
        """Create payment calculation explanation card"""
        try:
            explanation = self.payment_calculator.get_student_payment_explanation(
                self.student_id
            )
            
            if not explanation.get("success"):
                print(f"DEBUG: explanation failed: {explanation}")
                return None
            
            detailed_summary = explanation.get("summary", "")
            
            if not detailed_summary:
                print("DEBUG: No detailed_summary found")
                return None
            
            return ModernCard(
                content=ft.Container(
                    content=ft.Column([
                            ft.Row([
                            ft.Icon(ft.Icons.CALCULATE, size=20, color=ft.Colors.BLUE_600),
                            ft.Text(
                                "הסבר חישוב התשלום",
                                size=16,
                                weight=ft.FontWeight.W_600,
                                color=ft.Colors.GREY_800
                            ),
                            ft.Container(expand=True),
                            ft.IconButton(
                                icon=ft.Icons.INFO_OUTLINE,
                                icon_size=20,
                                icon_color=ft.Colors.BLUE_600,
                                tooltip="פרטים נוספים",
                                on_click=lambda e: self._show_detailed_explanation(explanation)
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        
                        ft.Container(height=12),
                        
                        ft.Container(
                            content=ft.Text(
                                self._create_short_summary(explanation),
                                size=15,
                                color=ft.Colors.GREY_800,
                                selectable=True,
                                text_align=ft.TextAlign.RIGHT,
                                weight=ft.FontWeight.W_500,
                                style=ft.TextStyle(
                                    font_family="Segoe UI",
                                    height=1.4, 
                                )
                            ),
                            alignment=ft.alignment.center_right,
                            width=float("inf")
                        )
                    ], 
                    spacing=0,
                    alignment=ft.CrossAxisAlignment.END,
                    horizontal_alignment=ft.CrossAxisAlignment.END
                    ),
                    padding=ft.padding.all(20),
                    alignment=ft.alignment.top_right,
                    width=float("inf")
                )
            )
            
        except Exception as e:
            print(f"DEBUG: Error creating payment explanation: {e}")
            import traceback
            traceback.print_exc()
            return None


    def _create_short_summary(self, explanation):
        """Create a short summary for the card"""
        try:
            groups = explanation.get("groups", [])
            num_groups = explanation.get("num_groups", 0)
            has_sister = explanation.get("has_sister", False)
            
            total_required = explanation.get("total_required", 0)
            payments_made = explanation.get("payments_made", {})
            total_paid = payments_made.get("total_paid", 0)
            balance = payments_made.get("balance", 0)
            
            periods = explanation.get("periods", [])
            final_monthly_price = 0
            
            if periods:
                last_period = periods[-1]
                final_monthly_price = last_period.get("monthly_price", 0)
            
            lines = []
            
            if final_monthly_price > 0:
                price_line = f"מחיר חודשי: {final_monthly_price}₪"
                if num_groups > 1:
                    price_line += f" ({num_groups} קבוצות)"
                if has_sister:
                    price_line += " (עם הנחת אחיות)"
                lines.append(price_line)
            
            lines.append(f"סה\"כ נדרש עד כה: {total_required}₪")
            
            lines.append(f"שולם: {total_paid}₪")
            
            if balance > 0:
                lines.append(f"יתרת חוב: {balance}₪")
            elif balance == 0:
                lines.append("סטטוס: שולם במלואו")
            else:
                lines.append(f"יתרת זכות: {abs(balance)}₪")
            
            return "\n".join(lines)
            
        except Exception as e:
            print(f"DEBUG: Error in _create_short_summary: {e}")
            import traceback
            traceback.print_exc()
            return "שגיאה בהצגת סיכום התשלום"


    def _show_detailed_explanation(self, explanation):
        """Show detailed payment explanation in dialog"""
        try:
            summary_text = explanation.get("summary", "")
            
            detailed_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CALCULATE, size=24, color=ft.Colors.BLUE_600),
                        ft.Text(
                            f"הסבר מפורט - {explanation.get('student_name', '')}",
                            size=20,
                            weight=ft.FontWeight.W_700,
                            text_align=ft.TextAlign.RIGHT,
                            color=ft.Colors.BLUE_800
                        )
                    ], 
                    alignment=ft.MainAxisAlignment.END,
                    spacing=8
                    ),
                    padding=ft.padding.only(bottom=20, top=10, left=20, right=20),
                    alignment=ft.alignment.center_right,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=ft.border_radius.only(top_left=16, top_right=16)
                ),
                content=ft.Container(
                    content=ft.Column([
                        ft.Container(
                            content=ft.Column([
                                ft.Text(
                                    summary_text,
                                    size=15,
                                    selectable=True,
                                    color=ft.Colors.GREY_900,
                                    text_align=ft.TextAlign.RIGHT,
                                    weight=ft.FontWeight.W_400,
                                    style=ft.TextStyle(
                                        font_family="Segoe UI",
                                        height=1.4, 
                                    )
                                )
                            ], 
                            scroll=ft.ScrollMode.AUTO,
                            alignment=ft.CrossAxisAlignment.END,
                            horizontal_alignment=ft.CrossAxisAlignment.END
                            ),
                            padding=ft.padding.all(25),
                            bgcolor=ft.Colors.WHITE,  
                            border_radius=12,
                            border=ft.border.all(1, ft.Colors.GREY_200),
                            width=750,
                            height=500
                        )
                    ], 
                    alignment=ft.CrossAxisAlignment.END,
                    horizontal_alignment=ft.CrossAxisAlignment.END
                    ),
                    padding=ft.padding.all(20),
                    alignment=ft.alignment.top_right
                ),
                actions=[
                    ft.Container(
                        content=ft.Row([
                            ft.Container(
                                content=ft.ElevatedButton(
                                    content=ft.Row([
                                        ft.Icon(ft.Icons.CLOSE, size=18, color=ft.Colors.WHITE),
                                        ft.Text("סגור", size=16, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE)
                                    ], spacing=8, alignment=ft.MainAxisAlignment.CENTER),
                                    on_click=lambda e: self._close_dialog(detailed_dialog),
                                    style=ft.ButtonStyle(
                                        bgcolor={
                                            "": ft.Colors.BLUE_600,
                                            "hovered": ft.Colors.BLUE_700
                                        },
                                        shape=ft.RoundedRectangleBorder(radius=10),
                                        padding=ft.padding.symmetric(horizontal=35, vertical=15),
                                        elevation=2
                                    )
                                ),
                            )
                        ], 
                        alignment=ft.MainAxisAlignment.CENTER
                        ),
                        padding=ft.padding.all(20)
                    )
                ],
                actions_alignment=ft.MainAxisAlignment.CENTER,
                bgcolor=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=20),
                content_padding=ft.padding.all(0),
            )
            
            self.page.open(detailed_dialog)
            self.page.update()
            
        except Exception as e:
            self.dialog.show_error(f"שגיאה בהצגת ההסבר המפורט: {str(e)}")

    def _close_dialog(self, dialog):
        """Close dialog"""
        self.page.close(dialog)
        self.page.update()

    def _render_empty_state(self):
        """Render empty state"""
        payments = self.student.get('payments', [])
        
        if payments:
            self._render_payments_list()
        
        empty_state = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.RECEIPT_LONG_OUTLINED, size=48, color=ft.Colors.GREY_400),
                ft.Text(
                    "אין תשלומים רשומים",
                    size=16,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
            padding=ft.padding.all(48),
            alignment=ft.alignment.center
        )
        self.parent.layout.controls.append(empty_state)

    def _render_payments_list(self):
        """Render payments list"""
        payments = self.student.get('payments', [])
        total_paid = sum(
            float(p['amount']) for p in payments
            if p['amount'].replace('.', '', 1).isdigit()
        )
        
        summary = ModernCard(
            content=ft.Container(
                content=ft.Row([
                    ft.Text(f"{len(payments)} תשלומים", size=14, color=ft.Colors.GREY_600),
                    ft.Text(f"{total_paid:,.0f}₪", size=18, weight=ft.FontWeight.W_600, color=ft.Colors.GREEN_600)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.padding.all(16)
            )
        )
        self.parent.layout.controls.append(summary)
        
        payments_list = ft.Column(spacing=8)
        
        for payment in payments:
            payment_item = self._create_payment_item(payment)
            payments_list.controls.append(payment_item)
        
        self.parent.layout.controls.append(payments_list)

    def _create_payment_item(self, payment):
        """Create payment item card"""
        return ModernCard(
            content=ft.Container(
                content=ft.Row([
                    ft.Column([
                        ft.Text(
                            f"{payment['amount']}₪",
                            size=16,
                            weight=ft.FontWeight.W_600,
                            color=ft.Colors.GREY_800
                        ),
                        ft.Text(
                            payment['date'],
                            size=12,
                            color=ft.Colors.GREY_600
                        )
                    ], spacing=2),
                    ft.Text(
                        f"צ'ק #{payment['check_number']}" if payment['payment_method'] == 'צ\'ק' and payment.get('check_number') else payment['payment_method'],
                        size=12,
                        color=ft.Colors.BLUE_600
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.padding.all(12)
            )
        )

    def _create_actions(self):
        """Create action buttons"""
        return ft.Container(
            content=ft.Row([
                CleanButton.create(
                    "הוסף תשלום",
                    ft.Icons.ADD,
                    ft.Colors.BLUE_600,
                    lambda e: self.parent.show_add_payment_form(self.student)
                ),
                CleanButton.create(
                    "חזרה",
                    ft.Icons.ARROW_BACK,
                    ft.Colors.GREY_600,
                    lambda e: self.parent.show_students(),
                    variant="outlined"
                )
            ], spacing=16, alignment=ft.MainAxisAlignment.CENTER),
            padding=ft.padding.symmetric(vertical=24)
        )