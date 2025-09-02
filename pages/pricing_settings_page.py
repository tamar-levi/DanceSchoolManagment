import flet as ft
import json

class PricingSettingsPage:
    def __init__(self, page, navigate_callback):
        self.page = page
        self.navigate = navigate_callback
        from utils.manage_json import ManageJSON
        self.config_file = ManageJSON.get_appdata_path() / "data" / "pricing.json"
        self.load_config()
        
    def load_config(self):
        if self.config_file.exists():
            with open(self.config_file, "r") as f:
                self.config = json.load(f)
        else:
            self.config = {
                "single": 180,
                "two": 280, 
                "three": 360,
                "sister": 20
            }
            self.save_config()
    
    def save_config(self):
        with open(self.config_file, "w") as f:
            json.dump(self.config, f)
    
    def get_view(self):
        header = ft.Row([
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_color="#4299e1",
                on_click=lambda e: self.navigate(None, 0)
            ),
            ft.Text("הגדרות תמחור", size=32, weight=ft.FontWeight.BOLD, color="#1a202c"),
        ])
        
        single = ft.TextField(label="חוג בודד", value=str(self.config["single"]), 
                            width=150, suffix_text="₪", keyboard_type=ft.KeyboardType.NUMBER)
        two = ft.TextField(label="2 חוגים", value=str(self.config["two"]), 
                         width=150, suffix_text="₪", keyboard_type=ft.KeyboardType.NUMBER)
        three = ft.TextField(label="3+ חוגים", value=str(self.config["three"]), 
                           width=150, suffix_text="₪", keyboard_type=ft.KeyboardType.NUMBER)
        sister = ft.TextField(label="הנחת אחיות", value=str(self.config["sister"]), 
                            width=150, suffix_text="₪", keyboard_type=ft.KeyboardType.NUMBER)
        
        message_text = ft.Text("", size=14, color="#48bb78", visible=False)
        
        def save_clicked(e):
            try:
                self.config["single"] = int(single.value)
                self.config["two"] = int(two.value)
                self.config["three"] = int(three.value)
                self.config["sister"] = int(sister.value)
                self.save_config()
                
                message_text.value = "נשמר בהצלחה"
                message_text.color = "#48bb78"
                message_text.visible = True
                self.page.update()
                
                import threading
                threading.Timer(3.0, lambda: hide_message()).start()
                
            except:
                message_text.value = " הזן מספרים בלבד"
                message_text.color = "#e53e3e"
                message_text.visible = True
                self.page.update()
        
        def hide_message():
            message_text.visible = False
            self.page.update()
        
        card = ft.Container(
            content=ft.Column([
                ft.Row([single, two, three], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                ft.Row([sister], alignment=ft.MainAxisAlignment.CENTER),
                message_text,  
                ft.ElevatedButton("שמור", icon=ft.Icons.SAVE, on_click=save_clicked,
                                style=ft.ButtonStyle(bgcolor="#4299e1", color=ft.Colors.WHITE))
            ], spacing=30, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=30,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK))
        )
        
        return ft.Column([header, card], spacing=30)