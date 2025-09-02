import json
import flet as ft
from typing import Dict, Any
from views.attendance_table_view import AttendanceTableView 
import datetime
from utils.attendance_utils import AttendanceUtils
from utils.manage_json import ManageJSON

class AttendanceCheckBox:
    def __init__(self, date: str, student_id: str, parent_page, is_checked: bool = False):
        self.date = date
        self.student_id = student_id
        self.parent_page = parent_page
        self.is_checked = is_checked
        
    def create_checkbox(self):
        """Create the modern checkbox widget with animations"""
        def on_click(e):
            self.is_checked = not self.is_checked
            self.parent_page.update_attendance(self.date, self.student_id, self.is_checked)
            e.control.content = self.get_checkbox_content()
            e.control.update()
        
        return ft.Container(
            content=self.get_checkbox_content(),
            width=40,
            height=40,
            border_radius=20,
            on_click=on_click,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            animate_scale=ft.Animation(200, ft.AnimationCurve.BOUNCE_OUT),
            ink=True,
            tooltip="לחץ כדי לשנות נוכחות",
        )
    
    def get_checkbox_content(self):
        """Get the modern checkbox content based on state"""
        if self.is_checked:
            return ft.Container(
                content=ft.Icon(
                    ft.Icons.CHECK_ROUNDED,
                    color=ft.Colors.WHITE,
                    size=24,
                ),
                bgcolor=ft.Colors.GREEN_500,
                border_radius=20,
                alignment=ft.alignment.center,
            )
        else:
            return ft.Container(
                content=ft.Icon(
                    ft.Icons.CLOSE_ROUNDED,
                    color=ft.Colors.WHITE,
                    size=24,
                ),
                bgcolor=ft.Colors.RED_500,
                border_radius=20,
                alignment=ft.alignment.center,
            )

class GroupAttendancePage:
    def __init__(self, page: ft.Page, navigation_handler=None, group: Dict[str, Any] = None):
        self.page = page
        self.navigation_handler = navigation_handler
        self.group = group or {}
        self.attendance_data = {}
        self.students = []
        
        self.main_content = None
        
        self.load_attendance()
        self.load_students()
        
    def load_attendance(self):
        """Load attendance data from JSON file"""
        attendances_dir = ManageJSON.get_appdata_path() / "attendances"
        attendance_file = attendances_dir / f"attendance_{self.group.get('id', '')}.json"
        
        if attendance_file.exists():
            try:
                with open(attendance_file, "r", encoding="utf-8") as f:
                    self.attendance_data = json.load(f)
            except Exception as e:
                print(f"Error loading attendance: {e}")
                self.attendance_data = {}
        else:
            self.attendance_data = {}

    def load_students(self):
        """Load students for this group"""
        try:
            data_dir = ManageJSON.get_appdata_path() / "data"
            students_file = data_dir / "students.json"
            
            if students_file.exists():
                with open(students_file, "r", encoding="utf-8") as f:
                    students_data = json.load(f)
                    self.students = []  
                    
                    for s in students_data.get("students", []):
                        student_groups = s.get("groups", [])
                        group_name = self.group.get("name", "").strip()
                        
                        if isinstance(student_groups, list):
                            if group_name in [g.strip() for g in student_groups]:
                                self.students.append({"id": s["id"], "name": s["name"]})
                        else:
                            if student_groups.strip() == group_name:
                                self.students.append({"id": s["id"], "name": s["name"]})
                                
        except Exception as e:
            print(f"Error loading students: {e}")
            self.students = []

    
    def load_data(self):
        """Load attendance and student data - FIXED VERSION"""
        self.attendance_data = AttendanceUtils.load_attendance_file(self.group.get('id', ''))
        
        try:
            data_dir = ManageJSON.get_appdata_path() / "data"
            students_file = data_dir / "students.json"
            
            if students_file.exists():
                with open(students_file, "r", encoding="utf-8") as f:
                    students_data = json.load(f)
                    self.students = []
                    
                    for s in students_data.get("students", []):
                        student_groups = s.get("groups", [])
                        group_name = self.group.get("name", "").strip()
                        
                        if isinstance(student_groups, list):
                            if group_name in [g.strip() for g in student_groups]:
                                self.students.append({"id": s["id"], "name": s["name"]})
                        else:
                            if student_groups.strip() == group_name:
                                self.students.append({"id": s["id"], "name": s["name"]})
                                
        except Exception as e:
            print(f"Error loading students in load_data: {e}")
            self.students = []

    def save_attendance(self):
        """Save attendance data to JSON file"""
        try:
            attendances_dir = ManageJSON.get_appdata_path() / "attendances"
            attendances_dir.mkdir(parents=True, exist_ok=True)
            attendance_file = attendances_dir / f"attendance_{self.group.get('id', '')}.json"
            
            with open(attendance_file, "w", encoding="utf-8") as f:
                json.dump(self.attendance_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving attendance: {e}")

    def update_attendance(self, date: str, student_id: str, is_present: bool):
        """Update attendance data"""
        if date not in self.attendance_data:
            self.attendance_data[date] = {}
        
        self.attendance_data[date][str(student_id)] = is_present
        self.save_attendance()

    def create_modern_card(self, content, bgcolor=None, padding=20, blur=True):
        """Create a modern glassmorphism card"""
        return ft.Container(
            content=content,
            bgcolor=bgcolor or ft.Colors.with_opacity(0.9, ft.Colors.WHITE),
            border_radius=16,
            padding=ft.padding.all(padding),
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, ft.Colors.GREY_300)),
            animate=ft.Animation(500, ft.AnimationCurve.EASE_OUT),
        )

    def create_header_card(self):
        """Create modern clean header card - RIGHT ALIGNED"""
        header_content = ft.Column([
            ft.Row([
                ft.Column([
                    ft.Text(
                        "ניהול נוכחות",
                        size=24,
                        weight=ft.FontWeight.W_700,
                        color=ft.Colors.GREY_800,
                        rtl=True
                    ),
                    ft.Text(
                        f"קבוצת {self.group.get('name', '')}",
                        size=14,
                        color=ft.Colors.GREY_500,
                        rtl=True
                    ),
                ], spacing=2, alignment=ft.CrossAxisAlignment.END),
                ft.Container(width=12),
                ft.Container(
                    content=ft.Icon(ft.Icons.HOW_TO_REG, size=28, color=ft.Colors.BLUE_600),
                    bgcolor=ft.Colors.BLUE_50,
                    border_radius=14,
                    padding=ft.padding.all(12),
                ),
            ], alignment=ft.alignment.center_right),
        ], 
        horizontal_alignment=ft.CrossAxisAlignment.END,
        spacing=0
        )
        
        return ft.Container(
            content=header_content,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_200),
            border_radius=16,
            padding=ft.padding.all(24),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                offset=ft.Offset(0, 4),
            ),
        )

    def create_stats_card(self):
        """Create clean centered statistics card"""
        dates = list(self.attendance_data.keys())
        total_dates = len(dates)
        total_students = len(self.students)
        
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Column([
                        ft.Container(
                            content=ft.Icon(ft.Icons.CALENDAR_TODAY_OUTLINED, size=20, color=ft.Colors.BLUE_600),
                            bgcolor=ft.Colors.BLUE_50,
                            border_radius=8,
                            padding=ft.padding.all(8),
                        ),
                        ft.Container(height=8),
                        ft.Text(str(total_dates), size=20, weight=ft.FontWeight.W_700, color=ft.Colors.GREY_800),
                        ft.Text("תאריכים", size=12, color=ft.Colors.GREY_500, rtl=True),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                    bgcolor=ft.Colors.WHITE,
                    border=ft.border.all(1, ft.Colors.GREY_200),
                    padding=ft.padding.all(16),
                    border_radius=12,
                    width=120,
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=8,
                        color=ft.Colors.with_opacity(0.06, ft.Colors.BLACK),
                        offset=ft.Offset(0, 2),
                    ),
                ),
                
                ft.Container(width=16),
                
                ft.Container(
                    content=ft.Column([
                        ft.Container(
                            content=ft.Icon(ft.Icons.PEOPLE_OUTLINE, size=20, color=ft.Colors.PURPLE_600),
                            bgcolor=ft.Colors.PURPLE_50,
                            border_radius=8,
                            padding=ft.padding.all(8),
                        ),
                        ft.Container(height=8),
                        ft.Text(str(total_students), size=20, weight=ft.FontWeight.W_700, color=ft.Colors.GREY_800),
                        ft.Text("תלמידים", size=12, color=ft.Colors.GREY_500, rtl=True),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                    bgcolor=ft.Colors.WHITE,
                    border=ft.border.all(1, ft.Colors.GREY_200),
                    padding=ft.padding.all(16),
                    border_radius=12,
                    width=120,
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=8,
                        color=ft.Colors.with_opacity(0.06, ft.Colors.BLACK),
                        offset=ft.Offset(0, 2),
                    ),
                ),
            ], 
            alignment=ft.MainAxisAlignment.CENTER,
            tight=True
            ),
            padding=ft.padding.symmetric(vertical=16),
            alignment=ft.alignment.center,
        )

    def create_actions_card(self):
        """Create clean centered actions section"""
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.ADD, size=18, color=ft.Colors.WHITE),
                        ft.Container(width=6),
                        ft.Text("הוסף תאריך", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE, rtl=True),
                    ], 
                    alignment=ft.MainAxisAlignment.CENTER,
                    tight=True,
                    spacing=0
                    ),
                    bgcolor=ft.Colors.BLUE_600,
                    border_radius=8,
                    padding=ft.padding.symmetric(horizontal=16, vertical=12),
                    width=140,
                    on_click=self.show_add_date_dialog,
                    animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
                    ink=True,
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=8,
                        color=ft.Colors.with_opacity(0.15, ft.Colors.BLUE_600),
                        offset=ft.Offset(0, 2),
                    ),
                ),
                
                ft.Container(width=12),
            ], 
            alignment=ft.MainAxisAlignment.CENTER,
            tight=True
            ),
            padding=ft.padding.symmetric(vertical=16),
            alignment=ft.alignment.center,
        )

    def show_add_date_dialog(self, e):
        """Show enhanced add date dialog with FIXED scrolling and clicking"""
        selected_date = None
        
        date_display = ft.Text(
            "לא נבחר תאריך",
            size=14,
            color=ft.Colors.GREY_500,
            rtl=True,
        )
        
        error_message = ft.Container(
            content=ft.Row([
                ft.Text("", size=12, color=ft.Colors.RED_500, rtl=True),
                ft.Container(width=8),
                ft.Icon(ft.Icons.ERROR_OUTLINE, size=16, color=ft.Colors.RED_500),
            ], alignment=ft.MainAxisAlignment.END),
            visible=False,
            bgcolor=ft.Colors.RED_50,
            border=ft.border.all(1, ft.Colors.RED_200),
            border_radius=8,
            padding=ft.padding.all(12),
            margin=ft.margin.only(top=8),
            alignment=ft.alignment.center_right,
        )
        
        def show_error(message):
            error_message.content.controls[0].value = message 
            error_message.visible = True
            error_message.update()
        
        def hide_error():
            error_message.visible = False
            error_message.update()
        
        def handle_date_change(e):
            nonlocal selected_date
            selected_date = e.control.value
            date_display.value = f"תאריך נבחר: {selected_date.strftime('%d/%m/%Y')}"
            date_display.color = ft.Colors.GREY_700
            date_display.update()
            hide_error()
        
        def handle_date_dismiss(e):
            pass
        
        def open_date_picker(e):
            hide_error()
            self.page.open(
                ft.DatePicker(
                    first_date=datetime.datetime(year=2020, month=1, day=1),
                    last_date=datetime.datetime(year=2030, month=12, day=31),
                    on_change=handle_date_change,
                    on_dismiss=handle_date_dismiss,
                )
            )
        
        date_picker_button = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.CALENDAR_TODAY, size=18, color=ft.Colors.BLUE_600),
                ft.Container(width=6),
                ft.Text("בחר תאריך", size=14, weight=ft.FontWeight.W_500, rtl=True),
            ], tight=True, alignment=ft.MainAxisAlignment.CENTER),
            bgcolor=ft.Colors.BLUE_50,
            border=ft.border.all(1, ft.Colors.BLUE_300),
            border_radius=8,
            padding=ft.padding.symmetric(horizontal=12, vertical=8),
            on_click=open_date_picker,
            ink=True,
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            width=140,
        )
        
        student_attendance = {}
        attendance_rows = []
        
        if self.students:
            for student in self.students:
                student_attendance[student["id"]] = False
                
                def create_toggle_click(student_id):
                    def toggle_attendance(e):
                        student_attendance[student_id] = not student_attendance[student_id]
                        is_present = student_attendance[student_id]
                        
                        if is_present:
                            e.control.icon = ft.Icons.CHECK_CIRCLE
                            e.control.icon_color = ft.Colors.GREEN_600
                            e.control.bgcolor = ft.Colors.GREEN_50
                            e.control.tooltip = "נוכח - לחץ לשינוי"
                        else:
                            e.control.icon = ft.Icons.CANCEL
                            e.control.icon_color = ft.Colors.RED_500
                            e.control.bgcolor = ft.Colors.RED_50
                            e.control.tooltip = "נעדר - לחץ לשינוי"
                        
                        e.control.update()
                        
                    return toggle_attendance
                
                student_row = ft.Row([
                    ft.Text(
                        student["name"],
                        size=14,
                        color=ft.Colors.GREY_700,
                        weight=ft.FontWeight.W_500,
                        rtl=True,
                        expand=True,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.CANCEL,  
                        icon_color=ft.Colors.RED_500, 
                        icon_size=24,
                        tooltip="נעדר - לחץ לשינוי",
                        on_click=create_toggle_click(student["id"]),
                        bgcolor=ft.Colors.RED_50,  
                        width=50,
                        height=50,
                        style=ft.ButtonStyle(
                            shape=ft.CircleBorder(),
                            animation_duration=200,  
                        ),
                    ),
                ], 
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                rtl=True,
                spacing=10,
                )
                
                wrapped_row = ft.Container(
                    content=student_row,
                    padding=ft.padding.all(12),
                    margin=ft.margin.only(bottom=8),
                    bgcolor=ft.Colors.WHITE,
                    border=ft.border.all(1, ft.Colors.GREY_200),
                    border_radius=8,
                )
                
                attendance_rows.append(wrapped_row)

        def on_confirm(e):
            try:
                if selected_date:
                    date_str = selected_date.strftime('%d/%m/%Y')
                    if date_str not in self.attendance_data:
                        self.attendance_data[date_str] = {}
                        
                        for student_id, is_present in student_attendance.items():
                            self.attendance_data[date_str][str(student_id)] = is_present
                        
                        self.save_attendance()
                        self.page.close(dlg)
                        self.refresh_view()
                        self.show_success_snackbar(f"תאריך {date_str} נוסף בהצלחה!")
                    else:
                        show_error("התאריך הזה כבר קיים במערכת!")
                else:
                    show_error("אנא בחרי תאריך")
            except Exception as ex:
                print(f"Error in add_date: {ex}")
                show_error("שגיאה בהוספת התאריך")

        def on_cancel(e):
            self.page.close(dlg)

        dialog_content = ft.Column([
            ft.Row([
                ft.Column([
                    ft.Text("הוסף תאריך חדש", size=18, weight=ft.FontWeight.W_700, color=ft.Colors.GREY_800, rtl=True),
                    ft.Text("בחר תאריך וסמן נוכחות", size=12, color=ft.Colors.GREY_500, rtl=True),
                ], spacing=4, alignment=ft.CrossAxisAlignment.END),
                ft.Container(width=12),
                ft.Container(
                    content=ft.Icon(ft.Icons.EVENT_OUTLINED, size=28, color=ft.Colors.BLUE_600),
                    bgcolor=ft.Colors.BLUE_50,
                    border_radius=14,
                    padding=ft.padding.all(10),
                ),
            ], alignment=ft.MainAxisAlignment.END),
            
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            
            ft.Column([
                ft.Row([
                    ft.Text("בחירת תאריך:", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_700, rtl=True),
                ], alignment=ft.MainAxisAlignment.END),
                ft.Container(height=8),
                ft.Row([date_picker_button], alignment=ft.MainAxisAlignment.END),
                ft.Container(height=8),
                ft.Row([date_display], alignment=ft.MainAxisAlignment.END),
                error_message,
            ]),
            
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            
            ft.Row([
                ft.Text("סמן נוכחות תלמידות:", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_700, rtl=True),
            ], alignment=ft.MainAxisAlignment.END),
            
            ft.Container(height=8),
            
        ], spacing=0, tight=True)

        if attendance_rows:
            students_list = ft.ListView(
                controls=attendance_rows,
                height=min(250, len(attendance_rows) * 70),
                spacing=0,
                padding=ft.padding.all(8),
            )
            
            students_container = ft.Container(
                content=students_list,
                bgcolor=ft.Colors.GREY_50,
                border_radius=12,
                border=ft.border.all(1, ft.Colors.GREY_200),
            )
            
            dialog_content.controls.append(students_container)

        actions = [
            ft.Row([
                ft.TextButton(
                    "ביטול", 
                    on_click=on_cancel,
                    style=ft.ButtonStyle(
                        color=ft.Colors.GREY_600,
                        padding=ft.padding.symmetric(horizontal=16, vertical=8),
                    )
                ),
                ft.Container(width=16),
                ft.ElevatedButton(
                    "הוסף תאריך",
                    on_click=on_confirm,
                    bgcolor=ft.Colors.BLUE_600,
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=ft.padding.symmetric(horizontal=16, vertical=8),
                        elevation=0,
                    )
                ),
            ], alignment=ft.MainAxisAlignment.CENTER)
        ]

        dlg = ft.AlertDialog(
            modal=True,
            content=ft.Container(
                content=dialog_content,
                width=450,
                height=min(600, 400 + (len(attendance_rows) * 70 if attendance_rows else 0)),
            ),
            actions=actions,
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=16),
            content_padding=ft.padding.all(24),
        )
        
        self.page.open(dlg)


    def create_attendance_table_card(self):
        """Create modern attendance table using AttendanceTableView"""
        dates = list(self.attendance_data.keys())
        
        if not dates and not self.students:
            empty_content = ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.EVENT_NOTE_OUTLINED, size=80, color=ft.Colors.GREY_300),
                    ft.Container(height=16),
                    ft.Text(
                        "אין תאריכים או תלמידים להצגה",
                        size=20,
                        weight=ft.FontWeight.W_500,
                        color=ft.Colors.GREY_600,
                        text_align=ft.TextAlign.CENTER,
                        rtl=True
                    ),
                    ft.Container(height=8),
                    ft.Text(
                        "הוסף תאריך חדש כדי להתחיל",
                        size=16,
                        color=ft.Colors.GREY_500,
                        text_align=ft.TextAlign.CENTER,
                        rtl=True
                    ),
                ], 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0
                ),
                padding=ft.padding.all(60),
                alignment=ft.alignment.center,
            )
            return self.create_modern_card(empty_content)
        
        self.table_view = AttendanceTableView(
            page=self.page, 
            navigation_handler=self.navigation_handler, 
            group=self.group,
            parent_page=self
        )
        
        table_header = ft.Column([
             ft.Row([
                ft.Icon(ft.Icons.TABLE_CHART, size=24, color=ft.Colors.BLUE_GREY_800),
                ft.Container(width=8),
                ft.Text(
                    "טבלת נוכחות",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_GREY_800,
                    rtl=True
                ),
            ]),
            ft.Container(height=8),
            ft.Text(
                "לחץ על התאריך כדי לערוך או למחוק אותו",
                size=14,
                color=ft.Colors.GREY_500,
                rtl=True,
                italic=True
            ),
            ft.Container(height=16),
        ])

        table_content = ft.Column([
            table_header,
            self.table_view.get_table_only(), 
        ], spacing=0, tight=True)

        return self.create_modern_card(table_content)

    def refresh_stats(self):
        """Refresh only statistics - simplified version"""
        try:
            self.refresh_view()
        except Exception as e:
            print(f"Error refreshing stats: {e}")

    def go_back(self, e):
        """Navigate back to attendance page"""
        try:
            if self.navigation_handler:
                self.navigation_handler(None, 2)
        except Exception as ex:
            print(f"Error in go_back: {ex}")

    def get_view(self):
        """Get the main view with clean design and full page scroll"""
        try:
            main_column = ft.Column([
                self.create_header_card(),
                self.create_stats_card(), 
                self.create_actions_card(),
                self.create_attendance_table_card(),
            ], 
            spacing=24,
            scroll=ft.ScrollMode.AUTO, 
            expand=True,
            )

            return ft.Container(
                content=main_column,
                padding=ft.padding.all(24),
                expand=True,
                bgcolor=ft.Colors.GREY_50,
            )
            
        except Exception as e:
            print(f"Error creating view: {e}")
            return ft.Container(
                content=ft.Text(f"שגיאה: {str(e)}", rtl=True),
                padding=ft.padding.all(40),
            )

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

    def refresh_view(self):
        """Refresh the view after data changes - WITHOUT navigation"""
        try:
            self.load_data()
            
            if hasattr(self, 'table_view') and self.table_view:
                self.table_view.force_refresh_from_external()
            
            if self.main_content:
                new_content = ft.Column([
                    self.create_header_card(),
                    self.create_stats_card(), 
                    self.create_actions_card(),
                    self.create_attendance_table_card(),
                ], 
                spacing=24,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                )
                
                self.main_content.content = new_content
                self.main_content.update()
            
            self.page.update()
                    
        except Exception as e:
            print(f"Error refreshing view: {e}")
            self.show_error_snackbar("שגיאה ברענון הנתונים")

    def refresh_table_only(self):
        """Refresh only the table part without full page reload"""
        try:
            self.load_attendance()
            
            if hasattr(self, 'table_view') and self.table_view:
                self.table_view.force_refresh_from_external()
                
        except Exception as e:
            print(f"Error refreshing table only: {e}")

    def refresh_stats_only(self):
        """Refresh only statistics without full reload"""
        try:
            self.load_attendance()
            
            if self.main_content and hasattr(self.main_content, 'content'):
                stats_card = self.create_stats_card()
                self.refresh_view()
                
        except Exception as e:
            print(f"Error refreshing stats only: {e}")
