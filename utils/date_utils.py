from datetime import datetime

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