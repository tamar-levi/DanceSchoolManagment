import flet as ft

class CleanButton:
    """Clean, minimal button factory"""
    
    @staticmethod
    def create(text, icon, color, on_click, variant="filled"):
        """Create clean, minimal buttons"""
        if variant == "filled":
            return ft.Container(
                content=ft.Row([
                    ft.Icon(icon, size=16, color=ft.Colors.WHITE),
                    ft.Text(text, size=14, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE)
                ], spacing=8, tight=True, alignment=ft.MainAxisAlignment.CENTER),
                bgcolor=color,
                border_radius=8,
                padding=ft.padding.symmetric(horizontal=16, vertical=10),
                animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
                on_click=on_click,
                ink=True
            )
        else:  
            return ft.Container(
                content=ft.Row([
                    ft.Icon(icon, size=16, color=color),
                    ft.Text(text, size=14, weight=ft.FontWeight.W_500, color=color)
                ], spacing=8, tight=True, alignment=ft.MainAxisAlignment.CENTER),
                bgcolor=ft.Colors.TRANSPARENT,
                border=ft.border.all(1, color),
                border_radius=8,
                padding=ft.padding.symmetric(horizontal=16, vertical=10),
                animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
                on_click=on_click,
                ink=True
            )

    @staticmethod
    def create_icon_button(icon, color, tooltip, on_click, bg_color=None):
        """Create clean icon button"""
        return ft.IconButton(
            icon=icon,
            icon_size=16,
            icon_color=color,
            bgcolor=bg_color or ft.Colors.GREY_100,
            tooltip=tooltip,
            on_click=on_click,
            style=ft.ButtonStyle(
                shape=ft.CircleBorder(),
                padding=ft.padding.all(8)
            )
        )