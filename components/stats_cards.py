import flet as ft

class StatsCards:
    """Statistics cards component"""
    
    @staticmethod
    def create_card(title: str, value: str, icon: str, color: str) -> ft.Container:
        """Create a statistics card"""
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(icon, size=24, color=color),
                    ft.Text(value, size=28, weight=ft.FontWeight.BOLD, color=color)
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                ft.Text(title, size=12, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER, rtl=True)
            ], spacing=8, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=160,
            height=100,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=ft.padding.all(16),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 2)
            ),
            border=ft.border.all(1, ft.Colors.with_opacity(0.1, ft.Colors.GREY_400))
        )
    
    @staticmethod
    def create_stats_row(stats: dict) -> ft.Row:
        """Create row of statistics cards"""
        return ft.Row([
            StatsCards.create_card(
                "סה״כ תלמידות", 
                str(stats["total"]), 
                ft.Icons.PEOPLE, 
                ft.Colors.BLUE_600
            ),
            StatsCards.create_card(
                "שילמו", 
                str(stats["paid"]), 
                ft.Icons.CHECK_CIRCLE, 
                ft.Colors.GREEN_600
            ),
            StatsCards.create_card(
                "לא שילמו", 
                str(stats["unpaid"]), 
                ft.Icons.PENDING, 
                ft.Colors.ORANGE_600
            ),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
