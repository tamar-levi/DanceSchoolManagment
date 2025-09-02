import flet as ft
import os
from typing import Optional
from pages.choose_group_attendance_page import AttendancePage
from pages.groups_page import GroupsPage  
from pages.students_list import StudentsListPage
from pages.payment_page import PaymentPage
from utils.dashboard_data import get_all_dashboard_data

def format_currency(amount):
    return f"₪{amount:,}"


class MainApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "זה הריקוד שלך"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.window_width = 1200
        self.page.window_height = 800
        self.page.window_min_width = 1000
        self.page.window_min_height = 700
        self.page.rtl = True
        self.page.fonts = {
            "Segoe UI": "fonts/SegoeUI.ttf" if os.path.exists("fonts/SegoeUI.ttf") else None
        }
        self.dashboard_data = get_all_dashboard_data()
        self.current_page_index = 0
        self.sidebar_buttons = []
        self.progress_bar = None
        self.progress_text = None
        self.groups_page = None
        self.setup_page()

    def setup_page(self):
        self.sidebar = self.create_sidebar()
        self.content_area = ft.Container(
            content=self.create_home_page(),
            bgcolor="#f8fafc",
            expand=True,
            padding=ft.padding.all(30),
        )
        
        main_row = ft.Row([
            self.sidebar,
            self.content_area
        ], spacing=0, expand=True)
        
        self.page.add(main_row)

    def create_sidebar_button(self, text: str, icon: str, index: int, is_selected: bool = False):
        """Create an animated sidebar button using built-in Flet components"""
        
        def on_click(e):
            self.navigate_to_page(index)
        
        button_content = ft.Row([
            ft.Icon(
                icon,
                color=ft.Colors.WHITE if is_selected else ft.Colors.GREY_400,
                size=20
            ),
            ft.Text(
                text,
                color=ft.Colors.WHITE if is_selected else ft.Colors.GREY_400,
                size=14,
                weight=ft.FontWeight.BOLD if is_selected else ft.FontWeight.NORMAL
            )
        ], spacing=10)
        
        button_container = ft.Container(
            content=button_content,
            padding=ft.padding.all(12),
            border_radius=8,
            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE) if is_selected else None,
            on_click=on_click,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
            ink=True,
        )
        
        if is_selected:
            return ft.Row([
                ft.Container(
                    width=4,
                    height=40,
                    bgcolor=ft.Colors.BLUE,
                    border_radius=2,
                ),
                ft.Container(
                    content=button_container,
                    expand=True
                )
            ], spacing=0)
        else:
            return ft.Container(
                content=button_container,
                margin=ft.margin.only(left=4)
            )

    def create_sidebar(self):
        home_btn = self.create_sidebar_button("דף הבית", ft.Icons.HOME, 0, self.current_page_index == 0)
        groups_btn = self.create_sidebar_button("קבוצות", ft.Icons.GROUP, 1, self.current_page_index == 1)
        attendance_btn = self.create_sidebar_button("נוכחות", ft.Icons.CHECK_CIRCLE, 2, self.current_page_index == 2)
        payment_btn = self.create_sidebar_button("תשלומים", ft.Icons.CREDIT_CARD, 3, self.current_page_index == 3)
        students_btn = self.create_sidebar_button("רשימת התלמידות", ft.Icons.LIST, 4, self.current_page_index == 4)

        self.sidebar_buttons = [home_btn, groups_btn, attendance_btn, payment_btn, students_btn]

        def toggle_dark_mode(e):
            self.toggle_dark_mode(e.control.value)
            
        dark_mode_switch = ft.Switch(
            value=False,
            on_change=toggle_dark_mode,
            active_color=ft.Colors.BLUE,
            inactive_thumb_color=ft.Colors.WHITE,
            inactive_track_color=ft.Colors.GREY_400,
        )

        sidebar_content = ft.Column([
            ft.Container(
                content=ft.Text("זה הריקוד שלך", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                padding=ft.padding.all(20),
                alignment=ft.alignment.center,
            ),
            
            ft.Divider(color=ft.Colors.GREY_600, height=1),            
            ft.Container(
                content=ft.Column([
                    home_btn,
                    groups_btn,
                    attendance_btn,
                    payment_btn,
                    students_btn,
                ], spacing=5),
                padding=ft.padding.symmetric(horizontal=10, vertical=20),
            ),
            ft.Container(expand=True),
            ft.Container(
                content=ft.Column([
                    ft.Text("הגדרות", size=12, color=ft.Colors.GREY_500),
                    ft.Row([
                        dark_mode_switch,
                        ft.Text("מצב כהה", color=ft.Colors.GREY_400),
                    ], spacing=10),
                ], spacing=10),
                padding=ft.padding.all(20),
            ),
        ], spacing=0)

        return ft.Container(
            content=sidebar_content,
            width=250,
            bgcolor="#2c3e50",
            height=self.page.window_height,
        )

    def navigate_to_page(self, page_index: int):
        """Navigate to a specific page"""
        self.current_page_index = page_index
        self.sidebar.content = self.create_sidebar().content
        if page_index == 0:
            self.content_area.content = self.create_home_page()
            self.refresh_home_page()
        elif page_index == 1:
            if self.groups_page is None:
                self.groups_page = GroupsPage(self.page, self.handle_navigation)
            self.content_area.content = self.groups_page.get_view()
        elif page_index == 2:
            attendance_page = AttendancePage(self.page, self.handle_navigation)
            self.content_area.content = attendance_page.get_view()
        elif page_index == 3:
            payment_page = PaymentPage(self.page, self.handle_navigation)
            self.content_area.content = payment_page.get_view()
        elif page_index == 4:
            students_page = StudentsListPage(self.page, self.handle_navigation)
            self.content_area.content = students_page.get_view()
        self.page.update()

    def handle_navigation(self, page_instance, page_index=None):
        """Handle navigation from sub-pages"""
        if page_index is not None:
            self.navigate_to_page(page_index)
        elif page_instance is not None:
            self.content_area.content = page_instance.get_view()
            self.page.update()

    def create_placeholder_page(self, title: str):
        """Create placeholder page for non-implemented pages"""
        return ft.Column([
            ft.Text(f"עמוד {title}", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("עמוד זה יומר בהמשך", size=16, color=ft.Colors.GREY_600),
        ], spacing=20)

    def create_animated_card(self, content, height: Optional[int] = None, width: Optional[int] = None, gradient_colors=None, on_click=None):
        """Create an animated card using built-in Flet components"""
        return ft.Container(
            content=content,
            bgcolor=ft.Colors.WHITE if not gradient_colors else None,
            gradient=ft.LinearGradient(
                colors=gradient_colors,
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
            ) if gradient_colors else None,
            border_radius=12,
            padding=ft.padding.all(20),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                offset=ft.Offset(0, 4),
            ),
            height=height,
            width=width,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            on_click=on_click,
            ink=True if on_click else False,
        )

    def create_home_page(self):
        welcome_section = ft.Container(
            content=ft.Column([
                ft.Text(
                    "ברוכים הבאים לזה הריקוד שלך", 
                    size=32, 
                    weight=ft.FontWeight.BOLD, 
                    color="#1a202c"
                ),
                ft.Text(
                    "הבית המקצועי לבלט ולמחול", 
                    size=16, 
                    color="#718096"
                ),
            ], spacing=8),
            padding=ft.padding.only(bottom=30),
        )

        students_card = self.create_animated_card(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.PERSON, size=24, color="#4299e1"),
                        bgcolor="#ebf8ff",
                        border_radius=8,
                        padding=ft.padding.all(8),
                    ),
                    ft.Column([
                        ft.Text("תלמידות", size=14, color="#718096"),
                        ft.Text(str(self.dashboard_data['total_students']), size=28, 
                               weight=ft.FontWeight.BOLD, color="#1a202c"),
                    ], spacing=2, expand=True),
                ], spacing=12, alignment=ft.MainAxisAlignment.START),
            ], spacing=5),
            height=100
        )

        groups_card = self.create_animated_card(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.GROUP, size=24, color="#48bb78"),
                        bgcolor="#f0fff4",
                        border_radius=8,
                        padding=ft.padding.all(8),
                    ),
                    ft.Column([
                        ft.Text("קבוצות פעילות", size=14, color="#718096"),
                        ft.Text(str(self.dashboard_data['total_groups']), size=28, 
                               weight=ft.FontWeight.BOLD, color="#1a202c"),
                    ], spacing=2, expand=True),
                ], spacing=12, alignment=ft.MainAxisAlignment.START),
            ], spacing=5),
            height=100
        )

        payments_card = self.create_animated_card(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, size=24, color="#ed8936"),
                        bgcolor="#fffaf0",
                        border_radius=8,
                        padding=ft.padding.all(8),
                    ),
                    ft.Column([
                        ft.Text("הכנסות החודש", size=14, color="#718096"),
                        ft.Text(format_currency(self.dashboard_data['monthly_payments']), size=24, 
                               weight=ft.FontWeight.BOLD, color="#1a202c"),
                    ], spacing=2, expand=True),
                ], spacing=12, alignment=ft.MainAxisAlignment.START),
            ], spacing=5),
            height=100
        )

        attendance_card = self.create_animated_card(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.ANALYTICS, size=24, color="#9f7aea"),
                        bgcolor="#faf5ff",
                        border_radius=8,
                        padding=ft.padding.all(8),
                    ),
                    ft.Column([
                        ft.Text("נוכחות חודשית", size=14, color="#718096"),
                        ft.Text(f"{self.dashboard_data['attendance_percentage']}%", size=28, 
                               weight=ft.FontWeight.BOLD, color="#1a202c"),
                    ], spacing=2, expand=True),
                ], spacing=12, alignment=ft.MainAxisAlignment.START),
            ], spacing=5),
            height=100
        )

        stats_grid = ft.Row([
            ft.Container(content=students_card, expand=1),
            ft.Container(content=groups_card, expand=1),
            ft.Container(content=payments_card, expand=1),
            ft.Container(content=attendance_card, expand=1),
        ], spacing=20)

        groups_section = self.create_groups_section()

        return ft.Column([
            welcome_section,
            stats_grid,
            groups_section,
        ], spacing=40, scroll=ft.ScrollMode.AUTO)

    def create_groups_section(self):
        """Create a section displaying all groups"""
        try:
            from utils.students_data_manager import StudentsDataManager
            data_manager = StudentsDataManager()
            groups = data_manager._get_groups()
            
            if not groups:
                return ft.Container(
                    content=ft.Column([
                        ft.Text("קבוצות", size=24, weight=ft.FontWeight.BOLD, color="#1a202c"),
                        ft.Text("אין קבוצות רשומות במערכת", size=16, color="#718096"),
                    ], spacing=10),
                    padding=ft.padding.symmetric(vertical=20),
                )
            
            group_cards = []
            for i, group in enumerate(groups):
                if isinstance(group, str):
                    group_name = group
                    teacher = "לא צוין"
                    day = "לא צוין"
                    time = "לא צוין"
                    students_count = 0
                    group_data = {
                        "name": group_name, 
                        "teacher": teacher, 
                        "day": day, 
                        "time": time, 
                        "students": [],
                        "members": [] 
                    }
                else:
                    group_name = group.get('name', group.get('group_name', 'קבוצה ללא שם'))
                    teacher = group.get('teacher', group.get('instructor', 'לא צוין'))
                    day = group.get('day', group.get('day_of_week', 'לא צוין'))
                    time = group.get('time', group.get('class_time', 'לא צוין'))
                    students_count = len(group.get('students', group.get('members', [])))
                    group_data = group
                
                def create_group_click_handler(group_info):
                    def on_group_click(e):
                        self.navigate_to_group_page(group_info)
                    return on_group_click
                
                group_card = self.create_animated_card(
                    content=ft.Column([
                        ft.Row([
                            ft.Container(
                                content=ft.Icon(ft.Icons.GROUP, size=20, color="#4299e1"),
                                bgcolor="#ebf8ff",
                                border_radius=6,
                                padding=ft.padding.all(6),
                            ),
                            ft.Column([
                                ft.Text(group_name, size=16, weight=ft.FontWeight.BOLD, color="#1a202c"),
                                ft.Text(f"מורה: {teacher}", size=12, color="#718096"),
                            ], spacing=2, expand=True),
                        ], spacing=10),
                        ft.Divider(height=1, color="#e2e8f0"),
                        ft.Container(
                            content=ft.Text("לחץ לפרטים ←", size=11, color="#4299e1", weight=ft.FontWeight.W_500),
                            margin=ft.margin.only(top=5),
                        )
                    ], spacing=8),
                    height=140,
                    on_click=create_group_click_handler(group_data)
                )
                group_cards.append(group_card)
            
            rows = []
            for i in range(0, len(group_cards), 4):
                row_cards = group_cards[i:i+4]
                while len(row_cards) < 4:
                    row_cards.append(ft.Container()) 
                
                row = ft.Row([
                    ft.Container(content=card, expand=1) for card in row_cards
                ], spacing=15)
                rows.append(row)
            
            return ft.Container(
                content=ft.Column([
                    ft.Text("קבוצות", size=24, weight=ft.FontWeight.BOLD, color="#1a202c"),
                    ft.Column(rows, spacing=15),
                ], spacing=20),
                padding=ft.padding.symmetric(vertical=20),
            )
            
        except Exception as e:
            print(f"שגיאה מפורטת בטעינת קבוצות: {e}")
            import traceback
            traceback.print_exc()
            return ft.Container(
                content=ft.Column([
                    ft.Text("קבוצות", size=24, weight=ft.FontWeight.BOLD, color="#1a202c"),
                    ft.Text(f"שגיאה בטעינת הקבוצות: {str(e)}", size=16, color="#e53e3e"),
                ], spacing=10),
                padding=ft.padding.symmetric(vertical=20),
            )


    def refresh_home_page(self):
        """Refresh home page data"""
        try:
            self.dashboard_data = get_all_dashboard_data()
            if self.current_page_index == 0:
                self.content_area.content = self.create_home_page()
                self.content_area.update()
        except Exception as e:
            print(f"שגיאה בעדכון עמוד הבית: {e}")

    def toggle_dark_mode(self, enabled: bool):
        """Toggle between light and dark mode"""
        if enabled:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.content_area.bgcolor = "#1a1a1a"
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.content_area.bgcolor = "#f8fafc"
        
        self.page.update()
    
    def navigate_to_group_page(self, group_data):
        """Navigate to group details page with tabs"""
        from pages.group_details_page import GroupDetailsPage
        group_page = GroupDetailsPage(self.page, self.handle_navigation, group_data)
        self.content_area.content = group_page.get_view()
        self.page.update()

def main(page: ft.Page):
    app = MainApp(page)


if __name__ == '__main__':
    ft.app(target=main)
