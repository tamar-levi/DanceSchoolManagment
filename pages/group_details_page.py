import flet as ft
from typing import Callable, Dict, Any
from pages.students_page import StudentsPage
from pages.group_attendance_page import GroupAttendancePage

class GroupDetailsPage:
    def __init__(self, page: ft.Page, navigation_callback: Callable, group_data: Dict[str, Any]):
        self.page = page
        self.navigation_callback = navigation_callback
        self.group_data = group_data
        self.current_tab = 0
        
        group_name = group_data.get('name', 'קבוצה')
        self.students_page = StudentsPage(self.page, self.handle_students_navigation, group_name, came_from_home=True)
        self.attendance_page = GroupAttendancePage(self.page, self.handle_attendance_navigation, group_data)
        
    def handle_students_navigation(self, page_instance=None, page_index=None):
        """Handle navigation from students page"""
        if page_instance is not None:
            self.navigation_callback(page_instance)
        elif page_index is not None:
            if page_index == 1:  
                return  
            else:
                self.navigation_callback(None, page_index)
        else:
            return
    
    def handle_attendance_navigation(self, page_instance=None, page_index=None):
        """Handle navigation from attendance page"""
        if page_instance is not None:
            self.navigation_callback(page_instance)
        elif page_index is not None:
            if page_index == 0:  
                self.navigation_callback(None, 0)
            else:
                self.navigation_callback(None, page_index)
        else:
            return
        
    def back_to_home(self, page_instance=None, page_index=None):
        """Return to home page"""
        self.navigation_callback(None, 0)
        
    def get_view(self):
        """Get the main view of the group details page"""
        return ft.Container(
            content=ft.Column([
                self.create_header(),
                self.create_tabs(),
            ], spacing=0, expand=True),
            expand=True,
            bgcolor="#f8fafc",
        )
    
    def create_header(self):
        """Create the page header"""
        def go_back(e):
            self.navigation_callback(None, 0) 
            
        return ft.Container(
            content=ft.Row([
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=go_back,
                    tooltip="חזרה לעמוד הבית",
                    icon_color="#4299e1",
                    icon_size=24,
                ),
                ft.Column([
                    ft.Text(
                        self.group_data.get('name', 'קבוצה'),
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color="#1a202c",
                        rtl=True
                    ),
                    ft.Text(
                        f"מורה: {self.group_data.get('teacher', 'לא צוין')}",
                        size=14,
                        color="#718096",
                        rtl=True
                    ),
                ], spacing=5, expand=True),
            ], alignment=ft.MainAxisAlignment.START),
            padding=ft.padding.all(24),
            bgcolor="#ffffff",
        )
    
    def create_tabs(self):
        """Create the tabs using existing pages"""
        def on_tab_change(e):
            self.current_tab = e.control.selected_index
            self.page.update()
            
        tabs = ft.Tabs(
            selected_index=self.current_tab,
            on_change=on_tab_change,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="תלמידות הקבוצה",
                    icon=ft.Icons.PEOPLE,
                    content=ft.Container(
                        content=self.students_page.get_view(),
                        expand=True,
                    )
                ),
                ft.Tab(
                    text="נוכחות הקבוצה", 
                    icon=ft.Icons.CHECK_CIRCLE,
                    content=ft.Container(
                        content=self.attendance_page.get_view(),
                        expand=True,
                    )
                ),
            ],
            expand=True,
            tab_alignment=ft.TabAlignment.CENTER,
        )
        
        return ft.Container(
            content=tabs,
            expand=True,
            bgcolor="#ffffff",
        )
