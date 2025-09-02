import json
from typing import List, Dict, Any
from utils.date_utils import DateUtils
from utils.manage_json import ManageJSON

class StudentsDataManager:
    """Manager for students data operations"""
    
    def __init__(self):
        data_dir = ManageJSON.get_appdata_path() / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        
        self.students_file = data_dir / "students.json"
        self.groups_file = data_dir / "groups.json"


    def load_students(self):
        """Load students from JSON file"""
        try:
            with open(self.students_file, encoding="utf-8") as f:
                data = json.load(f)
                return data.get("students", [])
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Error loading students: {e}")
            return []
        
    def get_students_stats(self, students: List[Dict[str, Any]]) -> Dict[str, int]:
        """Calculate students statistics"""
        total_students = len(students)
        paid_students = len([s for s in students if s.get("payment_status") == "שולם"])
        unpaid_students = total_students - paid_students
        
        return {
            "total": total_students,
            "paid": paid_students,
            "unpaid": unpaid_students
        }
    
    def filter_students(self, students: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """Filter students based on search query"""
        if not query:
            return students.copy()
        
        query_lower = query.lower()
        return [
            student for student in students
            if query_lower in json.dumps(student, ensure_ascii=False).lower()
        ]

    def get_all_students(self):
        """Get all students"""
        try:
            with open(self.students_file, encoding="utf-8") as f:
                return json.load(f).get("students", [])
        except Exception as e:
            print(f"Error loading students: {e}")
            return []

    def get_students_by_group(self, group_name):
        """Get students filtered by group"""
        students = self.get_all_students()
        return [s for s in students if group_name in s.get("groups", [])]

    def save_students(self, students):
        """Save students to file"""
        try:
            with open(self.students_file, 'w', encoding="utf-8") as f:
                json.dump({"students": students}, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Error saving students: {e}")
            return False

    def load_groups(self):
        """Load groups from JSON file"""
        try:
            with open(self.groups_file, encoding="utf-8") as f:
                data = json.load(f)
                return data.get("groups", [])
        except Exception as e:
            print(f"Error loading groups: {e}")
            return []
    
    def update_student(self, student_id, new_data):
        """Update a specific student by ID"""
        try:
            students = self.get_all_students()
            
            updated = False
            for i, student in enumerate(students):
                if student['id'] == student_id:
                    students[i] = new_data
                    updated = True
                    break
            
            if updated:
                success = self.save_students(students)
                return success
            else:
                return False
                
        except Exception as e:
            print(f"Error in update_student: {e}")
            return False


    def add_student(self, student_data):
        """Add new student or add group to existing student"""
        students = self.load_students()
        student_id = student_data.get("id")
        new_group = student_data.get("group")
        
        existing_student = None
        for i, student in enumerate(students):
            if student.get("id") == student_id:
                existing_student = i
                break
        
        if existing_student is not None:
            if "groups" not in students[existing_student]:
                old_group = students[existing_student].get("group")
                students[existing_student]["groups"] = [old_group] if old_group else []
                if "group" in students[existing_student]:
                    del students[existing_student]["group"]
            
            if new_group and new_group not in students[existing_student]["groups"]:
                students[existing_student]["groups"].append(new_group)
        else:
            if "group" in student_data:
                student_data["groups"] = [student_data["group"]]
                del student_data["group"]
            elif "groups" not in student_data:
                student_data["groups"] = []
            
            students.append(student_data)
        
        return self.save_students(students)
    
    def student_exists(self, student_id):
        """Check if student with given ID exists"""
        students = self.load_students()
        return any(student.get("id") == student_id for student in students)
    
    def student_exists_in_this_group(self, student_id, group_name):
        """Check if student with given ID exists in specific group"""
        students = self.load_students()
        return any(
            student.get("id") == student_id and 
            group_name in student.get("groups", [])
            for student in students
        )
    
    def delete_student_attendance(self, student_id, group_name):
        """Delete student attendance from group attendance file"""
        try:
            groups = self.load_groups()
            group_id = None
            
            for group in groups:
                if group.get("name") == group_name:
                    group_id = group.get("id")
                    break
            
            if not group_id:
                print(f"Group '{group_name}' not found")
                return False
            
            attendances_dir = ManageJSON.get_appdata_path() / "attendances"
            attendance_file = attendances_dir / f"attendance_{group_id}.json"
            
            if not attendance_file.exists():
                print(f"Attendance file {attendance_file} not found")
                return True  
            
            with open(attendance_file, 'r', encoding="utf-8") as f:
                attendance_data = json.load(f)
            
            updated = False
            for date in attendance_data:
                if student_id in attendance_data[date]:
                    del attendance_data[date][student_id]
                    updated = True
            
            if updated:
                with open(attendance_file, 'w', encoding="utf-8") as f:
                    json.dump(attendance_data, f, ensure_ascii=False, indent=2)
                print(f"Deleted attendance for student {student_id} from group {group_name}")
            
            return True
            
        except Exception as e:
            print(f"Error deleting student attendance: {e}")
            return False
    
    def delete_student_from_group(self, student_id, group_name):
        """Delete a student from specific group or completely if it's the last group"""
        try:
            students = self.get_all_students()
            updated = False
            
            for i, student in enumerate(students):
                if student['id'] == student_id:
                    if "group" in student and "groups" not in student:
                        student["groups"] = [student["group"]]
                        del student["group"]
                    
                    groups = student.get("groups", [])
                    
                    if group_name in groups:
                        groups.remove(group_name)
                        
                        self.delete_student_attendance(student_id, group_name)
                        
                        if len(groups) == 0:
                            students.pop(i)
                        else:
                            students[i]["groups"] = groups
                        
                        updated = True
                        break
            
            if updated:
                success = self.save_students(students)
                return success
            else:
                print("Student not found in specified group")
                return False
                
        except Exception as e:
            print(f"Error in delete_student_from_group: {e}")
            return False

    def delete_student(self, student_name):
        """Delete a student completely from all groups"""
        try:
            students = self.get_all_students()
            student_exists = any(s['name'] == student_name for s in students)
            print(f"Student exists: {student_exists}")
            updated_students = [s for s in students if s['name'] != student_name]
            success = self.save_students(updated_students)
            return success
            
        except Exception as e:
            print(f"Error in delete_student: {e}")
            return False

    def add_payment(self, student_id, payment_data):
        """Add payment to student and update payment status"""
        from .payment_utils import PaymentCalculator 
        
        students = self.get_all_students()
        payment_calculator = PaymentCalculator() 
        
        for student in students:
            if student['id'] == student_id:
                student.setdefault("payments", []).append(payment_data)
                
                total_paid = sum(
                    float(p['amount']) for p in student['payments']
                    if p['amount'].replace('.', '', 1).isdigit()
                )
                
                student_groups = student.get("groups", [])
                join_date = DateUtils.get_join_date_by_id(student.get("id"))
                
                total_owed = 0
                for group_name in student_groups:
                    groups = payment_calculator.load_groups()
                    group = next((g for g in groups if g['name'] == group_name), None)
                    
                    if group:
                        group_id = group.get("id")
                        group_end_date = group.get("group_end_date", "")
                        
                        if group_id and group_end_date:
                            group_payment = payment_calculator.get_payment_amount_for_period(
                                group_id, join_date, group_end_date
                            )
                            total_owed += group_payment
                
                if total_owed > 0:
                    if total_paid >= total_owed:
                        student['payment_status'] = "שולם"
                    else:
                        student['payment_status'] = f"חוב"
                else:
                    student['payment_status'] = "לא נמצא מחיר קבוצות"
                break
        
        return self.save_students(students)



    def _get_groups(self):
        """Get groups data for pricing"""
        try:
            with open(self.groups_file, encoding="utf-8") as f:
                return json.load(f).get("groups", [])
        except Exception as e:
            print(f"Error loading groups: {e}")
            return []

    def migrate_old_format(self):
        """Migrate old format (single group) to new format (groups array)"""
        try:
            students = self.get_all_students()
            updated = False
            
            for student in students:
                if "group" in student and "groups" not in student:
                    old_group = student["group"]
                    student["groups"] = [old_group] if old_group else []
                    del student["group"]
                    updated = True
            
            if updated:
                return self.save_students(students)
            return True
            
        except Exception as e:
            print(f"Error in migrate_old_format: {e}")
            return False
