import flet as ft

class FormFields:
    """Factory for creating consistent form fields"""
    
    @staticmethod
    def create_text_field(label, hint_text, keyboard_type=None):
        """Create a styled text field"""
        return ft.TextField(
            label=label,
            hint_text=hint_text,
            border_radius=8,
            bgcolor="#f7fafc",
            border_color="#e2e8f0",
            focused_border_color="#4299e1",
            text_size=14,
            label_style=ft.TextStyle(color="#4a5568"),
            keyboard_type=keyboard_type,
        )
    
    @staticmethod
    def create_group_form_fields():
        """Create all group form fields"""
        return {
            'name': FormFields.create_text_field(
                "שם הקבוצה",
                "הכנס את שם הקבוצה"
            ),
            'location': FormFields.create_text_field(
                "מיקום הקבוצה",
                "הכנס את מיקום הקבוצה"
            ),
            'price': FormFields.create_text_field(
                "עלות הקבוצה",
                "הכנס את עלות הקבוצה",
                ft.KeyboardType.NUMBER
            ),
            'age': FormFields.create_text_field(
                "קבוצת גילאים",
                "לדוגמה: 6-8 שנים"
            ),
            'teacher': FormFields.create_text_field(
                "שם המורה",
                "הכנס את שם המורה"
            )
        }
