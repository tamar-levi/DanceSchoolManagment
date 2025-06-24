import re
from datetime import datetime

class AddGroupValidator:
    """Validation for add group form"""
    
    @staticmethod
    def is_valid_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return re.match(pattern, email) is not None

    @staticmethod
    def is_valid_phone(phone):
        """Validate Israeli phone number format"""
        phone = re.sub(r'[\s-]', '', phone)
        patterns = [
            r'^0[2-9]\d{7,8}',
            r'^05[0-9]\d{7}',
            r'^1[5-9]\d{2,3}',
            r'^\+972[2-9]\d{7,8}',
        ]
        return any(re.match(pattern, phone) for pattern in patterns)

    @staticmethod
    def is_valid_date(date_str):
        """Validate date format dd/mm/yyyy"""
        try:
            datetime.strptime(date_str, '%d/%m/%Y')
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_field(key, value, required_fields):
        """Validate individual field"""
        error = None
        
        if key in required_fields and (not value or not value.strip()):
            error = f"{required_fields[key]} הוא שדה חובה"
        elif value and value.strip():
            if key == 'email' and value:
                if not AddGroupValidator.is_valid_email(value):
                    error = "כתובת אימייל לא תקינה"
            elif key == 'phone' and value:
                if not AddGroupValidator.is_valid_phone(value):
                    error = "מספר טלפון לא תקין"
            elif key == 'price':
                if not value.isdigit() or int(value) <= 0:
                    error = "המחיר חייב להיות מספר חיובי"
            elif key == 'start_date':
                if not AddGroupValidator.is_valid_date(value):
                    error = "תאריך לא תקין (dd/mm/yyyy)"
            elif key == 'name':
                if len(value.strip()) < 2:
                    error = "שם הקבוצה חייב להכיל לפחות 2 תווים"
            elif key == 'teacher':
                if len(value.strip()) < 2:
                    error = "שם המורה חייב להכיל לפחות 2 תווים"
        
        return error
