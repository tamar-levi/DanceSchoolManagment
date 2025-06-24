import flet as ft
from datetime import datetime


class FormFields:
    """Factory for creating form fields"""
    
    @staticmethod
    def create_text_field(label, hint_text, icon, keyboard_type=None):
        """Create a styled text field"""
        return ft.TextField(
            label=label,
            hint_text=hint_text,
            prefix_icon=icon,
            border_radius=12,
            bgcolor=ft.Colors.WHITE,
            border_color=ft.Colors.GREY_300,
            focused_border_color=ft.Colors.GREEN_600,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=16),
            keyboard_type=keyboard_type,
            text_align=ft.TextAlign.RIGHT
        )

    @staticmethod
    def create_dropdown(label, icon, options, default_value=None):
        """Create a styled dropdown"""
        dropdown_options = [ft.dropdown.Option(option) for option in options]
        
        return ft.Dropdown(
            label=label,
            prefix_icon=icon,
            border_radius=12,
            bgcolor=ft.Colors.WHITE,
            border_color=ft.Colors.GREY_300,
            focused_border_color=ft.Colors.GREEN_600,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=16),
            options=dropdown_options,
            value=default_value
        )

    @staticmethod
    def create_date_field(label, icon, default_to_today=True):
        """Create a date field"""
        value = datetime.now().strftime("%d/%m/%Y") if default_to_today else ""
        
        return ft.TextField(
            label=label,
            hint_text="dd/mm/yyyy",
            prefix_icon=icon,
            border_radius=12,
            bgcolor=ft.Colors.WHITE,
            border_color=ft.Colors.GREY_300,
            focused_border_color=ft.Colors.GREEN_600,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=16),
            value=value,
            text_align=ft.TextAlign.RIGHT
        )
