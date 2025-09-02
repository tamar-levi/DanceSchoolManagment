import json
import flet as ft
from typing import Dict, Any
from pages.group_attendance_page import GroupAttendancePage
from utils.manage_json import ManageJSON

def load_groups():
    """Load groups from JSON file"""
    try:
        data_dir = ManageJSON.get_appdata_path() / "data"
        groups_file = data_dir / "groups.json"
        
        with open(groups_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("groups", [])
    except Exception as e:
        print("Error on Load groups", e)
        return []

class AttendancePage:
    def __init__(self, page: ft.Page, navigation_handler=None):
        self.page = page
        self.navigation_handler = navigation_handler
        self.groups = []
        
        self.refresh_data()

    def refresh_data(self):
        """Refresh groups data"""
        self.groups = load_groups()

    def create_clean_card(self, content, bgcolor=ft.Colors.WHITE, padding=20):
        """Create a clean, simple card container"""
        return ft.Container(
            content=content,
            bgcolor=bgcolor,
            border_radius=12,
            padding=ft.padding.all(padding),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 4),
            ),
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
        )

    def create_header_card(self):
        """Create the header card with title and subtitle - fully centered"""
        header_content = ft.Column([
            ft.Container(
                content=ft.Icon(ft.Icons.GROUPS, size=48, color=ft.Colors.BLUE_600),
                margin=ft.margin.only(bottom=15),
                alignment=ft.alignment.center,
            ),
            ft.Text(
                "ניהול נוכחות",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_GREY_800,
                text_align=ft.TextAlign.CENTER,
                rtl=True
            ),
            ft.Text(
                "בחר קבוצה לניהול נוכחות",
                size=16,
                color=ft.Colors.GREY_600,
                text_align=ft.TextAlign.CENTER,
                rtl=True
            ),
        ], 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=8
        )
        
        return ft.Container(
            content=header_content,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=15,
            padding=ft.padding.all(30),
            margin=ft.margin.only(bottom=25),
            alignment=ft.alignment.center,
            width=float('inf'), 
        )

    def show_group_attendance(self, group):
        """Show attendance table page for selected group"""
        attendance_page = GroupAttendancePage(self.page, self.navigation_handler, group)
        self.navigation_handler(attendance_page, None)

    def create_group_button(self, group: Dict[str, Any], index: int):
        """Create a clean group button with full width"""
        def on_group_click(e):
            self.show_group_attendance(group)

        def on_hover(e):
            if e.data == "true":
                e.control.bgcolor = ft.Colors.BLUE_50
                e.control.shadow = ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=20,
                    color=ft.Colors.with_opacity(0.15, ft.Colors.BLUE_400),
                    offset=ft.Offset(0, 6),
                )
            else:
                e.control.bgcolor = ft.Colors.WHITE
                e.control.shadow = ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=10,
                    color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                    offset=ft.Offset(0, 3),
                )
            e.control.update()

        group_info = []
        if group.get("description"):
            group_info.append(
                ft.Text(
                    group["description"],
                    size=13,
                    color=ft.Colors.GREY_500,
                    text_align=ft.TextAlign.CENTER,
                    rtl=True,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS,
                )
            )

        members_count = len(group.get("members", []))
        if members_count > 0:
            group_info.append(
                ft.Container(
                    content=ft.Text(
                        f"👥 {members_count} חברים",
                        size=12,
                        color=ft.Colors.GREEN_600,
                        rtl=True
                    ),
                    margin=ft.margin.only(top=8),
                )
            )

        button_content = ft.Column([
            ft.Container(
                content=ft.Icon(ft.Icons.GROUP, size=32, color=ft.Colors.BLUE_500),
                margin=ft.margin.only(bottom=12),
            ),
            ft.Text(
                group.get("name", ""),
                size=18,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_GREY_800,
                text_align=ft.TextAlign.CENTER,
                rtl=True,
                max_lines=2,
                overflow=ft.TextOverflow.ELLIPSIS,
            ),
            *group_info,
            ft.Container(
                content=ft.Text(
                    "לחץ לניהול נוכחות ←",
                    size=12,
                    color=ft.Colors.BLUE_600,
                    rtl=True
                ),
                margin=ft.margin.only(top=12),
            )
        ], 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=6
        )

        return ft.Container(
            content=button_content,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=ft.padding.all(20),
            margin=ft.margin.symmetric(vertical=8),
            on_click=on_group_click,
            on_hover=on_hover,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                offset=ft.Offset(0, 3),
            ),
            ink=True,
            width=float('inf'),  
        )

    def create_groups_grid(self):
        """Create responsive grid layout for groups"""
        if not self.groups:
            return None
            
        rows = []
        for i in range(0, len(self.groups), 3):
            group_batch = self.groups[i:i+3]
            row_controls = []
            
            for group in group_batch:
                group_button = self.create_group_button(group, i)
                row_controls.append(
                    ft.Container(
                        content=group_button,
                        expand=True,
                        padding=ft.padding.symmetric(horizontal=5),
                    )
                )
            
            while len(row_controls) < 3:
                row_controls.append(ft.Container(expand=True))
            
            rows.append(
                ft.Row(
                    controls=row_controls,
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )
        
        return ft.Column(
            controls=rows,
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def create_groups_card(self):
        """Create groups selection card with responsive grid layout"""
        if not self.groups:
            def refresh_groups(e):
                self.refresh_data()
                self.build_content()

            empty_content = ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.GROUP_OFF, size=64, color=ft.Colors.GREY_400),
                    ft.Text(
                        "אין קבוצות זמינות",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREY_600,
                        text_align=ft.TextAlign.CENTER,
                        rtl=True
                    ),
                    ft.Text(
                        "הוסף קבוצות כדי להתחיל לנהל נוכחות",
                        size=14,
                        color=ft.Colors.GREY_500,
                        text_align=ft.TextAlign.CENTER,
                        rtl=True
                    ),
                    ft.Container(
                        content=ft.ElevatedButton(
                            text="🔄 רענן רשימת קבוצות",
                            on_click=refresh_groups,
                            bgcolor=ft.Colors.BLUE_600,
                            color=ft.Colors.WHITE,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                                padding=ft.padding.symmetric(horizontal=20, vertical=12),
                            ),
                        ),
                        margin=ft.margin.only(top=20),
                    )
                ], 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
                ),
                padding=ft.padding.all(40),
                alignment=ft.alignment.center,
            )
            return self.create_clean_card(empty_content)

        groups_header = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.LIST, size=24, color=ft.Colors.BLUE_600),
                ft.Text(
                    f"קבוצות זמינות ({len(self.groups)})",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_GREY_800,
                    rtl=True
                )
            ], 
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
            ),
            margin=ft.margin.only(bottom=20),
            alignment=ft.alignment.center,
        )

        groups_grid = self.create_groups_grid()

        groups_content = ft.Column([
            groups_header,
            ft.Container(
                content=groups_grid,
                padding=ft.padding.all(10),
            )
        ], 
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        return self.create_clean_card(groups_content, padding=25)

    def go_home(self, e):
        """Navigate back to home page"""
        if self.navigation_handler:
            self.navigation_handler(None, 0)

    def create_navigation_card(self):
        """Create the navigation card with back button"""
        back_button = ft.ElevatedButton(
            text="חזרה לעמוד הראשי",
            on_click=self.go_home,
            icon=ft.Icons.HOME,
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=ft.padding.symmetric(horizontal=25, vertical=15),
            ),
            height=50,
        )

        nav_content = ft.Container(
            content=back_button,
            alignment=ft.alignment.center,
        )

        return ft.Container(
            content=nav_content,
            margin=ft.margin.only(top=25),
            alignment=ft.alignment.center,
        )

    def build_content(self):
        """Build and update the main content"""
        if hasattr(self, '_main_content'):
            main_content_column = self._create_main_content()
            self._main_content.content = main_content_column
            self.page.update()

    def _create_main_content(self):
        """Create the main content structure with proper expand settings"""
        return ft.Column([
            self.create_header_card(),
            ft.Container(
                content=self.create_groups_card(),
                expand=True,
            ),
            self.create_navigation_card(),
        ], 
        spacing=0,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO, 
        )


    def get_view(self):
        """Get the main view of the attendance page"""
        main_content_column = self._create_main_content()

        self._main_content = ft.Container(
            content=ft.Column([
                main_content_column
            ], 
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            ),
            padding=ft.padding.all(25),
            bgcolor=ft.Colors.GREY_50,
            expand=True,
        )

        return self._main_content
