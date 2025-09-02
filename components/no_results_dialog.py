import flet as ft

class NoResultsDialog:
    """No results dialog component"""
    
    @staticmethod
    def show(page: ft.Page):
        """Show no results dialog"""
        def close_dialog(e):
            dialog.open = False
            page.update()

        dialog = ft.AlertDialog(
            modal=True,
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.SEARCH_OFF, size=24, color=ft.Colors.ORANGE_600),
                        ft.Text("אין תוצאות", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_800)
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                    
                    ft.Container(height=16), 
                    
                    ft.Text(
                        "לא נמצאה אף תלמידה התואמת לדרישות החיפוש",
                        size=16,
                        color=ft.Colors.BLUE_GREY_600,
                        text_align=ft.TextAlign.CENTER,
                        rtl=True
                    ),
                    ft.Container(height=8),
                    ft.Text(
                        "נסה לחפש במילים אחרות או לבדוק את האיות",
                        size=14,
                        color=ft.Colors.GREY_500,
                        text_align=ft.TextAlign.CENTER,
                        rtl=True
                    ),
                    
                    ft.Container(height=20), 
                    
                    ft.ElevatedButton(
                        "הבנתי",
                        on_click=close_dialog,
                        bgcolor=ft.Colors.BLUE_600,
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.padding.symmetric(horizontal=20, vertical=12)
                        )
                    )
                ], 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
                tight=True 
                ),
                padding=ft.padding.all(20),  
                width=300 
            ),
            shape=ft.RoundedRectangleBorder(radius=16),
            bgcolor=ft.Colors.WHITE,
            content_padding=ft.padding.all(0)  
        )

        page.open(dialog)
        page.update()


class NoResultsDialogAlternative:
    """No results dialog component - פתרון חלופי"""
    
    @staticmethod
    def show(page: ft.Page):
        """Show no results dialog"""
        def close_dialog(e):
            dialog.open = False
            page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.SEARCH_OFF, size=24, color=ft.Colors.ORANGE_600),
                ft.Text("אין תוצאות", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_800)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        "לא נמצאה אף תלמידה התואמת לדרישות החיפוש",
                        size=16,
                        color=ft.Colors.BLUE_GREY_600,
                        text_align=ft.TextAlign.CENTER,
                        rtl=True
                    ),
                    ft.Container(height=8),
                    ft.Text(
                        "נסה לחפש במילים אחרות או לבדוק את האיות",
                        size=14,
                        color=ft.Colors.GREY_500,
                        text_align=ft.TextAlign.CENTER,
                        rtl=True
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.symmetric(vertical=8),
                margin=ft.margin.only(bottom=-10)
            ),
            actions=[
                ft.ElevatedButton(
                    "הבנתי",
                    on_click=close_dialog,
                    bgcolor=ft.Colors.BLUE_600,
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=ft.padding.symmetric(horizontal=12, vertical=12)
                    )
                )
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            shape=ft.RoundedRectangleBorder(radius=16),
            bgcolor=ft.Colors.WHITE,
            content_padding=ft.padding.all(16),
            actions_padding=ft.padding.only(bottom=16, left=16, right=16, top=0)
        )

        page.open(dialog)
        page.update()