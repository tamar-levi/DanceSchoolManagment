import flet as ft


class ModernDialog:
    """Modern dialog component for various use cases"""
    
    def __init__(self, page):
        self.page = page

    def show_success(self, message, callback=None):
        """Show success dialog"""
        self._show_dialog(
            "הצלחה",
            message,
            ft.Icons.CHECK_CIRCLE,
            ft.Colors.GREEN_600,
            callback
        )

    def show_error(self, message, callback=None):
        """Show error dialog"""
        self._show_dialog(
            "שגיאה",
            message,
            ft.Icons.ERROR,
            ft.Colors.RED_600,
            callback
        )

    def show_confirmation(self, message, subtitle, on_confirm):
        """Show confirmation dialog"""
        def handle_yes(e):
            self.page.close(dialog)
            if on_confirm:
                on_confirm()
            
        def handle_no(e):
            self.page.close(dialog)
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                "אישור פעולה", 
                size=18, 
                weight=ft.FontWeight.W_600,
                text_align=ft.TextAlign.RIGHT
            ),
            content=ft.Column([
                ft.Text(
                    message, 
                    size=14, 
                    color=ft.Colors.GREY_700,
                    text_align=ft.TextAlign.RIGHT,
                    rtl=True  # הוספת RTL
                ),
                ft.Text(
                    subtitle, 
                    size=12, 
                    color=ft.Colors.GREY_700,  # שינוי מאדום לשחור
                    text_align=ft.TextAlign.RIGHT,
                    rtl=True  # הוספת RTL
                )
            ], 
            spacing=4, 
            tight=True, 
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.END  # יישור אופקי לימין
            ),
            actions=[
                ft.TextButton("ביטול", on_click=handle_no),
                ft.FilledButton(
                    "אישור", 
                    on_click=handle_yes, 
                    style=ft.ButtonStyle(bgcolor=ft.Colors.RED_600)
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            content_padding=ft.padding.only(left=24, right=24, top=20, bottom=30),
        )
        
        self.page.open(dialog)

    def _show_dialog(self, title, message, icon, color, callback=None):
        """Show styled dialog"""
        def close_dialog(e):
            self.page.close(dialog)
            if callback:
                callback()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(icon, color=color, size=24),
                ft.Text(
                    title, 
                    size=20, 
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.RIGHT
                )
            ], spacing=12, alignment=ft.MainAxisAlignment.END),
            content=ft.Text(
                message, 
                size=16, 
                color=ft.Colors.GREY_700,
                text_align=ft.TextAlign.RIGHT,
                rtl=True  
            ),
            actions=[
                ft.ElevatedButton(
                    "אישור",
                    on_click=close_dialog,
                    bgcolor=color,
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(
                        padding=ft.padding.symmetric(horizontal=24, vertical=12),
                        shape=ft.RoundedRectangleBorder(radius=8)
                    )
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            shape=ft.RoundedRectangleBorder(radius=16)
        )
        
        self.page.open(dialog)
