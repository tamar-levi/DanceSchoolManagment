import flet as ft


class ModernCard(ft.Container):
    """Modern card component with hover effects"""
    
    def __init__(self, content=None, hover_effect=True, **kwargs):
        super().__init__(
            content=content,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT) if hover_effect else None,
            **kwargs
        )
        
        if hover_effect:
            self.on_hover = self._handle_hover

    def _handle_hover(self, e):
        """Handle hover effect"""
        if e.data == "true":
            self.shadow = ft.BoxShadow(
                spread_radius=0,
                blur_radius=12,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 4),
            )
        else:
            self.shadow = ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            )
        self.update()