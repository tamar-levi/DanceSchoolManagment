from datetime import datetime
import json

class DateUtils:
    """Utility class for date operations"""
    
    @staticmethod
    def get_current_date():
        """Get current date in Hebrew format"""
        return datetime.now().strftime("%d/%m/%Y")
    
    @staticmethod
    def format_date(date_string):
        """Format date string consistently"""
        if not date_string:
            return ""
        
        try:
            date_obj = datetime.strptime(date_string, "%d/%m/%Y")
            return date_obj.strftime("%d/%m/%Y")
        except ValueError:
            return date_string
    
    @staticmethod
    def validate_date(date_string):
        """Validate date format"""
        if not date_string:
            return False, "תאריך נדרש"
        
        try:
            datetime.strptime(date_string, "%d/%m/%Y")
            return True, None
        except ValueError:
            return False, "פורמט תאריך לא תקין (dd/mm/yyyy)"
        
    @staticmethod
    def get_join_date_by_id(student_id: str) -> str | None:
        try:
            from utils.manage_json import ManageJSON
            data_dir = ManageJSON.get_appdata_path() / "data"
            joining_dates_file = data_dir / "joining_dates.json"
            
            if not joining_dates_file.exists():
                return None
                
            with open(joining_dates_file, "r", encoding="utf-8") as f:
                joining_dates = json.load(f)
            
            for group in joining_dates.values():
                for student in group:
                    if student.get("student_id") == student_id:
                        return student.get("join_date")
            
            return None
            
        except Exception as e:
            print(f"Error getting join date for student {student_id}: {e}")
            return None