import json
import os
import flet as ft
from typing import Dict, Any
from utils.attendance_utils import AttendanceUtils

class AttendanceTableView:
    def __init__(self, page: ft.Page, navigation_handler=None, group: Dict[str, Any] = None, parent_page=None):
        self.page = page
        self.navigation_handler = navigation_handler
        self.group = group or {}
        self.parent_page = parent_page  
        self.attendance_data = {}
        self.students = []
        self.table_container = None 
        
        # Load data
        self.load_data()

    def load_data(self):
        """Load attendance and student data"""
        self.attendance_data = AttendanceUtils.load_attendance_file(self.group.get('id', ''))
        
        try:
            if os.path.exists("data/students.json"):
                with open("data/students.json", "r", encoding="utf-8") as f:
                    students_data = json.load(f)
                    self.students = []
                    for s in students_data.get("students", []):
                        student_groups = s.get("groups", [])
                        if self.group.get("name", "").strip() in student_groups:
                            self.students.append({"id": s["id"], "name": s["name"]})
        except Exception as e:
            print(f"Error loading students: {e}")

    def save_attendance(self):
        """Save attendance data"""
        try:
            AttendanceUtils.save_attendance_file(self.group.get('id', ''), self.attendance_data)
        except Exception as e:
            print(f"Error saving attendance: {e}")

    def get_table_only(self):
        """Get only the table component - for embedding in other pages"""
        table = self.create_modern_data_table()
        
        self.table_container = ft.Container(
            content=table.content if hasattr(table, 'content') else table,
            bgcolor=getattr(table, 'bgcolor', ft.Colors.WHITE),
            border_radius=getattr(table, 'border_radius', 16),
            border=getattr(table, 'border', ft.border.all(1, ft.Colors.GREY_200)),
            padding=getattr(table, 'padding', ft.padding.all(0)),
            shadow=getattr(table, 'shadow', None),
        )
        
        return self.table_container

    def create_modern_data_table(self):
        """Create modern React-style table with clean design and horizontal scroll"""
        dates = list(self.attendance_data.keys())
        
        if not dates or not self.students:
            return self.create_empty_table_state()
        
        header_row = self.create_table_header()
        
        table_rows = []
        for date in sorted(dates, reverse=True):
            table_rows.append(self.create_table_row(date))
        
        table_content = ft.Column([
            header_row,
            ft.Container(height=1, bgcolor=ft.Colors.GREY_200),  
            ft.Column(table_rows, spacing=0),
        ], spacing=0)
        
        return ft.Container(
            content=ft.Row([
                table_content
            ], scroll=ft.ScrollMode.AUTO), 
            bgcolor=ft.Colors.WHITE,
            border_radius=16,
            border=ft.border.all(1, ft.Colors.GREY_200),
            padding=ft.padding.all(0),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                offset=ft.Offset(0, 4),
            ),
        )

    def create_table_header(self):
        """Create React-style table header with fixed widths"""
        header_cells = [
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.CALENDAR_TODAY, size=16, color=ft.Colors.GREY_600),
                    ft.Container(width=8),
                    ft.Text(
                        "תאריך", 
                        size=14, 
                        weight=ft.FontWeight.W_600, 
                        color=ft.Colors.GREY_700,
                        rtl=True
                    ),
                ], alignment=ft.MainAxisAlignment.START),
                width=160,  
                padding=ft.padding.symmetric(horizontal=16, vertical=16),
            )
        ]
        
        for student in self.students:
            header_cells.append(
                ft.Container(
                    content=ft.Text(
                        student["name"],
                        size=14,
                        weight=ft.FontWeight.W_600,
                        color=ft.Colors.GREY_700,
                        text_align=ft.TextAlign.CENTER,
                        rtl=True,
                        overflow=ft.TextOverflow.ELLIPSIS, 
                    ),
                    width=140,  
                    padding=ft.padding.symmetric(horizontal=12, vertical=16),
                    alignment=ft.alignment.center,
                    tooltip=student["name"],  
                )
            )
        
        return ft.Container(
            content=ft.Row(header_cells, spacing=0),
            bgcolor=ft.Colors.GREY_50,
            border_radius=ft.border_radius.only(top_left=16, top_right=16),
        )

    def create_table_row(self, date: str):
        """Create React-style table row with fixed widths"""
        row_cells = [
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.EDIT_OUTLINED, size=14, color=ft.Colors.BLUE_400),
                    ft.Container(width=8),
                    ft.Text(
                        date, 
                        size=14, 
                        color=ft.Colors.GREY_700,
                        weight=ft.FontWeight.W_500
                    ),
                ], alignment=ft.MainAxisAlignment.START),
                width=160,  
                padding=ft.padding.symmetric(horizontal=16, vertical=12),
                on_click=lambda e, d=date: self.show_date_options(d),
                ink=True,
                border_radius=8,
                tooltip="לחץ לעריכה",
            )
        ]
        
        for student in self.students:
            is_present = self.attendance_data.get(date, {}).get(str(student["id"]), False)
            row_cells.append(
                ft.Container(
                    content=self.create_status_toggle(is_present, date, student["id"]),
                    width=140,  
                    padding=ft.padding.symmetric(horizontal=12, vertical=12),
                    alignment=ft.alignment.center,
                )
            )
        
        return ft.Container(
            content=ft.Row(row_cells, spacing=0),
            bgcolor=ft.Colors.WHITE,
            border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.GREY_100)),
            on_hover=self.on_row_hover,
        )

    def on_row_hover(self, e):
        """Handle row hover effect"""
        if e.data == "true":
            e.control.bgcolor = ft.Colors.GREY_50
        else:
            e.control.bgcolor = ft.Colors.WHITE
        e.control.update()

    def create_status_toggle(self, is_present: bool, date: str, student_id: str):
        """Create clean icon-only status toggle button"""
        def toggle_attendance(e):
            current_status = self.attendance_data.get(date, {}).get(str(student_id), False)
            new_status = not current_status
            
            if date not in self.attendance_data:
                self.attendance_data[date] = {}
            self.attendance_data[date][str(student_id)] = new_status
            self.save_attendance()
            
            # עדכון האייקון מיידית
            if new_status:
                new_icon = ft.Icon(ft.Icons.CHECK_CIRCLE, size=22, color=ft.Colors.GREEN_600)
                e.control.tooltip = "נוכח - לחץ לשינוי"
            else:
                new_icon = ft.Icon(ft.Icons.CLOSE, size=22, color=ft.Colors.RED_500)
                e.control.tooltip = "נעדר - לחץ לשינוי"
            
            e.control.content = new_icon
            e.control.update()
            
            # עדכון הטבלה המלאה ביחד עם ההודעות
            self.update_table_instantly()
            self.show_success_snackbar(f"נוכחות עודכנה ל{'נוכח' if new_status else 'נעדר'}")
        
        current_status = self.attendance_data.get(date, {}).get(str(student_id), False)
        
        if current_status:
            icon = ft.Icon(ft.Icons.CHECK_CIRCLE, size=22, color=ft.Colors.GREEN_600)
            tooltip_text = "נוכח - לחץ לשינוי"
        else:
            icon = ft.Icon(ft.Icons.CLOSE, size=22, color=ft.Colors.RED_500)
            tooltip_text = "נעדר - לחץ לשינוי"
        
        return ft.Container(
            content=icon,
            padding=ft.padding.all(8),
            border_radius=8,
            on_click=toggle_attendance,
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            tooltip=tooltip_text,
            ink=True,
            width=40,
            height=40,
            alignment=ft.alignment.center,
        )

    def create_empty_table_state(self):
        """Create empty state for table"""
        return ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.TABLE_VIEW_OUTLINED, size=64, color=ft.Colors.GREY_300),
                ft.Container(height=20),
                ft.Text(
                    "אין נתונים להצגה",
                    size=18,
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER,
                    rtl=True
                ),
                ft.Container(height=8),
                ft.Text(
                    "הוסף תאריכים ותלמידים כדי לראות את הטבלה",
                    size=14,
                    color=ft.Colors.GREY_500,
                    text_align=ft.TextAlign.CENTER,
                    rtl=True
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.all(80),
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.WHITE,
            border_radius=16,
            border=ft.border.all(1, ft.Colors.GREY_200),
        )

    def show_date_options(self, date: str):
        """Show options for date (edit/delete)"""
        def edit_date(e):
            self.page.close(dlg)
            self.edit_date_dialog(date)

        def delete_date(e):
            self.page.close(dlg)
            self.delete_date_dialog(date)

        def close_menu(e):
            self.page.close(dlg)

        content = ft.Column([
            ft.Container(
                content=ft.ListTile(
                    leading=ft.Icon(ft.Icons.EDIT_OUTLINED, color=ft.Colors.BLUE_500, size=20),
                    title=ft.Text("ערוך תאריך", rtl=True, size=14, color=ft.Colors.GREY_700),
                    on_click=edit_date,
                ),
                border_radius=8,
                ink=True,
            ),
            ft.Container(height=4),
            ft.Container(
                content=ft.ListTile(
                    leading=ft.Icon(ft.Icons.DELETE_OUTLINE, color=ft.Colors.RED_500, size=20),
                    title=ft.Text("מחק תאריך", rtl=True, size=14, color=ft.Colors.GREY_700),
                    on_click=delete_date,
                ),
                border_radius=8,
                ink=True,
            ),
        ], tight=True, spacing=0)

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"פעולות עבור {date}", rtl=True, size=16, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_800),
            content=content,
            actions=[
                ft.TextButton(
                    "ביטול", 
                    on_click=close_menu,
                    style=ft.ButtonStyle(color=ft.Colors.GREY_600)
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=16),
        )
        
        self.page.open(dlg)

    def edit_date_dialog(self, current_date: str):
        """Show edit date dialog with instant table update and CLEAR ERROR MESSAGES"""
        date_input = ft.TextField(
            value=current_date,
            width=280,
            text_align=ft.TextAlign.CENTER,
            border_radius=12,
            bgcolor=ft.Colors.GREY_50,
            border_color=ft.Colors.GREY_200,
            focused_border_color=ft.Colors.BLUE_400,
            text_size=14,
            autofocus=True,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
        )

        error_message = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.ERROR_OUTLINE, size=16, color=ft.Colors.RED_500),
                ft.Container(width=8),
                ft.Text("", size=12, color=ft.Colors.RED_500, rtl=True, weight=ft.FontWeight.W_500),
            ], alignment=ft.MainAxisAlignment.CENTER),
            visible=False,
            bgcolor=ft.Colors.RED_50,
            border=ft.border.all(1, ft.Colors.RED_200),
            border_radius=8,
            padding=ft.padding.all(12),
            margin=ft.margin.only(top=12),
            animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
        )

        def show_error(message):
            """Show error message in dialog"""
            error_message.content.controls[2].value = message  
            error_message.visible = True
            error_message.update()
            
            date_input.border_color = ft.Colors.RED_400
            date_input.focused_border_color = ft.Colors.RED_400
            date_input.update()

        def hide_error():
            """Hide error message"""
            error_message.visible = False
            error_message.update()
            
            date_input.border_color = ft.Colors.GREY_200
            date_input.focused_border_color = ft.Colors.BLUE_400
            date_input.update()

        def on_input_change(e):
            """Hide error when user starts typing"""
            if error_message.visible:
                hide_error()

        date_input.on_change = on_input_change

        def on_confirm(e):
            try:
                new_date = date_input.value.strip() if date_input.value else ""
                
                if not new_date:
                    show_error("אנא הכנס תאריך!")
                    return
                
                if not AttendanceUtils.validate_date(new_date):
                    show_error("פורמט התאריך לא תקין! השתמש בפורמט: dd/mm/yyyy")
                    return
                
                if new_date != current_date and new_date in self.attendance_data:
                    show_error("התאריך הזה כבר קיים במערכת!")
                    return
                
                if new_date == current_date:
                    show_error("התאריך זהה לתאריך הנוכחי!")
                    return
                
                self.attendance_data[new_date] = self.attendance_data.pop(current_date)
                self.save_attendance()
                self.page.close(dlg)
                
                self.update_table_instantly()
                
                self.show_success_snackbar(f"התאריך עודכן מ-{current_date} ל-{new_date}")
                        
            except Exception as ex:
                print(f"Error in edit_date: {ex}")
                show_error("שגיאה בעריכת התאריך - נסה שוב")

        def on_cancel(e):
            self.page.close(dlg)

        # ✅ תוכן הדיאלוג עם הודעת השגיאה
        content = ft.Column([
            # אייקון ראשי
            ft.Container(
                content=ft.Icon(ft.Icons.EDIT_CALENDAR_OUTLINED, size=40, color=ft.Colors.BLUE_500),
                bgcolor=ft.Colors.BLUE_50,
                border_radius=20,
                padding=ft.padding.all(16),
            ),
            
            ft.Container(height=20),
            
            # הוראות
            ft.Text("ערוך את התאריך:", rtl=True, size=14, color=ft.Colors.GREY_700, weight=ft.FontWeight.W_500),
            ft.Text("(פורמט: dd/mm/yyyy)", rtl=True, size=12, color=ft.Colors.GREY_500, italic=True),
            
            ft.Container(height=12),
            
            # שדה הקלט
            date_input,
            
            # ✅ הודעת השגיאה
            error_message,
            
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, tight=True)

        actions = [
            ft.TextButton(
                "ביטול", 
                on_click=on_cancel,
                style=ft.ButtonStyle(color=ft.Colors.GREY_600)
            ),
            ft.ElevatedButton(
                "עדכן", 
                on_click=on_confirm,
                bgcolor=ft.Colors.BLUE_500,
                color=ft.Colors.WHITE,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                    padding=ft.padding.symmetric(horizontal=24, vertical=12)
                )
            ),
        ]

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("ערוך תאריך", rtl=True, size=18, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_800),
            content=content,
            actions=actions,
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=16),
        )
        
        self.page.open(dlg)


    def delete_date_dialog(self, date: str):
        """Show delete confirmation dialog with instant table update"""
        def confirm_delete(e):
            try:
                if date in self.attendance_data:
                    del self.attendance_data[date]
                    self.save_attendance()
                    self.page.close(dlg)
                    
                    # עדכון מיידי של הטבלה
                    self.update_table_instantly()
                    
                    # הודעת הצלחה
                    self.show_success_snackbar("התאריך נמחק בהצלחה!")
            except Exception as ex:
                print(f"Error in delete_date: {ex}")
                self.show_error_snackbar("שגיאה במחיקת התאריך")

        def cancel_delete(e):
            self.page.close(dlg)

        content = ft.Column([
            ft.Container(
                content=ft.Icon(ft.Icons.WARNING_AMBER_OUTLINED, size=40, color=ft.Colors.AMBER_500),
                bgcolor=ft.Colors.AMBER_50,
                border_radius=20,
                padding=ft.padding.all(16),
            ),
            ft.Container(height=20),
            ft.Text(
                f"האם אתה בטוח שברצונך למחוק את התאריך {date}?",
                rtl=True,
                text_align=ft.TextAlign.CENTER,
                size=14,
                color=ft.Colors.GREY_700
            ),
            ft.Container(height=8),
            ft.Text(
                "פעולה זו לא ניתנת לביטול!",
                rtl=True,
                text_align=ft.TextAlign.CENTER,
                size=12,
                color=ft.Colors.RED_600,
                weight=ft.FontWeight.W_500
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, tight=True)

        actions = [
            ft.TextButton(
                "ביטול", 
                on_click=cancel_delete,
                style=ft.ButtonStyle(color=ft.Colors.GREY_600)
            ),
            ft.ElevatedButton(
                "מחק",
                on_click=confirm_delete,
                bgcolor=ft.Colors.RED_500,
                color=ft.Colors.WHITE,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                    padding=ft.padding.symmetric(horizontal=24, vertical=12)
                )
            ),
        ]

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("מחיקת תאריך", rtl=True, size=18, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_800),
            content=content,
            actions=actions,
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=16),
        )
        
        self.page.open(dlg)

    def update_table_instantly(self):
        """Update the table instantly after data changes - הפונקציה המרכזית לעדכון מיידי"""
        try:
            self.load_data()
            if self.table_container:
                new_table = self.create_modern_data_table()
                
                if hasattr(new_table, 'content'):
                    self.table_container.content = new_table.content
                else:
                    self.table_container.content = new_table
                
                self.table_container.bgcolor = getattr(new_table, 'bgcolor', ft.Colors.WHITE)
                self.table_container.border_radius = getattr(new_table, 'border_radius', 16)
                self.table_container.border = getattr(new_table, 'border', ft.border.all(1, ft.Colors.GREY_200))
                self.table_container.shadow = getattr(new_table, 'shadow', None)
                
                self.table_container.update()
            
            if self.parent_page and hasattr(self.parent_page, 'refresh_stats_only'):
                self.parent_page.refresh_stats_only()
            
            try:
                self.page.update()
            except:
                pass
                    
        except Exception as e:
            print(f"Error updating table instantly: {e}")
            self.show_error_snackbar("שגיאה בעדכון הטבלה")

    def force_refresh_from_external(self):
        """פונקציה מיוחדת לרענון מעמודים חיצוניים - ללא ניווט"""
        try:
            print("Force refresh called from external source")
            self.load_data()
            
            if self.table_container:
                new_table = self.create_modern_data_table()
                
                if hasattr(new_table, 'content'):
                    self.table_container.content = new_table.content
                else:
                    self.table_container.content = new_table
                
                self.table_container.bgcolor = getattr(new_table, 'bgcolor', ft.Colors.WHITE)
                self.table_container.border_radius = getattr(new_table, 'border_radius', 16)
                self.table_container.border = getattr(new_table, 'border', ft.border.all(1, ft.Colors.GREY_200))
                self.table_container.shadow = getattr(new_table, 'shadow', None)
                
                self.table_container.update()
            
            if hasattr(self.page, 'update'):
                self.page.update()
                
        except Exception as e:
            print(f"Error in force_refresh_from_external: {e}")

    
    def on_page_resume(self):
        """פונקציה שנקראת כשחוזרים לעמוד - לשימוש בניווט"""
        try:
            print("Page resumed - refreshing table")
            self.force_refresh_from_external()
        except Exception as e:
            print(f"Error in on_page_resume: {e}")
    
    def refresh_table(self):
        """Refresh the table data and view - פונקציה נוספת לרענון כללי"""
        try:
            self.update_table_instantly()
        except Exception as e:
            print(f"Error refreshing table: {e}")
            self.show_error_snackbar("שגיאה ברענון הטבלה")

    def show_success_snackbar(self, message: str):
        """Show success snackbar"""
        try:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Row([
                    ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color=ft.Colors.WHITE, size=20),
                    ft.Container(width=8),
                    ft.Text(message, rtl=True, color=ft.Colors.WHITE, size=14),
                ]),
                bgcolor=ft.Colors.GREEN_500,
                shape=ft.RoundedRectangleBorder(radius=12),
            )
            self.page.snack_bar.open = True
            self.page.update()
        except Exception as e:
            print(f"Error showing success snackbar: {e}")

    def show_error_snackbar(self, message: str):
        """Show error snackbar"""
        try:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Row([
                    ft.Icon(ft.Icons.ERROR_OUTLINE, color=ft.Colors.WHITE, size=20),
                    ft.Container(width=8),
                    ft.Text(message, rtl=True, color=ft.Colors.WHITE, size=14),
                ]),
                bgcolor=ft.Colors.RED_500,
                shape=ft.RoundedRectangleBorder(radius=12),
            )
            self.page.snack_bar.open = True
            self.page.update()
        except Exception as e:
            print(f"Error showing error snackbar: {e}")

    def go_back(self, e):
        """Go back to group attendance page"""
        from pages.group_attendance_page import GroupAttendancePage
        try:
            if self.navigation_handler:
                group_page = GroupAttendancePage(self.page, self.navigation_handler, self.group)
                self.navigation_handler(group_page, None)
        except Exception as ex:
            print(f"Error in go_back: {ex}")

    def create_gradient_background(self):
        """Create subtle gradient background"""
        return ft.Container()  