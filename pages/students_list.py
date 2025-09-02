import flet as ft
from utils.students_data_manager import StudentsDataManager
from views.students_list_view import StudentsListView

class StudentsListPage:
    """Main students list page controller"""
    
    def __init__(self, page: ft.Page, navigation_callback=None):
        self.page = page
        self.navigation_callback = navigation_callback
        
        self.data_manager = StudentsDataManager()
        
        self.layout = ft.Column(
            controls=[],
            spacing=0,
            expand=True,
            scroll=ft.ScrollMode.AUTO
        )
        
        self.view = StudentsListView(self)
        
        self.initialize()
    
    def initialize(self):
        """Initialize the page"""
        self.view.load_data()
        self.view.render()
    
    def get_view(self) -> ft.Container:
        """Get the main page view"""
        return ft.Container(
            content=self.layout,
            padding=ft.padding.all(24),
            expand=True,
            bgcolor=ft.Colors.with_opacity(0.02, ft.Colors.BLUE_GREY_900)
        )
