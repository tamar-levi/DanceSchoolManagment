import flet as ft
from components.modern_card import ModernCard
from components.clean_button import CleanButton


class AddStudentView:
    """View for add student form"""
    
    def __init__(self, parent):
        self.parent = parent
        self.page = parent.page

    def render(self):
        """Render the add student form"""
        # Header Card
        header_card = self._create_header_card()
        self.parent.layout.controls.append(header_card)
        
        # Form Card
        form_card = self._create_form_card()
        self.parent.layout.controls.append(form_card)
        
        # Action Buttons
        actions_card = self._create_actions_card()
        self.parent.layout.controls.append(actions_card)
        
        self.page.update()

    def _create_header_card(self):
        """Create header card"""
        return ModernCard(
            content=ft.Container(
                content=ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color=ft.Colors.GREY_600,
                        on_click=self.parent.go_back,
                        tooltip="חזרה"
                    ),
                    ft.Container(
                        content=ft.Icon(ft.Icons.PERSON_ADD, size=32, color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.GREEN_600,
                        border_radius=50,
                        padding=ft.padding.all(12)
                    ),
                    ft.Column([
                        ft.Text(
                            "הוספת תלמידה חדשה",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREY_800
                        ),
                        ft.Text(
                            f"לקבוצת {self.parent.group_name}",
                            size=16,
                            color=ft.Colors.GREY_600
                        )
                    ], spacing=4, expand=True)
                ], spacing=16),
                padding=ft.padding.all(24)
            ),
            gradient=ft.LinearGradient(
                colors=[ft.Colors.WHITE, ft.Colors.with_opacity(0.98, ft.Colors.GREEN_50)],
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
            )
        )

    def _create_form_card(self):
        """Create form card with all fields"""
        return ModernCard(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        "פרטי התלמידה",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREY_800
                    ),
                    ft.Divider(height=1, color=ft.Colors.GREY_200),
                    
                    # Personal Info Section
                    self._create_personal_info_section(),
                    
                    # Group & Payment Section
                    self._create_group_payment_section(),
                    
                    # Info box
                    self._create_info_box()
                ], spacing=24),
                padding=ft.padding.all(24)
            )
        )

    def _create_personal_info_section(self):
        """Create personal info section"""
        return ft.Container(
            content=ft.Column([
                ft.Text(
                    "👤 פרטים אישיים",
                    size=16,
                    weight=ft.FontWeight.W_500,
                    color=ft.Colors.GREY_700
                ),
                self.parent.name_input,
                self.parent.id_input,
                self.parent.phone_input,
            ], spacing=16),
            bgcolor=ft.Colors.GREY_50,
            border_radius=12,
            padding=ft.padding.all(16)
        )

    def _create_group_payment_section(self):
        """Create group and payment section"""
        return ft.Container(
            content=ft.Column([
                ft.Text(
                    "🏫 פרטי קבוצה ותשלום",
                    size=16,
                    weight=ft.FontWeight.W_500,
                    color=ft.Colors.GREY_700
                ),
                self.parent.group_dropdown,
                self.parent.payment_status_dropdown,
                self.parent.join_date_input,
                self.parent.has_sister_checkbox
            ], spacing=16),
            bgcolor=ft.Colors.BLUE_50,
            border_radius=12,
            padding=ft.padding.all(16)
        )

    def _create_info_box(self):
        """Create info box"""
        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.INFO_OUTLINE, size=16, color=ft.Colors.BLUE_600),
                ft.Text(
                    "כל השדות נדרשים למילוי. התלמידה תתווסף לקבוצה שנבחרה.",
                    size=12,
                    color=ft.Colors.GREY_600
                )
            ], spacing=8),
            bgcolor=ft.Colors.BLUE_50,
            border_radius=8,
            padding=ft.padding.all(12)
        )

    def _create_actions_card(self):
        """Create action buttons card"""
        return ModernCard(
            content=ft.Container(
                content=ft.Row([
                    CleanButton.create(
                        "הוסף תלמידה",
                        ft.Icons.SAVE,
                        ft.Colors.GREEN_600,
                        self.parent.add_student
                    ),
                    CleanButton.create(
                        "ביטול",
                        ft.Icons.CANCEL,
                        ft.Colors.GREY_600,
                        self.parent.go_back,
                        variant="outlined"
                    )
                ], spacing=16, alignment=ft.MainAxisAlignment.CENTER),
                padding=ft.padding.all(20)
            )
        )
