import flet as ft
from components.stats_cards import StatsCards
from components.students_table import StudentsTable
from components.no_results_dialog import NoResultsDialog


class StudentsListView:
    """Main view for students list page"""
    
    def __init__(self, parent):
        self.parent = parent
        self.page = parent.page
        self.data_manager = parent.data_manager
        
        self.students_table = StudentsTable()
        self.search_field = None  
        self.stats_container = None 
        self.table_container = None  
        
        self.current_students = []
        self.filtered_students = []
        
    def create_header(self) -> ft.Container:
        """Create page header"""
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.PEOPLE, size=32, color=ft.Colors.BLUE_600),
                    ft.Text(
                        "תלמידות",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_GREY_800,
                        rtl=True
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=12),
                ft.Container(height=8),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.symmetric(vertical=32),
            bgcolor=ft.Colors.with_opacity(0.02, ft.Colors.BLUE_600),
            border_radius=16,
            margin=ft.margin.only(bottom=20)
        )
    
    def create_search_section(self) -> ft.Container:
        """Create search section"""
        self.search_field = ft.TextField(
            hint_text="חיפוש לפי שם, קבוצה, טלפון או כל פרט אחר...",
            hint_style=ft.TextStyle(color=ft.Colors.GREY_400),
            text_size=14,
            height=50,
            border_color=ft.Colors.GREY_300,
            border_width=1,
            border_radius=8,
            filled=True,
            fill_color=ft.Colors.WHITE,
            on_change=self.filter_students,
            rtl=True,
            text_align=ft.TextAlign.RIGHT,
            prefix_icon=ft.Icons.SEARCH,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12)
        )
        
        search_container = ft.Container(
            content=self.search_field,
            width=600,
            margin=ft.margin.only(bottom=16),
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=search_container,
                    alignment=ft.alignment.center
                ),
                ft.Row([
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.REFRESH, size=18, color=ft.Colors.WHITE),
                            ft.Text("רענן", size=14, color=ft.Colors.WHITE)
                        ], spacing=8, tight=True),
                        bgcolor=ft.Colors.BLUE_600,
                        on_click=self.refresh_data,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.padding.symmetric(horizontal=20, vertical=12)
                        )
                    ),
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.CLEAR_ALL, size=18, color=ft.Colors.GREY_700),
                            ft.Text("נקה חיפוש", size=14, color=ft.Colors.GREY_700)
                        ], spacing=8, tight=True),
                        bgcolor=ft.Colors.GREY_100,
                        on_click=self.clear_search,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.padding.symmetric(horizontal=20, vertical=12)
                        )
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=16)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            margin=ft.margin.only(bottom=24)
        )
    
    def create_stats_section(self) -> ft.Container:
        """Create statistics section"""
        stats = self.data_manager.get_students_stats(self.filtered_students)
        
        self.stats_container = ft.Container(
            content=StatsCards.create_stats_row(stats),
            margin=ft.margin.only(bottom=32)
        )
        
        return self.stats_container
    
    def create_table_section(self) -> ft.Container:
        """Create table section"""
        if not self.filtered_students:
            self.table_container = self.create_empty_state()
        else:
            self.students_table.update(self.filtered_students)
            self.table_container = self.students_table.get_container()
        
        return self.table_container
    
    def create_empty_state(self) -> ft.Container:
        """Create empty state when no students"""
        return ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.PEOPLE_OUTLINE, size=64, color=ft.Colors.GREY_400),
                ft.Container(height=16),
                ft.Text(
                    "אין תלמידות להצגה",
                    size=20,
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER,
                    rtl=True
                ),
                ft.Container(height=8),
                ft.Text(
                    "נסה לרענן את הנתונים או לנקות את החיפוש",
                    size=14,
                    color=ft.Colors.GREY_500,
                    text_align=ft.TextAlign.CENTER,
                    rtl=True
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.all(64),
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            border=ft.border.all(1, ft.Colors.with_opacity(0.1, ft.Colors.GREY_400))
        )
    
    def filter_students(self, e):
        """Filter students based on search query"""
        query = e.control.value.strip() if e and e.control and e.control.value else ""
        
        if not query:
            self.filtered_students = self.current_students.copy()
        else:
            self.filtered_students = self.data_manager.filter_students(self.current_students, query)
            
            if not self.filtered_students:
                NoResultsDialog.show(self.page)
        
        self.update_components()
    
    def refresh_data(self, e=None):
        """Refresh students data"""
        self.load_data()
        self.update_components()
        
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("הנתונים רוענו בהצלחה", rtl=True),
            bgcolor=ft.Colors.GREEN_600
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def clear_search(self, e=None):
        """Clear search and show all students"""
        if self.search_field:
            self.search_field.value = ""
            self.search_field.update()
        
        self.filtered_students = self.current_students.copy()
        self.update_components()
    
    def update_components(self):
        """Update only the dynamic components without rebuilding everything"""
        if self.stats_container:
            stats = self.data_manager.get_students_stats(self.filtered_students)
            self.stats_container.content = StatsCards.create_stats_row(stats)
            self.stats_container.update()
        
        if self.table_container:
            for i, control in enumerate(self.parent.layout.controls):
                if control == self.table_container:
                    new_table = self.create_table_section()
                    self.parent.layout.controls[i] = new_table
                    self.table_container = new_table
                    break
        
        self.page.update()
    
    def load_data(self):
        """Load students data"""
        self.current_students = self.data_manager.load_students()
        self.filtered_students = self.current_students.copy()
    
    def render(self):
        """Render the complete view"""
        self.parent.layout.controls.extend([
            self.create_header(),
            self.create_search_section(),
            self.create_stats_section(),
            self.create_table_section()
        ])
