import flet as ft


class SearchBar:
    """Search bar component"""
    
    @staticmethod
    def create(on_change_callback, placeholder: str = "חיפוש...") -> ft.Container:
        """Create search input field"""
        search_input = ft.TextField(
            hint_text=placeholder,
            hint_style=ft.TextStyle(color=ft.Colors.GREY_400),
            text_size=14,
            height=50,
            border_color=ft.Colors.GREY_300,
            focused_border_color=ft.Colors.GREY_500,
            border_width=1,
            border_radius=8,
            filled=True,
            fill_color=ft.Colors.WHITE,
            on_change=on_change_callback,
            rtl=True,
            text_align=ft.TextAlign.RIGHT,
            prefix_icon=ft.Icons.SEARCH,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12)
        )
        
        return ft.Container(
            content=search_input,
            width=600,
            margin=ft.margin.only(bottom=24),
        )
