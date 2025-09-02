import flet as ft
import threading
import time

class AddGroupComponents:
    """All components for add group page"""
    
    @staticmethod
    def create_text_field(label, hint, icon, key, suffix=None, keyboard_type=None, required=False, on_change=None, on_blur=None):
        """Create a modern text field component"""
        field = ft.TextField(
            label=label,
            hint_text=hint,
            prefix_icon=icon,
            suffix_text=suffix,
            keyboard_type=keyboard_type,
            border_radius=12,
            bgcolor="#fafbfc",
            border_color="#e1e7ef",
            focused_border_color="#3b82f6",
            focused_bgcolor="#ffffff",
            label_style=ft.TextStyle(
                color="#64748b", 
                size=14,
                weight=ft.FontWeight.W_500
            ),
            text_style=ft.TextStyle(
                color="#0f172a", 
                size=16,
                weight=ft.FontWeight.W_400
            ),
            hint_style=ft.TextStyle(
                color="#94a3b8",
                size=14
            ),
            content_padding=ft.padding.symmetric(horizontal=16, vertical=14),
            cursor_color="#3b82f6",
            selection_color=ft.Colors.with_opacity(0.2, "#3b82f6"),
            on_change=lambda e: on_change(key, e.control.value) if on_change else None,
            on_blur=lambda e: on_blur(key, e.control.value) if on_blur and required else None
        )
        return field

    @staticmethod
    def create_cancel_button(on_click):
        """Create elegant cancel button"""
        return ft.Container(
            content=ft.TextButton(
                content=ft.Row([
                    ft.Icon(ft.Icons.ARROW_BACK_ROUNDED, size=18, color="#64748b"),
                    ft.Text("ביטול", color="#64748b", size=15, weight=ft.FontWeight.W_600)
                ], spacing=10, tight=True),
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=14),
                    padding=ft.padding.symmetric(horizontal=28, vertical=16),
                    bgcolor={
                        ft.ControlState.DEFAULT: "#ffffff",
                        ft.ControlState.HOVERED: "#f8fafc",
                        ft.ControlState.PRESSED: "#f1f5f9",
                    },
                    overlay_color="transparent",
                    side={
                        ft.ControlState.DEFAULT: ft.BorderSide(1, "#e2e8f0"),
                        ft.ControlState.HOVERED: ft.BorderSide(1, "#cbd5e1"),
                    }
                ),
                on_click=on_click
            ),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.04, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
        )
    
    @staticmethod
    def create_save_button(on_click):
        """Create beautiful save button"""
        return ft.Container(
            content=ft.ElevatedButton(
                content=ft.Row([
                    ft.Icon(ft.Icons.BOOKMARK_ADD_OUTLINED, size=20, color="white"),
                    ft.Text("שמור קבוצה", color="white", size=15, weight=ft.FontWeight.BOLD)
                ], spacing=12, tight=True),
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=14),
                    padding=ft.padding.symmetric(horizontal=32, vertical=18),
                    elevation={
                        ft.ControlState.DEFAULT: 3,
                        ft.ControlState.HOVERED: 6,
                        ft.ControlState.PRESSED: 1,
                    },
                    shadow_color=ft.Colors.with_opacity(0.3, "#059669"),
                    bgcolor={
                        ft.ControlState.DEFAULT: "#10b981",
                        ft.ControlState.HOVERED: "#059669",
                        ft.ControlState.PRESSED: "#047857",
                    },
                    overlay_color={
                        ft.ControlState.HOVERED: ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                        ft.ControlState.PRESSED: ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
                    }
                ),
                on_click=on_click
            ),
            animate_scale=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
        )

    @staticmethod
    def show_success_dialog(page, on_close_callback=None):
        """Show compact success dialog with auto-close - FIXED VERSION"""
        
        success_icon = ft.Container(
            content=ft.Icon(
                ft.Icons.CHECK_CIRCLE_ROUNDED,
                color="#10b981",
                size=50
            ),
            width=80,
            height=80,
            border_radius=40,
            bgcolor=ft.Colors.with_opacity(0.15, "#10b981"),
            alignment=ft.alignment.center,
            margin=ft.margin.only(bottom=20),
            animate_scale=ft.Animation(600, ft.AnimationCurve.BOUNCE_OUT)
        )
        
        dialog_content = ft.Column([
            success_icon,
            ft.Text(
                "🎉 !הקבוצה נוספה בהצלחה",
                size=18,
                weight=ft.FontWeight.BOLD,
                color="#0f172a",
                text_align=ft.TextAlign.CENTER
            ),
            ft.Container(height=8),
            ft.Text(
                "ניתן לערוך את פרטי הקבוצה בעמוד הקבוצות",
                size=14,
                weight=ft.FontWeight.BOLD,
                color="#0f172a",
                text_align=ft.TextAlign.CENTER
            ),
        ], 
        spacing=0, 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER
        )
        
        dialog = ft.AlertDialog(
            modal=True,
            content=ft.Container(
                content=dialog_content,
                width=300,
                height=200,
                padding=ft.padding.all(30),
                alignment=ft.alignment.center
            ),
            shape=ft.RoundedRectangleBorder(radius=20),
            bgcolor="#ffffff",
            elevation=15,
            shadow_color=ft.Colors.with_opacity(0.2, "#10b981"),
        )
        
        def close_dialog():
            """Function to close the dialog"""
            try:
                if hasattr(dialog, 'open') and dialog.open:
                    dialog.open = False
                    page.update()
                if on_close_callback:
                    on_close_callback()
            except Exception as e:
                print(f"Error closing dialog: {e}")
        
        def auto_close():
            """Automatically closes after 2.5 seconds"""
            time.sleep(2.5)
            close_dialog()
        
        page.open(dialog)
        page.update()
        
        threading.Thread(target=auto_close, daemon=True).start()
        
        return dialog

    @staticmethod
    def show_error_dialog(page, message, title="שגיאה"):
        """Show error dialog - COMPACT VERSION"""
        
        def close_error_dialog():
            dialog.open = False
            page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.ERROR_OUTLINE, color="#ef4444", size=32),
                    ft.Text(title, size=22, weight=ft.FontWeight.BOLD, color="#ef4444")
                ], spacing=15, alignment=ft.MainAxisAlignment.CENTER)
            ),
            content=ft.Text(
                message, 
                size=16, 
                color="#64748b", 
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.W_400
            ),
            actions=[
                ft.ElevatedButton(
                    "הבנתי",
                    on_click=lambda e: close_error_dialog(),
                    style=ft.ButtonStyle(
                        bgcolor="#ef4444",
                        color="white",
                        text_style=ft.TextStyle(weight=ft.FontWeight.BOLD, size=16),
                        shape=ft.RoundedRectangleBorder(radius=12),
                        padding=ft.padding.symmetric(horizontal=30, vertical=10)
                    )
                )
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            shape=ft.RoundedRectangleBorder(radius=20),
            bgcolor="#ffffff",
            elevation=12,
            shadow_color=ft.Colors.with_opacity(0.2, "#ef4444")
        )
        
        page.open(dialog)
        page.update()
        return dialog
    
    @staticmethod
    def show_confirmation_dialog(page, title, message, on_confirm, on_cancel=None):
        
        def handle_confirm():
            dialog.open = False
            page.update()
            if on_confirm:
                on_confirm()
        
        def handle_cancel():
            dialog.open = False
            page.update()
            if on_cancel:
                on_cancel()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.HELP_OUTLINE, color="#f59e0b", size=28),
                    ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color="#0f172a")
                ], spacing=12, alignment=ft.MainAxisAlignment.CENTER),
                padding=ft.padding.only(bottom=10)
            ),
            content=ft.Container(
                content=ft.Text(
                    message, 
                    size=16, 
                    color="#64748b", 
                    text_align=ft.TextAlign.CENTER
                ),
                width=350,
                padding=ft.padding.all(20),
                alignment=ft.alignment.center
            ),
            actions=[
                ft.Row([
                    ft.Container(
                        content=ft.TextButton(
                            "ביטול",
                            on_click=lambda e: handle_cancel(),
                            style=ft.ButtonStyle(
                                color="#64748b",
                                text_style=ft.TextStyle(weight=ft.FontWeight.W_500, size=16),
                                shape=ft.RoundedRectangleBorder(radius=10),
                                padding=ft.padding.symmetric(horizontal=25, vertical=12)
                            )
                        ),
                        expand=1
                    ),
                    ft.Container(width=10),
                    ft.Container(
                        content=ft.ElevatedButton(
                            "אישור",
                            on_click=lambda e: handle_confirm(),
                            style=ft.ButtonStyle(
                                bgcolor="#10b981",
                                color="white",
                                text_style=ft.TextStyle(weight=ft.FontWeight.BOLD, size=16),
                                shape=ft.RoundedRectangleBorder(radius=10),
                                padding=ft.padding.symmetric(horizontal=25, vertical=12)
                            )
                        ),
                        expand=1
                    )
                ], spacing=0, alignment=ft.MainAxisAlignment.SPACE_EVENLY)
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            shape=ft.RoundedRectangleBorder(radius=16),
            bgcolor="#ffffff",
            elevation=10
        )
        
        page.open(dialog)
        page.update()
        return dialog