import flet as ft
import json
from utils.manage_json import ManageJSON

class GroupDialogs:
    @staticmethod
    def create_edit_dialog(page, group, on_success_callback):
        """Create the complete edit group dialog"""
        
        name_field = ft.TextField(
            label="שם הקבוצה",
            value=group.get("name", ""),
            border_color="#e1e7ef",
            focused_border_color="#3b82f6",
            text_align=ft.TextAlign.RIGHT,
            rtl=True,
            label_style=ft.TextStyle(color="#64748b", size=14, weight=ft.FontWeight.W_500),
            text_style=ft.TextStyle(color="#0f172a", size=16),
            border_radius=12,
            filled=True,
            fill_color="#fafbfc",
            content_padding=ft.padding.symmetric(horizontal=16, vertical=14),
            cursor_color="#3b82f6"
        )
        
        teacher_field = ft.TextField(
            label="מורה",
            value=group.get("teacher", ""),
            border_color="#e1e7ef",
            focused_border_color="#3b82f6",
            text_align=ft.TextAlign.RIGHT,
            rtl=True,
            label_style=ft.TextStyle(color="#64748b", size=14, weight=ft.FontWeight.W_500),
            text_style=ft.TextStyle(color="#0f172a", size=16),
            border_radius=12,
            filled=True,
            fill_color="#fafbfc",
            content_padding=ft.padding.symmetric(horizontal=16, vertical=14),
            cursor_color="#3b82f6"
        )
        
        age_group_field = ft.TextField(
            label="קבוצת גיל",
            value=group.get("age_group", ""),
            border_color="#e1e7ef",
            focused_border_color="#3b82f6",
            text_align=ft.TextAlign.RIGHT,
            rtl=True,
            label_style=ft.TextStyle(color="#64748b", size=14, weight=ft.FontWeight.W_500),
            text_style=ft.TextStyle(color="#0f172a", size=16),
            border_radius=12,
            filled=True,
            fill_color="#fafbfc",
            content_padding=ft.padding.symmetric(horizontal=16, vertical=14),
            cursor_color="#3b82f6"
        )
        
        price_field = ft.TextField(
            label="מחיר לחודש",
            value=str(group.get("price", "")),
            border_color="#e1e7ef",
            focused_border_color="#3b82f6",
            keyboard_type=ft.KeyboardType.NUMBER,
            text_align=ft.TextAlign.RIGHT,
            rtl=True,
            suffix_text="₪",
            label_style=ft.TextStyle(color="#64748b", size=14, weight=ft.FontWeight.W_500),
            text_style=ft.TextStyle(color="#0f172a", size=16),
            border_radius=12,
            filled=True,
            fill_color="#fafbfc",
            content_padding=ft.padding.symmetric(horizontal=16, vertical=14),
            cursor_color="#3b82f6",
            disabled=True
        )
        
        location_field = ft.TextField(
            label="מיקום",
            value=group.get("location", ""),
            border_color="#e1e7ef",
            focused_border_color="#3b82f6",
            text_align=ft.TextAlign.RIGHT,
            rtl=True,
            label_style=ft.TextStyle(color="#64748b", size=14, weight=ft.FontWeight.W_500),
            text_style=ft.TextStyle(color="#0f172a", size=16),
            border_radius=12,
            filled=True,
            fill_color="#fafbfc",
            content_padding=ft.padding.symmetric(horizontal=16, vertical=14),
            cursor_color="#3b82f6"
        )
        
        start_date_field = ft.TextField(
            label="תאריך התחלה",
            value=group.get("group_start_date", ""),
            border_color="#e1e7ef",
            focused_border_color="#3b82f6",
            hint_text="dd/mm/yyyy",
            text_align=ft.TextAlign.RIGHT,
            rtl=True,
            label_style=ft.TextStyle(color="#64748b", size=14, weight=ft.FontWeight.W_500),
            text_style=ft.TextStyle(color="#0f172a", size=16),
            hint_style=ft.TextStyle(color="#94a3b8", size=14),
            border_radius=12,
            filled=True,
            fill_color="#fafbfc",
            content_padding=ft.padding.symmetric(horizontal=16, vertical=14),
            cursor_color="#3b82f6"
        )

        end_date_field = ft.TextField(
            label="תאריך סיום",
            value=group.get("group_end_date", ""),
            border_color="#e1e7ef",
            focused_border_color="#3b82f6",
            hint_text="dd/mm/yyyy",
            text_align=ft.TextAlign.RIGHT,
            rtl=True,
            label_style=ft.TextStyle(color="#64748b", size=14, weight=ft.FontWeight.W_500),
            text_style=ft.TextStyle(color="#0f172a", size=16),
            hint_style=ft.TextStyle(color="#94a3b8", size=14),
            border_radius=12,
            filled=True,
            fill_color="#fafbfc",
            content_padding=ft.padding.symmetric(horizontal=16, vertical=14),
            cursor_color="#3b82f6"
        )

        
        day_of_week_dropdown = ft.Dropdown(
            label="יום בשבוע",
            value=group.get("day_of_week", ""),
            border_color="#e1e7ef",
            focused_border_color="#3b82f6",
            text_align=ft.TextAlign.RIGHT,
            label_style=ft.TextStyle(color="#64748b", size=14, weight=ft.FontWeight.W_500),
            text_style=ft.TextStyle(color="#0f172a", size=16),
            border_radius=12,
            filled=True,
            fill_color="#fafbfc",
            content_padding=ft.padding.symmetric(horizontal=16, vertical=14),
            alignment=ft.alignment.center_right,
            width=None,
            expand=True,  
            options=[
                ft.dropdown.Option("ראשון"),
                ft.dropdown.Option("שני"),
                ft.dropdown.Option("שלישי"),
                ft.dropdown.Option("רביעי"),
                ft.dropdown.Option("חמישי"),
                ft.dropdown.Option("שישי"),
                ft.dropdown.Option("שבת"),
            ]
        )

        
        phone_field = ft.TextField(
            label="טלפון מורה",
            value=group.get("teacher_phone", ""),
            border_color="#e1e7ef",
            focused_border_color="#3b82f6",
            keyboard_type=ft.KeyboardType.PHONE,
            text_align=ft.TextAlign.RIGHT,
            rtl=True,
            label_style=ft.TextStyle(color="#64748b", size=14, weight=ft.FontWeight.W_500),
            text_style=ft.TextStyle(color="#0f172a", size=16),
            border_radius=12,
            filled=True,
            fill_color="#fafbfc",
            content_padding=ft.padding.symmetric(horizontal=16, vertical=14),
            cursor_color="#3b82f6"
        )
        
        email_field = ft.TextField(
            label="אימייל מורה",
            value=group.get("teacher_email", ""),
            border_color="#e1e7ef",
            focused_border_color="#3b82f6",
            keyboard_type=ft.KeyboardType.EMAIL,
            text_align=ft.TextAlign.RIGHT,
            rtl=True,
            label_style=ft.TextStyle(color="#64748b", size=14, weight=ft.FontWeight.W_500),
            text_style=ft.TextStyle(color="#0f172a", size=16),
            border_radius=12,
            filled=True,
            fill_color="#fafbfc",
            content_padding=ft.padding.symmetric(horizontal=16, vertical=14),
            cursor_color="#3b82f6"
        )

        error_container = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.ERROR_OUTLINE, color="#ef4444", size=20),
                ft.Text("", color="#ef4444", size=14, weight=ft.FontWeight.BOLD)
            ], spacing=8),
            bgcolor=ft.Colors.with_opacity(0.1, "#ef4444"),
            border_radius=8,
            padding=ft.padding.all(12),
            visible=False,
            margin=ft.margin.only(bottom=16),
            alignment=ft.alignment.center_right  
        )

        def check_group_name_exists(new_name, current_name):
            """Check if group name already exists (excluding current group)"""
            try:
                data_dir = ManageJSON.get_appdata_path() / "data"
                data_dir.mkdir(parents=True, exist_ok=True)
                groups_file = data_dir / "groups.json"
                
                with open(groups_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                existing_groups = data.get("groups", [])
                return any(g.get('name', '').strip().lower() == new_name.lower() 
                          for g in existing_groups 
                          if g.get('name', '').strip().lower() != current_name.lower())
            except Exception as e:
                print(f"Error checking group name existence: {e}")
                return False

        def show_error_dialog(message):
            """Show error message inside dialog"""
            error_container.content.controls[1].value = message
            error_container.visible = True
            page.update()

        def save_changes(e):
            try:
                error_container.visible = False
                
                new_group_name = name_field.value.strip() if name_field.value.strip() else "לא צוין"
                current_group_name = group.get("name", "")
                
                if new_group_name != current_group_name and check_group_name_exists(new_group_name, current_group_name):
                    show_error_dialog("קבוצה בשם זה כבר קיימת במערכת")
                    return
                
                data_dir = ManageJSON.get_appdata_path() / "data"
                data_dir.mkdir(parents=True, exist_ok=True)
                groups_file = data_dir / "groups.json"
                
                with open(groups_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                groups = data.get("groups", [])
                old_group_name = None
                
                for i, g in enumerate(groups):
                    if g.get("id") == group.get("id") or g.get("name") == group.get("name"):
                        old_group_name = g.get("name")
                        updated_group = {
                            "id": g.get("id", group.get("id")),
                            "name": new_group_name,
                            "teacher": teacher_field.value.strip() if teacher_field.value.strip() else "לא צוין",
                            "age_group": age_group_field.value.strip() if age_group_field.value.strip() else "לא צוין",
                            "price": price_field.value.strip() if price_field.value.strip() else "0",
                            "location": location_field.value.strip() if location_field.value.strip() else "לא צוין",
                            "group_start_date": start_date_field.value.strip() if start_date_field.value.strip() else "לא צוין",
                            "group_end_date": end_date_field.value.strip() if end_date_field.value.strip() else "לא צוין",
                            "day_of_week": day_of_week_dropdown.value if day_of_week_dropdown.value else "לא צוין",
                            "teacher_phone": phone_field.value.strip() if phone_field.value.strip() else "לא צוין",
                            "teacher_email": email_field.value.strip() if email_field.value.strip() else "לא צוין",
                            "students": g.get("students", []) 
                        }
                        groups[i] = updated_group
                        break
                
                with open(groups_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                if old_group_name and old_group_name != new_group_name:
                    try:
                        students_file = data_dir / "students.json"
                        if students_file.exists():
                            with open(students_file, "r", encoding="utf-8") as f:
                                students_data = json.load(f)
                            
                            students_updated = False
                            for student in students_data.get("students", []):
                                student_groups = student.get("groups", [])
                                
                                if isinstance(student_groups, list):
                                    for j, group_name in enumerate(student_groups):
                                        if group_name.strip() == old_group_name.strip():
                                            student_groups[j] = new_group_name
                                            students_updated = True
                                elif isinstance(student_groups, str):
                                    if student_groups.strip() == old_group_name.strip():
                                        student["groups"] = new_group_name
                                        students_updated = True
                            
                            if students_updated:
                                with open(students_file, "w", encoding="utf-8") as f:
                                    json.dump(students_data, f, ensure_ascii=False, indent=2)
                            
                    except Exception as students_ex:
                        print(f"⚠️ Error in update: {str(students_ex)}")
                
                page.close(edit_dialog)
                on_success_callback("הקבוצה עודכנה בהצלחה")
                
            except Exception as ex:
                on_success_callback(f"שגיאה בעדכון הקבוצה: {str(ex)}", is_error=True)


        def cancel_edit(e):
            page.close(edit_dialog)

        edit_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Column([
                            ft.Text(
                                "עריכת קבוצה",
                                size=28,
                                weight=ft.FontWeight.BOLD,
                                color="#0f172a",
                                text_align=ft.TextAlign.RIGHT
                            ),
                            ft.Text(
                                f"עדכון פרטי הקבוצה: {group.get('name', 'לא צוין')}",
                                size=16,
                                color="#64748b",
                                text_align=ft.TextAlign.RIGHT
                            ),
                        ], spacing=4, expand=True, horizontal_alignment=ft.CrossAxisAlignment.END),
                        ft.Container(
                            content=ft.Icon(
                                ft.Icons.EDIT_OUTLINED,
                                size=32,
                                color="#3b82f6"
                            ),
                            bgcolor=ft.Colors.with_opacity(0.1, "#3b82f6"),
                            border_radius=12,
                            padding=ft.padding.all(12)
                        ),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Container(height=16),
                    ft.Divider(color="#e2e8f0", height=1, thickness=1),
                ], spacing=0),
                padding=ft.padding.all(0)
            ),
            content=ft.Container(
                content=ft.Column([
                    error_container,  
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Container(
                                    content=ft.Icon(ft.Icons.INFO_OUTLINE, color="#3b82f6", size=18),
                                    bgcolor=ft.Colors.with_opacity(0.1, "#3b82f6"),
                                    border_radius=8,
                                    padding=ft.padding.all(6)
                                ),
                                ft.Text(
                                    "פרטים כלליים",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color="#0f172a"
                                ),
                            ], alignment=ft.MainAxisAlignment.END, spacing=8),
                            
                            ft.Container(height=16),
                            
                            ft.ResponsiveRow([
                                ft.Container(
                                    content=name_field,
                                    col={"xs": 12, "md": 6},
                                    padding=ft.padding.only(bottom=16, left=8)
                                ),
                                ft.Container(
                                    content=teacher_field,
                                    col={"xs": 12, "md": 6},
                                    padding=ft.padding.only(bottom=16, right=8)
                                ),
                            ]),
                            
                            ft.ResponsiveRow([
                                ft.Container(
                                    content=age_group_field,
                                    col={"xs": 12, "md": 6},
                                    padding=ft.padding.only(bottom=16, left=8)
                                ),
                                ft.Container(
                                    content=price_field,
                                    col={"xs": 12, "md": 6},
                                    padding=ft.padding.only(bottom=16, right=8)
                                ),
                            ]),
                        ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.END),
                        bgcolor="#ffffff",
                        border_radius=12,
                        padding=ft.padding.all(20),
                        border=ft.border.all(1, "#f1f5f9"),
                        margin=ft.margin.only(bottom=16)
                    ),
                    
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Container(
                                    content=ft.Icon(ft.Icons.LOCATION_ON_OUTLINED, color="#10b981", size=18),
                                    bgcolor=ft.Colors.with_opacity(0.1, "#10b981"),
                                    border_radius=8,
                                    padding=ft.padding.all(6)
                                ),
                                ft.Text(
                                    "מיקום ולוח זמנים",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color="#0f172a"
                                ),
                            ], alignment=ft.MainAxisAlignment.END, spacing=8),
                            
                            ft.Container(height=16),
                            
                            ft.ResponsiveRow([
                                ft.Container(
                                    content=location_field,
                                    col={"xs": 12, "md": 6},
                                    padding=ft.padding.only(bottom=16, left=8)
                                ),
                                ft.Container(
                                    content=day_of_week_dropdown,
                                    col={"xs": 12, "md": 6},
                                    padding=ft.padding.only(bottom=16, right=8)
                                ),
                            ]),
                            
                            ft.ResponsiveRow([
                                 ft.Container(
                                    content=end_date_field,
                                    col={"xs": 12, "md": 6},
                                    padding=ft.padding.only(bottom=16, right=8)
                                ),
                                ft.Container(
                                    content=start_date_field,
                                    col={"xs": 12, "md": 6},
                                    padding=ft.padding.only(bottom=16, left=8)
                                )
                            ]),

                        ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.END),
                        bgcolor="#ffffff",
                        border_radius=12,
                        padding=ft.padding.all(20),
                        border=ft.border.all(1, "#f1f5f9"),
                        margin=ft.margin.only(bottom=16)
                    ),
                    
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Container(
                                    content=ft.Icon(ft.Icons.CONTACT_PHONE_OUTLINED, color="#f59e0b", size=18),
                                    bgcolor=ft.Colors.with_opacity(0.1, "#f59e0b"),
                                    border_radius=8,
                                    padding=ft.padding.all(6)
                                ),
                                ft.Text(
                                    "פרטי קשר",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color="#0f172a"
                                ),
                            ], alignment=ft.MainAxisAlignment.END, spacing=8),
                            
                            ft.Container(height=16),
                            
                            ft.ResponsiveRow([
                                ft.Container(
                                    content=email_field,
                                    col={"xs": 12, "md": 6},
                                    padding=ft.padding.only(bottom=0, left=8)
                                ),
                                ft.Container(
                                    content=phone_field,
                                    col={"xs": 12, "md": 6},
                                    padding=ft.padding.only(bottom=0, right=8)
                                ),
                            ]),
                        ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.END),
                        bgcolor="#ffffff",
                        border_radius=12,
                        padding=ft.padding.all(20),
                        border=ft.border.all(1, "#f1f5f9"),
                    ),
                ], spacing=0, scroll=ft.ScrollMode.AUTO),
                width=800,
                height=600,
                padding=ft.padding.all(0)
            ),
            actions=[
                ft.Container(
                    content=ft.Column([
                        ft.Divider(color="#e2e8f0", height=1),
                        ft.Container(height=16),
                        ft.Row([
                            ft.Container(
                                content=ft.TextButton(
                                    content=ft.Row([
                                        ft.Icon(ft.Icons.CLOSE, size=18, color="#64748b"),
                                        ft.Text("ביטול", color="#64748b", size=15, weight=ft.FontWeight.W_600)
                                    ], spacing=8, tight=True),
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=12),
                                        padding=ft.padding.symmetric(horizontal=24, vertical=14),
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
                                    on_click=cancel_edit
                                ),
                                shadow=ft.BoxShadow(
                                    spread_radius=0,
                                    blur_radius=6,
                                    color=ft.Colors.with_opacity(0.04, ft.Colors.BLACK),
                                    offset=ft.Offset(0, 2),
                                ),
                            ),
                            
                            ft.Container(width=16),
                            
                            ft.Container(
                                content=ft.ElevatedButton(
                                    content=ft.Row([
                                        ft.Icon(ft.Icons.SAVE_OUTLINED, size=20, color="white"),
                                        ft.Text("שמור שינויים", color="white", size=15, weight=ft.FontWeight.BOLD)
                                    ], spacing=10, tight=True),
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=12),
                                        padding=ft.padding.symmetric(horizontal=28, vertical=16),
                                        elevation={
                                            ft.ControlState.DEFAULT: 3,
                                            ft.ControlState.HOVERED: 6,
                                            ft.ControlState.PRESSED: 1,
                                        },
                                        bgcolor={
                                            ft.ControlState.DEFAULT: "#3b82f6",
                                            ft.ControlState.HOVERED: "#2563eb",
                                            ft.ControlState.PRESSED: "#1d4ed8",
                                        },
                                        overlay_color={
                                            ft.ControlState.HOVERED: ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                                            ft.ControlState.PRESSED: ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
                                        }
                                    ),
                                    on_click=save_changes
                                ),
                                animate_scale=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
                            ),
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=0),
                    ], spacing=0),
                    padding=ft.padding.symmetric(horizontal=24, vertical=0)
                )
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            bgcolor="#f8fafc",
            shape=ft.RoundedRectangleBorder(radius=16),
            content_padding=ft.padding.all(24),
            title_padding=ft.padding.all(24),
            actions_padding=ft.padding.only(left=24, right=24, bottom=24, top=0),
        )

        error_container.visible = False

        return edit_dialog

    @staticmethod
    def create_delete_confirmation_dialog(page, group, on_success_callback):
        """Show confirmation dialog before deleting group"""
        
        def delete_group(e):
            try:
                data_dir = ManageJSON.get_appdata_path() / "data"
                data_dir.mkdir(parents=True, exist_ok=True)
                groups_file = data_dir / "groups.json"
                
                with open(groups_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                groups = data.get("groups", [])
                groups = [g for g in groups if g["name"] != group["name"]]
                data["groups"] = groups
                
                with open(groups_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                page.close(delete_dialog)
                
                on_success_callback("הקבוצה נמחקה בהצלחה")
                
            except Exception as ex:
                on_success_callback(f"שגיאה במחיקת הקבוצה: {str(ex)}", is_error=True)

        def cancel_delete(e):
            page.close(delete_dialog)

        delete_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("מחיקת קבוצה", size=20, weight=ft.FontWeight.BOLD, color="#f56565", text_align=ft.TextAlign.RIGHT),
            content=ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.WARNING, size=48, color="#f56565"),
                    ft.Text(
                        f"\u202Bהאם אתה בטוח שברצונך למחוק את הקבוצה {group['name']}?\u202C",
                        size=16,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "פעולה זו לא ניתנת לביטול",
                        size=14,
                        color="#718096",
                        text_align=ft.TextAlign.CENTER
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12, tight=True),
                width=350,
                padding=ft.padding.symmetric(vertical=10)
            ),
            actions=[
                ft.TextButton(
                    "ביטול",
                    on_click=cancel_delete,
                    style=ft.ButtonStyle(color="#718096")
                ),
                ft.ElevatedButton(
                    "מחק",
                    on_click=delete_group,
                    bgcolor="#f56565",
                    color="white"
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        return delete_dialog