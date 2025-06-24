import json
import os
from datetime import datetime

def get_total_students():
    """מחזירה את מספר התלמידות הכולל"""
    try:
        students_file = "data/students.json"
        
        if not os.path.exists(students_file):
            return 0
            
        with open(students_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if 'students' in data:
                return len(data['students'])
            return 0
                    
    except Exception:
        return 0

def get_total_groups():
    """מחזירה את מספר הקבוצות הכולל"""
    try:
        groups_file = "data/groups.json"
        
        if not os.path.exists(groups_file):
            return 0
            
        with open(groups_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if 'groups' in data:
                return len(data['groups'])
            return 0
                
    except Exception:
        return 0

def get_monthly_payments():
    """מחזירה את סכום התשלומים החודשיים"""
    try:
        total_payments = 0
        current_month = datetime.now().strftime("%m/%Y")  # פורמט התאריך שלך
        students_file = "data/students.json"
        
        if not os.path.exists(students_file):
            return 0
            
        with open(students_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if 'students' in data:
                for student in data['students']:
                    if 'payments' in student:
                        for payment in student['payments']:
                            # בדיקה אם התשלום מהחודש הנוכחי
                            payment_date = payment.get('date', '')
                            if payment_date.endswith(current_month):
                                amount = payment.get('amount', 0)
                                if isinstance(amount, (int, float)):
                                    total_payments += amount
                                elif isinstance(amount, str):
                                    try:
                                        total_payments += float(amount.replace(',', ''))
                                    except ValueError:
                                        continue
                    
        return int(total_payments)
    except Exception:
        return 0

def get_monthly_attendance_percentage():
    """מחזירה את אחוז הנוכחות החודשית הממוצע"""
    try:
        total_present = 0
        total_records = 0
        current_month = datetime.now().strftime("%m/%Y")  # פורמט mm/yyyy
        attendances_dir = "attendances"
        
        if not os.path.exists(attendances_dir):
            return 75  # ברירת מחדל
            
        # עבור על כל הקבצים בתיקיית attendances
        for filename in os.listdir(attendances_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(attendances_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        attendance_data = json.load(f)
                        
                        # עבור על כל התאריכים בקובץ
                        for date, students_attendance in attendance_data.items():
                            # בדיקה אם התאריך מהחודש הנוכחי
                            if date.endswith(current_month):
                                # עבור על כל התלמידות באותו תאריך
                                for student_id, is_present in students_attendance.items():
                                    total_records += 1
                                    if is_present:
                                        total_present += 1
                                        
                except (json.JSONDecodeError, KeyError):
                    continue
        
        if total_records == 0:
            return 75  # ברירת מחדל אם אין נתונים
            
        # חישוב אחוז הנוכחות
        attendance_percentage = int((total_present / total_records) * 100)
        return attendance_percentage
        
    except Exception:
        return 75  # ברירת מחדל במקרה של שגיאה

def get_all_time_attendance_percentage():
    """מחזירה את אחוז הנוכחות הכללי (כל הזמנים)"""
    try:
        total_present = 0
        total_records = 0
        attendances_dir = "attendances"
        
        if not os.path.exists(attendances_dir):
            return 75  # ברירת מחדל
            
        # עבור על כל הקבצים בתיקיית attendances
        for filename in os.listdir(attendances_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(attendances_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        attendance_data = json.load(f)
                        
                        # עבור על כל התאריכים בקובץ
                        for date, students_attendance in attendance_data.items():
                            # עבור על כל התלמידות באותו תאריך
                            for student_id, is_present in students_attendance.items():
                                total_records += 1
                                if is_present:
                                    total_present += 1
                                        
                except (json.JSONDecodeError, KeyError):
                    continue
        
        if total_records == 0:
            return 75  # ברירת מחדל אם אין נתונים
            
        # חישוב אחוז הנוכחות
        attendance_percentage = int((total_present / total_records) * 100)
        return attendance_percentage
        
    except Exception:
        return 75  # ברירת מחדל במקרה של שגיאה

def get_attendance_statistics():
    """מחזירה סטטיסטיקות מפורטות על נוכחות"""
    try:
        total_present = 0
        total_absent = 0
        attendances_dir = "attendances"
        
        if not os.path.exists(attendances_dir):
            return {"present": 0, "absent": 0, "percentage": 75}
            
        # עבור על כל הקבצים בתיקיית attendances
        for filename in os.listdir(attendances_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(attendances_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        attendance_data = json.load(f)
                        
                        # עבור על כל התאריכים בקובץ
                        for date, students_attendance in attendance_data.items():
                            # עבור על כל התלמידות באותו תאריך
                            for student_id, is_present in students_attendance.items():
                                if is_present:
                                    total_present += 1
                                else:
                                    total_absent += 1
                                        
                except (json.JSONDecodeError, KeyError):
                    continue
        
        total_records = total_present + total_absent
        if total_records == 0:
            return {"present": 0, "absent": 0, "percentage": 75}
            
        percentage = int((total_present / total_records) * 100)
        
        return {
            "present": total_present,
            "absent": total_absent,
            "total": total_records,
            "percentage": percentage
        }
        
    except Exception:
        return {"present": 0, "absent": 0, "percentage": 75}


def get_total_payments_amount():
    """מחזירה את סכום כל התשלומים שהתקבלו"""
    try:
        total_payments = 0
        students_file = "data/students.json"
        
        if not os.path.exists(students_file):
            return 0
            
        with open(students_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if 'students' in data:
                for student in data['students']:
                    if 'payments' in student:
                        for payment in student['payments']:
                            amount = payment.get('amount', 0)
                            if isinstance(amount, (int, float)):
                                total_payments += amount
                            elif isinstance(amount, str):
                                try:
                                    total_payments += float(amount.replace(',', ''))
                                except ValueError:
                                    continue
        return int(total_payments)
    except Exception:
        return 0

def get_students_by_payment_status():
    """מחזירה סטטיסטיקות על סטטוס תשלומים של התלמידות"""
    try:
        paid_count = 0
        debt_count = 0
        students_file = "data/students.json"
        
        if not os.path.exists(students_file):
            return {"paid": 0, "debt": 0}
            
        with open(students_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if 'students' in data:
                for student in data['students']:
                    payment_status = student.get('payment_status', '')
                    if payment_status == 'שולם':
                        paid_count += 1
                    elif 'חוב' in payment_status:
                        debt_count += 1
                    
        return {"paid": paid_count, "debt": debt_count}
    except Exception:
        return {"paid": 0, "debt": 0}

def get_groups_info():
    """מחזירה מידע על הקבוצות"""
    try:
        groups_file = "data/groups.json"
        
        if not os.path.exists(groups_file):
            return []
            
        with open(groups_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if 'groups' in data:
                return data['groups']
            return []
                
    except Exception:
        return []

def get_students_info():
    """מחזירה מידע על התלמידות"""
    try:
        students_file = "data/students.json"
        
        if not os.path.exists(students_file):
            return []
            
        with open(students_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if 'students' in data:
                return data['students']
            return []
                
    except Exception:
        return []

def format_currency(amount):
    """מעצבת סכום כסף בפורמט ישראלי"""
    return f"₪ {amount:,}".replace(',', ',')

def get_all_dashboard_data():
    """מחזירה את כל הנתונים לדשבורד במבנה אחד"""
    attendance_stats = get_attendance_statistics()
    
    return {
        'total_students': get_total_students(),
        'total_groups': get_total_groups(),
        'monthly_payments': get_monthly_payments(),
        'total_payments': get_total_payments_amount(),
        'attendance_percentage': get_monthly_attendance_percentage(),
        'all_time_attendance': get_all_time_attendance_percentage(),
        'payment_status': get_students_by_payment_status(),
        'attendance_stats': attendance_stats
    }

