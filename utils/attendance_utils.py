import json
import os
from typing import Dict, List, Any
import datetime

class AttendanceUtils:
    """Utility functions for attendance management"""
    
    @staticmethod
    def validate_date(date_str: str) -> bool:
        """Validate if date string is valid and not empty"""
        if not date_str or not date_str.strip():
            return False
        
        # Check if it's a reasonable date format
        date_str = date_str.strip()
        if len(date_str) < 8:  # Minimum for DD/MM/YY
            return False
            
        return True
    
    @staticmethod
    def clean_date_string(date_str: str) -> str:
        """Clean and normalize date string"""
        if not date_str:
            return ""
        return date_str.strip()
    
    @staticmethod
    def sort_dates_newest_first(dates: List[str]) -> List[str]:
        """Sort dates from newest to oldest with better parsing"""
        try:
            date_objects = []
            
            for date_str in dates:
                if not AttendanceUtils.validate_date(date_str):
                    continue
                    
                try:
                    date_obj = None
                    clean_date = AttendanceUtils.clean_date_string(date_str)
                    
                    # Try DD/MM/YYYY
                    if '/' in clean_date and len(clean_date.split('/')) == 3:
                        parts = clean_date.split('/')
                        if len(parts[0]) <= 2 and len(parts[1]) <= 2 and len(parts[2]) == 4:
                            day, month, year = parts
                            date_obj = datetime.datetime(int(year), int(month), int(day))
                    
                    # Try DD-MM-YYYY
                    elif '-' in clean_date and len(clean_date.split('-')) == 3:
                        parts = clean_date.split('-')
                        if len(parts[0]) <= 2 and len(parts[1]) <= 2 and len(parts[2]) == 4:
                            day, month, year = parts
                            date_obj = datetime.datetime(int(year), int(month), int(day))
                    
                    if date_obj:
                        date_objects.append((date_obj, clean_date))
                    else:
                        # If parsing failed, put at end
                        date_objects.append((datetime.datetime(1900, 1, 1), clean_date))
                        
                except Exception as e:
                    print(f"Error parsing date {date_str}: {e}")
                    date_objects.append((datetime.datetime(1900, 1, 1), clean_date))
            
            # Sort by date (newest first)
            date_objects.sort(key=lambda x: x[0], reverse=True)
            
            # Return only the date strings
            return [date_str for _, date_str in date_objects]
            
        except Exception as e:
            print(f"Error in sort_dates_newest_first: {e}")
            return sorted([d for d in dates if AttendanceUtils.validate_date(d)], reverse=True)
    
    @staticmethod
    def clean_attendance_data(attendance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean invalid dates from attendance data"""
        try:
            cleaned_data = {}
            
            for date, data in attendance_data.items():
                if AttendanceUtils.validate_date(date):
                    clean_date = AttendanceUtils.clean_date_string(date)
                    cleaned_data[clean_date] = data
                else:
                    print(f"Removed invalid date: '{date}'")
            
            return cleaned_data
            
        except Exception as e:
            print(f"Error cleaning attendance data: {e}")
            return attendance_data
    
    @staticmethod
    def calculate_attendance_stats(attendance_data: Dict[str, Any], students: List[Dict]) -> Dict[str, Any]:
        """Calculate attendance statistics"""
        try:
            valid_dates = [d for d in attendance_data.keys() if AttendanceUtils.validate_date(d)]
            total_classes = len(valid_dates)
            total_students = len(students)
            
            if total_classes == 0 or total_students == 0:
                return {
                    'total_classes': 0,
                    'total_students': 0,
                    'total_present': 0,
                    'attendance_rate': 0.0
                }
            
            total_present = 0
            for date in valid_dates:
                for student in students:
                    if attendance_data[date].get(str(student["id"]), False):
                        total_present += 1
            
            total_possible = total_classes * total_students
            attendance_rate = (total_present / total_possible * 100) if total_possible > 0 else 0
            
            return {
                'total_classes': total_classes,
                'total_students': total_students,
                'total_present': total_present,
                'attendance_rate': round(attendance_rate, 1)
            }
            
        except Exception as e:
            print(f"Error calculating stats: {e}")
            return {
                'total_classes': 0,
                'total_students': 0,
                'total_present': 0,
                'attendance_rate': 0.0
            }
    
    @staticmethod
    def save_attendance_file(group_id: str, attendance_data: Dict[str, Any]) -> bool:
        """Save attendance data to file"""
        try:
            os.makedirs("attendances", exist_ok=True)
            path = f"attendances/attendance_{group_id}.json"
            
            # Clean data before saving
            cleaned_data = AttendanceUtils.clean_attendance_data(attendance_data)
            
            with open(path, "w", encoding="utf-8") as f:
                json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error saving attendance file: {e}")
            return False
    
    @staticmethod
    def load_attendance_file(group_id: str) -> Dict[str, Any]:
        """Load attendance data from file"""
        try:
            path = f"attendances/attendance_{group_id}.json"
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                # Clean data after loading
                return AttendanceUtils.clean_attendance_data(data)
            
            return {}
            
        except Exception as e:
            print(f"Error loading attendance file: {e}")
            return {}

    @staticmethod
    def get_attendance_statistics(attendance_data: Dict[str, Any], students: List[Dict]) -> Dict[str, Any]:
        """Get comprehensive attendance statistics"""
        try:
            # Clean data first
            cleaned_data = AttendanceUtils.clean_attendance_data(attendance_data)
            valid_dates = [d for d in cleaned_data.keys() if AttendanceUtils.validate_date(d)]
            
            total_classes = len(valid_dates)
            total_students = len(students)
            
            if total_classes == 0 or total_students == 0:
                return {
                    'total_classes': 0,
                    'total_students': 0,
                    'total_present': 0,
                    'total_absent': 0,
                    'attendance_rate': 0.0,
                    'absence_rate': 0.0,
                    'student_stats': {}
                }
            
            total_present = 0
            total_absent = 0
            student_stats = {}
            
            # Initialize student stats
            for student in students:
                student_stats[student["id"]] = {
                    'name': student["name"],
                    'present': 0,
                    'absent': 0,
                    'attendance_rate': 0.0
                }
            
            # Calculate stats
            for date in valid_dates:
                date_data = cleaned_data.get(date, {})
                for student in students:
                    student_id = str(student["id"])
                    is_present = date_data.get(student_id, False)
                    
                    if is_present:
                        total_present += 1
                        student_stats[student["id"]]['present'] += 1
                    else:
                        total_absent += 1
                        student_stats[student["id"]]['absent'] += 1
            
            # Calculate rates
            total_possible = total_classes * total_students
            attendance_rate = (total_present / total_possible * 100) if total_possible > 0 else 0
            absence_rate = (total_absent / total_possible * 100) if total_possible > 0 else 0
            
            # Calculate individual student rates
            for student_id in student_stats:
                present = student_stats[student_id]['present']
                student_stats[student_id]['attendance_rate'] = (present / total_classes * 100) if total_classes > 0 else 0
            
            return {
                'total_classes': total_classes,
                'total_students': total_students,
                'total_present': total_present,
                'total_absent': total_absent,
                'attendance_rate': round(attendance_rate, 1),
                'absence_rate': round(absence_rate, 1),
                'student_stats': student_stats
            }
            
        except Exception as e:
            print(f"Error calculating attendance statistics: {e}")
            return {
                'total_classes': 0,
                'total_students': 0,
                'total_present': 0,
                'total_absent': 0,
                'attendance_rate': 0.0,
                'absence_rate': 0.0,
                'student_stats': {}
            }
