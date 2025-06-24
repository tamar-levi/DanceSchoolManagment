class ValidationUtils:
    """Utility class for form validation"""
    
    @staticmethod
    def validate_required_fields(fields_dict):
        """Validate that all required fields are filled"""
        empty_fields = [key for key, value in fields_dict.items() if not value or not value.strip()]
        return len(empty_fields) == 0, empty_fields
    
    @staticmethod
    def validate_numeric(value, field_name="Field"):
        """Validate that a value is numeric"""
        try:
            float(value)
            return True, None
        except ValueError:
            return False, f"{field_name} חייב להיות מספר"
    
    @staticmethod
    def validate_phone(phone):
        """Basic phone validation"""
        if not phone:
            return False, "מספר טלפון נדרש"
        
        # Remove spaces and dashes
        clean_phone = phone.replace(" ", "").replace("-", "")
        
        # Check if it's all digits and reasonable length
        if not clean_phone.isdigit() or len(clean_phone) < 9 or len(clean_phone) > 11:
            return False, "מספר טלפון לא תקין"
        
        return True, None
    
    @staticmethod
    def validate_name(name):
        """Basic name validation"""
        if not name or not name.strip():
            return False, "שם נדרש"
        
        if len(name.strip()) < 2:
            return False, "שם חייב להכיל לפחות 2 תווים"
        
        return True, None
