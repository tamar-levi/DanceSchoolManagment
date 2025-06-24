import json
import os
from datetime import datetime, timedelta

from components.modern_card import ModernCard

class PaymentCalculator:
    def __init__(self):
        self.groups_file_path = "data/groups.json"
        self.students_file_path = "data/students.json" 
        self.joining_dates_file_path = "data/joining_dates.json" 
    
    def load_groups(self):
        try:
            if os.path.exists(self.groups_file_path):
                with open(self.groups_file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("groups", [])
            return []
        except Exception as e:
            print(f"Error loading groups: {e}")
            return []
    
    def load_students(self):
        try:
            if os.path.exists(self.students_file_path):
                with open(self.students_file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("students", {})
            return []
        except Exception as e:
            print(f"Error loading students: {e}")
            return []

    def load_dates(self):
        try:
            if os.path.exists(self.joining_dates_file_path):
                with open(self.joining_dates_file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data
            return []
        except Exception as e:
            print(f"Error loading dates: {e}")
            return []
    
    def get_student_join_date_for_group(self, student_id, group_id):
        try:
            joining_dates = self.load_dates()
            
            group_id_str = str(group_id)  
            
            group_data = joining_dates.get(group_id_str, [])
            
            for student_entry in group_data:
                if str(student_entry.get("student_id")) == str(student_id):
                    join_date = student_entry.get("join_date")
                    return join_date
            
            print(f"DEBUG: No join date found for student {student_id} in group {group_id}")
            return None
            
        except Exception as e:
            print(f"Error getting student join date for group: {e}")
            return None

    def get_student_groups_with_join_dates(self, student_id):
        """Get all groups for student with their join dates"""
        try:
            student = self.get_student_by_id(student_id)
            if not student:
                return []
            
            groups_with_dates = []
            for group_name in student.get("groups", []):
                group_id = self.get_group_id_by_name(group_name)
                if group_id:
                    join_date = self.get_student_join_date_for_group(student_id, group_id)
                    if join_date:
                        groups_with_dates.append({
                            "group_name": group_name,
                            "group_id": group_id,
                            "join_date": join_date
                        })
            
            # Sort by join date
            groups_with_dates.sort(key=lambda x: datetime.strptime(x["join_date"], "%d/%m/%Y"))
            return groups_with_dates
            
        except Exception as e:
            print(f"Error getting student groups with join dates: {e}")
            return []

    def check_if_same_day_multiple_groups(self, groups_with_dates):
        """Check if student joined multiple groups on the same day"""
        if len(groups_with_dates) <= 1:
            return False
        
        date_groups = {}
        for group_info in groups_with_dates:
            join_date = group_info["join_date"]
            if join_date not in date_groups:
                date_groups[join_date] = []
            date_groups[join_date].append(group_info)
        
        for date, groups in date_groups.items():
            if len(groups) > 1:
                return True
        
        return False

    
    def create_discount_periods_for_student(self, student_id, end_date):
        """Create discount periods for student based on group join dates"""
        try:
            groups_with_dates = self.get_student_groups_with_join_dates(student_id)
            if not groups_with_dates:
                return []
            
            groups_with_dates.sort(key=lambda x: datetime.strptime(x["join_date"], "%d/%m/%Y"))
            
            periods = []
            
            if len(groups_with_dates) == 1:
                group_info = groups_with_dates[0]
                periods.append({
                    "start_date": group_info["join_date"],
                    "end_date": end_date.strftime("%d/%m/%Y"),
                    "active_groups": [group_info],
                    "discount_applies": False,
                    "reason": "קבוצה יחידה"
                })
            else:
                # Multiple groups - create periods based on discount rules
                first_group = groups_with_dates[0]
                
                # Check if joined multiple groups on same day
                same_day_multiple = self.check_if_same_day_multiple_groups(groups_with_dates)
                
                if same_day_multiple:
                    # All groups from day 1 with discount
                    periods.append({
                        "start_date": first_group["join_date"],
                        "end_date": end_date.strftime("%d/%m/%Y"),
                        "active_groups": groups_with_dates,
                        "discount_applies": True,
                        "reason": "הצטרפות לכמה קבוצות באותו יום"
                    })
                else:
                    # Different join dates - create separate periods
                    second_group = groups_with_dates[1]
                    second_group_date = datetime.strptime(second_group["join_date"], "%d/%m/%Y")
                    end_of_second_group_month = self.get_end_of_month(second_group_date)
                    
                    # Period 1: First group only (until second group joins)
                    period1_end = (second_group_date - timedelta(days=1)).strftime("%d/%m/%Y")
                    periods.append({
                        "start_date": first_group["join_date"],
                        "end_date": period1_end,
                        "active_groups": [first_group],
                        "discount_applies": False,
                        "reason": "קבוצה ראשונה לבד"
                    })
                    
                    # Period 2: Second group's first month (ONLY the second group, not both!)
                    periods.append({
                        "start_date": second_group["join_date"],
                        "end_date": end_of_second_group_month.strftime("%d/%m/%Y"),
                        "active_groups": [second_group],  # Only the second group!
                        "discount_applies": False,
                        "reason": "חודש ראשון של קבוצה שנייה - רק הקבוצה השנייה"
                    })
                    
                    # Period 3: All groups with discount (from start of next month)
                    if end_of_second_group_month < end_date:
                        discount_start_date = end_of_second_group_month + timedelta(days=1)
                        periods.append({
                            "start_date": discount_start_date.strftime("%d/%m/%Y"),
                            "end_date": end_date.strftime("%d/%m/%Y"),
                            "active_groups": groups_with_dates,
                            "discount_applies": True,
                            "reason": "מתחילת החודש שאחרי הצטרפות לקבוצה שנייה"
                        })
            return periods
            
        except Exception as e:
            print(f"DEBUG: Error creating discount periods: {e}")
            return []


    def calculate_period_payment_with_discount_rules(self, student_id, period):
        """Calculate payment for a specific period with discount rules"""
        try:
            student = self.get_student_by_id(student_id)
            if not student:
                return {"success": False, "error": "Student not found"}
            
            start_date = datetime.strptime(period["start_date"], "%d/%m/%Y")
            end_date = datetime.strptime(period["end_date"], "%d/%m/%Y")
            active_groups = period["active_groups"]
            num_groups = len(active_groups)
            discount_applies = period["discount_applies"]
            has_sister = student.get("has_sister", False)
            
            # Calculate monthly price with discounts
            base_price = 180
            if discount_applies and num_groups > 1:
                monthly_price = self.calculate_multiple_groups_discount(base_price, num_groups)
            else:
                monthly_price = base_price * num_groups
            
            # Apply sister discount
            if has_sister:
                monthly_price = self.calculate_sister_discount(monthly_price, has_sister)
            
            # Calculate time-based payment
            total_months = self.calculate_months_between_dates(start_date, end_date)
            
            if total_months == 0:                
                if num_groups == 1:
                    # Single group - straightforward
                    group_id = active_groups[0]["group_id"]
                    meetings = self.count_meetings_in_date_range(group_id, start_date, end_date)
                else:
                    # Multiple groups - use the group with most meetings in this period
                    max_meetings = 0
                    for group_info in active_groups:
                        group_meetings = self.count_meetings_in_date_range(
                            group_info["group_id"], start_date, end_date
                        )
                        max_meetings = max(max_meetings, group_meetings)
                    meetings = max_meetings
                
                payment = self.calculate_first_month_payment(monthly_price, meetings)
                
                return {
                    "success": True,
                    "period_info": {
                        "start_date": period["start_date"],
                        "end_date": period["end_date"],
                        "num_groups": num_groups,
                        "groups": [g["group_name"] for g in active_groups],
                        "discount_applies": discount_applies,
                        "reason": period.get("reason", "")
                    },
                    "monthly_price": monthly_price,
                    "first_month_meetings": meetings,
                    "first_month_payment": payment,
                    "remaining_months": 0,
                    "remaining_months_payment": 0,
                    "total_payment": round(payment, 2)
                }
            else:
                # Multi-month period
                end_of_first_month = self.get_end_of_month(start_date)
                
                # Count meetings in first month
                if num_groups == 1:
                    group_id = active_groups[0]["group_id"]
                    first_month_meetings = self.count_meetings_in_date_range(
                        group_id, start_date, end_of_first_month
                    )
                else:
                    # Multiple groups - use the group with most meetings
                    max_meetings = 0
                    for group_info in active_groups:
                        group_meetings = self.count_meetings_in_date_range(
                            group_info["group_id"], start_date, end_of_first_month
                        )
                        max_meetings = max(max_meetings, group_meetings)
                    first_month_meetings = max_meetings
                
                first_month_payment = self.calculate_first_month_payment(monthly_price, first_month_meetings)
                
                remaining_months = total_months
                remaining_months_payment = remaining_months * monthly_price
                total_payment = first_month_payment + remaining_months_payment
                
                return {
                    "success": True,
                    "period_info": {
                        "start_date": period["start_date"],
                        "end_date": period["end_date"],
                        "num_groups": num_groups,
                        "groups": [g["group_name"] for g in active_groups],
                        "discount_applies": discount_applies,
                        "reason": period.get("reason", "")
                    },
                    "monthly_price": monthly_price,
                    "first_month_meetings": first_month_meetings,
                    "first_month_payment": first_month_payment,
                    "remaining_months": remaining_months,
                    "remaining_months_payment": remaining_months_payment,
                    "total_payment": round(total_payment, 2)
                }
                
        except Exception as e:
            print(f"DEBUG: Error in calculate_period_payment_with_discount_rules: {e}")
            return {"success": False, "error": str(e)}


    def calculate_student_payment_until_now_with_correct_discounts(self, student_id):
        """Calculate student payment with correct discount timing"""
        try:
            student = self.get_student_by_id(student_id)
            if not student:
                return {
                    "success": False,
                    "error": f"Student with ID {student_id} not found"
                }
            
            current_date = datetime.now()
            end_of_current_month = self.get_end_of_month(current_date)
            
            periods = self.create_discount_periods_for_student(student_id, end_of_current_month)
            if not periods:
                return {
                    "success": False,
                    "error": "No valid periods found for student"
                }
            
            period_payments = []
            total_payment = 0
            
            for i, period in enumerate(periods):
                period_result = self.calculate_period_payment_with_discount_rules(student_id, period)
                if period_result.get("success"):
                    period_payments.append(period_result)
                    total_payment += period_result["total_payment"]
                else:
                    print(f"DEBUG: Period {i+1} failed: {period_result.get('error')}")
            
            return {
                "success": True,
                "student_name": student.get("name", ""),
                "student_id": student_id,
                "calculation_period": f"עד סוף החודש הנוכחי ({end_of_current_month.strftime('%d/%m/%Y')})",
                "periods": period_payments,
                "total_payment": round(total_payment, 2),
                "payment_type": "Multi-period calculation with correct discounts"
            }
            
        except Exception as e:
            print(f"Error in calculate_student_payment_until_now_with_correct_discounts: {e}")
            return {
                "success": False,
                "error": f"Error calculating student payment: {str(e)}"
            }

    def calculate_student_payment_until_now(self, student_id, group_id=None):
        """Updated to use correct discount timing"""
        return self.calculate_student_payment_until_now_with_correct_discounts(student_id)

    def validate_group_id(self, group_id):
        """Validate that group_id is a proper group ID, not a date"""
        try:
            if isinstance(group_id, str) and '/' in group_id:
                try:
                    datetime.strptime(group_id, "%d/%m/%Y")
                    print(f"WARNING: Group ID {group_id} appears to be a date, not a group ID")
                    return False
                except ValueError:
                    pass 
            return True
        except Exception as e:
            print(f"Error validating group ID: {e}")
            return False

    def get_student_by_id(self, student_id):
        students = self.load_students()
        for student in students:
            if student.get("id") == student_id:
                return student
        return None
    
    def calculate_multiple_groups_discount(self, base_price, num_groups):
        if num_groups == 1:
            return base_price
        elif num_groups == 2:
            return 280
        elif num_groups >= 3:
            return 380
        else:
            return base_price
    
    def calculate_sister_discount(self, price, has_sister):
        if has_sister:
            return max(0, price - 20)  
        return price
    
    def calculate_monthly_price_with_discounts(self, student_id, base_price=180):
        try:
            student = self.get_student_by_id(student_id)
            if not student:
                return {
                    "success": False,
                    "error": f"Student with ID {student_id} not found"
                }
            
            groups = student.get("groups", [])
            num_groups = len(groups)
            
            if num_groups == 0:
                return {
                    "success": False,
                    "error": "Student is not enrolled in any groups"
                }
            
            price_after_groups_discount = self.calculate_multiple_groups_discount(base_price, num_groups)
            
            has_sister = student.get("has_sister", False)
            final_price = self.calculate_sister_discount(price_after_groups_discount, has_sister)
            
            return {
                "success": True,
                "student_name": student.get("name", ""),
                "student_id": student_id,
                "num_groups": num_groups,
                "groups": groups,
                "base_price": base_price,
                "price_before_discounts": base_price * num_groups,
                "price_after_groups_discount": price_after_groups_discount,
                "has_sister": has_sister,
                "sister_discount": 20 if has_sister else 0,
                "final_monthly_price": final_price,
                "total_discount": (base_price * num_groups) - final_price
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error calculating monthly price with discounts: {str(e)}"
            }
    
    def get_group_by_id(self, group_id):
        groups = self.load_groups()
        for group in groups:
            if group.get("id") == group_id:
                return group
        return None
    
    def get_group_id_by_name(self, group_name):
        groups = self.load_groups()
        for group in groups:
            if group.get("name") == group_name:
                group_id = group.get("id")
                return group_id
        print(f"DEBUG: Group '{group_name}' not found")
        return None

    def get_end_of_month(self, date):
        if isinstance(date, str):
            date = datetime.strptime(date, "%d/%m/%Y")
        
        if date.month == 12:
            next_month = date.replace(year=date.year + 1, month=1, day=1)
        else:
            next_month = date.replace(month=date.month + 1, day=1)
        
        end_of_month = next_month - timedelta(days=1)
        return end_of_month
    
    def count_meetings_in_date_range(self, group_id, start_date, end_date):
        try:
            group = self.get_group_by_id(group_id)
            if not group:
                print(f"Group with ID {group_id} not found")
                return 0
            
            course_day = group.get("day_of_week")
            if not course_day:
                print(f"Course day not found for group {group_id}")
                return 0
            
            hebrew_days = {
                "ראשון": 6,    # Sunday
                "שני": 0,      # Monday  
                "שלישי": 1,    # Tuesday
                "רביעי": 2,    # Wednesday
                "חמישי": 3,    # Thursday
                "שישי": 4,     # Friday
                "שבת": 5       # Saturday
            }
            
            course_weekday = hebrew_days.get(course_day)
            if course_weekday is None:
                print(f"Invalid course day: {course_day}")
                return 0
            
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, "%d/%m/%Y")
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, "%d/%m/%Y")
            
            meetings_count = 0
            current_date = start_date
            
            while current_date <= end_date:
                if current_date.weekday() == course_weekday:
                    meetings_count += 1
                current_date += timedelta(days=1)
            
            return meetings_count
            
        except Exception as e:
            print(f"Error counting meetings in date range: {e}")
            return 0
    
    def calculate_months_between_dates(self, start_date, end_date):
        try:
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, "%d/%m/%Y")
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, "%d/%m/%Y")
            
            if end_date.day == 1:
                if end_date.month == 1:
                    end_date = end_date.replace(year=end_date.year - 1, month=12, day=31)
                else:
                    previous_month = end_date.month - 1
                    if previous_month in [1, 3, 5, 7, 8, 10, 12]:
                        last_day = 31
                    elif previous_month in [4, 6, 9, 11]:
                        last_day = 30
                    else:  
                        year = end_date.year
                        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                            last_day = 29
                        else:
                            last_day = 28
                    
                    end_date = end_date.replace(month=previous_month, day=last_day)
            
            months_diff = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
            
            if end_date.day < start_date.day:
                months_diff -= 1
            
            return max(0, months_diff)
            
        except Exception as e:
            print(f"Error calculating months between dates: {e}")
            return 0

    def calculate_first_month_payment(self, monthly_price, meetings_attended):
        if meetings_attended >= 3:
            return monthly_price
        else:
            return (monthly_price / 4) * meetings_attended
    
    def _get_student_and_validate(self, student_id):
        student = self.get_student_by_id(student_id)
        if not student:
            return None, {
                "success": False,
                "error": f"Student with ID {student_id} not found"
            }
        
        price_calculation = self.calculate_monthly_price_with_discounts(student_id)
        if not price_calculation.get("success"):
            return None, price_calculation
        
        monthly_price = price_calculation["final_monthly_price"]
        
        return student, {
            "monthly_price": monthly_price,
            "price_details": price_calculation
        }
    
    def _get_group_and_validate(self, group_id):
        group = self.get_group_by_id(group_id)
        if not group:
            return None, {
                "success": False,
                "error": f"Group with ID {group_id} not found"
            }
        
        monthly_price = float(group.get("price", 180))  
        
        return group, {"monthly_price": monthly_price}
    
    def _create_payment_result(self, student_or_group, monthly_price, total_months, first_month_meetings, 
                             first_month_payment, remaining_months, remaining_months_payment,
                             start_date, end_date, payment_type, current_date=None, price_details=None):
        total_payment = first_month_payment + remaining_months_payment
        
        if isinstance(student_or_group, dict) and "name" in student_or_group:
            entity_name = student_or_group.get("name", "")
            entity_type = "student"
        else:
            entity_name = student_or_group.get("name", "") if student_or_group else ""
            entity_type = "group"
        
        result = {
            "success": True,
            "entity_name": entity_name,
            "entity_type": entity_type,
            "monthly_price": monthly_price,
            "total_months": total_months,
            "first_month_meetings": first_month_meetings,
            "first_month_full_price": first_month_meetings >= 3,
            "first_month_payment": round(first_month_payment, 2),
            "remaining_months": remaining_months,
            "remaining_months_payment": remaining_months_payment,
            "total_payment": round(total_payment, 2),
            "start_date": start_date,
            "end_date": end_date,
            "calculation_method": "Full price" if first_month_meetings >= 3 else "Proportional (price/4 * meetings)",
            "payment_type": payment_type
        }
        
        if current_date:
            result["current_date"] = current_date
        
        if price_details:
            result["price_details"] = price_details
            
        return result
        
    def calculate_student_payment_for_period(self, student_id, group_id, start_date, end_date):
        try:
            student, validation_result = self._get_student_and_validate(student_id)
            if not student:
                return validation_result
            
            monthly_price = validation_result["monthly_price"]
            price_details = validation_result["price_details"]
            
            if isinstance(start_date, str):
                start_date_dt = datetime.strptime(start_date, "%d/%m/%Y")
            else:
                start_date_dt = start_date
            
            payment_type = "Full period payment"
            
            total_months = self.calculate_months_between_dates(start_date, end_date)
            
            end_of_first_month = self.get_end_of_month(start_date_dt)
            
            if total_months == 0:
                end_date_dt = datetime.strptime(end_date, "%d/%m/%Y")
                period_meetings = self.count_meetings_in_date_range(
                    group_id, start_date_dt, end_date_dt
                )
                first_month_payment = self.calculate_first_month_payment(monthly_price, period_meetings)
                
                return self._create_payment_result(
                    student, monthly_price, 1, period_meetings, 
                    first_month_payment, 0, 0, start_date, end_date, 
                    payment_type, None, price_details
                )
            
            first_month_meetings = self.count_meetings_in_date_range(
                group_id, start_date_dt, end_of_first_month
            )
            
            first_month_payment = self.calculate_first_month_payment(monthly_price, first_month_meetings)
            
            remaining_months = total_months
            remaining_months_payment = remaining_months * monthly_price
            
            total_months_display = total_months + 1
            
            return self._create_payment_result(
                student, monthly_price, total_months_display, first_month_meetings,
                first_month_payment, remaining_months, remaining_months_payment,
                start_date, end_date, payment_type, None, price_details
            )
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error calculating student payment for period: {str(e)}"
            }
        
    def calculate_payment_until_now(self, group_id, start_date):
        try:
            group, validation_result = self._get_group_and_validate(group_id)
            if not group:
                return validation_result
            
            monthly_price = validation_result["monthly_price"]
            
            if isinstance(start_date, str):
                start_date_dt = datetime.strptime(start_date, "%d/%m/%Y")
            else:
                start_date_dt = start_date
            
            current_date = datetime.now()
            end_of_current_month = self.get_end_of_month(current_date)
            end_date_str = end_of_current_month.strftime("%d/%m/%Y")
            payment_type = "Until current month end"
            current_date_str = current_date.strftime("%d/%m/%Y")
            
            if start_date_dt > current_date:
                return {
                    "success": True,
                    "entity_name": group.get("name", ""),
                    "entity_type": "group",
                    "monthly_price": monthly_price,
                    "total_months": 0,
                    "first_month_meetings": 0,
                    "first_month_payment": 0,
                    "remaining_months": 0,
                    "remaining_months_payment": 0,
                    "total_payment": 0,
                    "start_date": start_date,
                    "current_date": current_date_str,
                    "end_date": end_date_str,
                    "calculation_method": "Course hasn't started yet",
                    "payment_type": payment_type
                }
            
            total_months = self.calculate_months_between_dates(start_date, end_date_str)
            
            end_of_first_month = self.get_end_of_month(start_date_dt)
            
            if total_months == 0:
                current_month_meetings = self.count_meetings_in_date_range(
                    group_id, start_date_dt, end_of_current_month
                )
                first_month_payment = self.calculate_first_month_payment(monthly_price, current_month_meetings)
                
                return self._create_payment_result(
                    group, monthly_price, 1, current_month_meetings, 
                    first_month_payment, 0, 0, start_date, end_date_str, 
                    payment_type, current_date_str
                )
            
            first_month_meetings = self.count_meetings_in_date_range(
                group_id, start_date_dt, end_of_first_month
            )
            
            first_month_payment = self.calculate_first_month_payment(monthly_price, first_month_meetings)
            
            remaining_months = total_months
            total_months_display = total_months + 1  
            remaining_months_payment = remaining_months * monthly_price
            
            return self._create_payment_result(
                group, monthly_price, total_months_display, first_month_meetings,
                first_month_payment, remaining_months, remaining_months_payment,
                start_date, end_date_str, payment_type, current_date_str
            )
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error calculating payment until now: {str(e)}"
            }
    
    def calculate_payment_for_period(self, group_id, start_date, end_date):
        try:
            group, validation_result = self._get_group_and_validate(group_id)
            if not group:
                return validation_result
            
            monthly_price = validation_result["monthly_price"]
            
            if isinstance(start_date, str):
                start_date_dt = datetime.strptime(start_date, "%d/%m/%Y")
            else:
                start_date_dt = start_date
            
            payment_type = "Full period payment"
            
            total_months = self.calculate_months_between_dates(start_date, end_date)
            
            end_of_first_month = self.get_end_of_month(start_date_dt)
            
            if total_months == 0:
                end_date_dt = datetime.strptime(end_date, "%d/%m/%Y")
                period_meetings = self.count_meetings_in_date_range(
                    group_id, start_date_dt, end_date_dt
                )
                first_month_payment = self.calculate_first_month_payment(monthly_price, period_meetings)
                
                return self._create_payment_result(
                    group, monthly_price, 1, period_meetings, 
                    first_month_payment, 0, 0, start_date, end_date, 
                    payment_type
                )
            
            first_month_meetings = self.count_meetings_in_date_range(
                group_id, start_date_dt, end_of_first_month
            )
            
            first_month_payment = self.calculate_first_month_payment(monthly_price, first_month_meetings)
            
            remaining_months = total_months
            remaining_months_payment = remaining_months * monthly_price
            
            total_months_display = total_months + 1
            
            return self._create_payment_result(
                group, monthly_price, total_months_display, first_month_meetings,
                first_month_payment, remaining_months, remaining_months_payment,
                start_date, end_date, payment_type
            )
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error calculating payment for period: {str(e)}"
            }
    
    def get_student_payment_amount_until_now(self, student_id, group_id=None):
        result = self.calculate_student_payment_until_now(student_id, group_id)
        if result.get("success"):
            return result["total_payment"]
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
            return 0

    def get_student_payment_amount_for_period(self, student_id, group_id, start_date, end_date):
        result = self.calculate_student_payment_for_period(student_id, group_id, start_date, end_date)
        if result.get("success"):
            return result["total_payment"]
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
            return 0
        
    def get_payment_amount_until_now(self, group_id, start_date):
        result = self.calculate_payment_until_now(group_id, start_date)
        if result.get("success"):
            return result["total_payment"]
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
            return 0
    
    def get_payment_amount_for_period(self, group_id, start_date, end_date):
        result = self.calculate_payment_for_period(group_id, start_date, end_date)
        if result.get("success"):
            return result["total_payment"]
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
            return 0

    def calculate_payment(self, group_id, start_date, end_date=None):
        if end_date is None:
            return self.calculate_payment_until_now(group_id, start_date)
        else:
            return self.calculate_payment_for_period(group_id, start_date, end_date)
    
    def calculate_student_payment(self, student_id, group_id=None, start_date=None, end_date=None):
        if start_date is None:
            student = self.get_student_by_id(student_id)
            if not student:
                return {
                    "success": False,
                    "error": f"Student with ID {student_id} not found"
                }
            
            student_groups = student.get("groups", [])
            if not student_groups:
                return {
                    "success": False,
                    "error": "Student is not enrolled in any groups"
                }
            
            if group_id is None:
                first_group_name = student_groups[0]
                group_id = self.get_group_id_by_name(first_group_name)
            
            start_date = self.get_student_join_date_for_group(student_id, group_id)
            if not start_date:
                return {
                    "success": False,
                    "error": f"Join date not found for student {student_id} in group {group_id}"
                }
        
        if end_date is None:
            return self.calculate_student_payment_until_now(student_id, group_id)
        else:
            return self.calculate_student_payment_for_period(student_id, group_id, start_date, end_date)

    def get_all_students_payment_summary(self):
        try:
            students = self.load_students()
            summary = []
            
            for student in students:
                student_id = student.get("id")
                if not student_id:
                    continue
                
                price_calc = self.calculate_monthly_price_with_discounts(student_id)
                if price_calc.get("success"):
                    summary.append({
                        "student_id": student_id,
                        "student_name": student.get("name", ""),
                        "groups": student.get("groups", []),
                        "has_sister": student.get("has_sister", False),
                        "join_date": student.get("join_date", ""),
                        "payment_status": student.get("payment_status", ""),
                        "monthly_price": price_calc["final_monthly_price"],
                        "num_groups": price_calc["num_groups"],
                        "total_discount": price_calc["total_discount"],
                        "price_breakdown": {
                            "base_price_per_group": price_calc["base_price"],
                            "price_before_discounts": price_calc["price_before_discounts"],
                            "groups_discount": price_calc["price_before_discounts"] - price_calc["price_after_groups_discount"],
                            "sister_discount": price_calc["sister_discount"],
                            "final_price": price_calc["final_monthly_price"]
                        }
                    })
            
            return summary
            
        except Exception as e:
            print(f"Error getting students payment summary: {e}")
            return []
    
    def update_student_groups(self, student_id, new_groups):
        try:
            students = self.load_students()
            student_found = False
            
            for student in students:
                if student.get("id") == student_id:
                    student["groups"] = new_groups
                    student_found = True
                    break
            
            if not student_found:
                return {
                    "success": False,
                    "error": f"Student with ID {student_id} not found"
                }
            
            with open(self.students_file_path, "w", encoding="utf-8") as f:
                json.dump({"students": students}, f, ensure_ascii=False, indent=2)
            
            return self.calculate_monthly_price_with_discounts(student_id)
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error updating student groups: {str(e)}"
            }
    
    def update_student_sister_status(self, student_id, has_sister):
        try:
            students = self.load_students()
            student_found = False
            
            for student in students:
                if student.get("id") == student_id:
                    student["has_sister"] = has_sister
                    student_found = True
                    break
            
            if not student_found:
                return {
                    "success": False,
                    "error": f"Student with ID {student_id} not found"
                }
            
            with open(self.students_file_path, "w", encoding="utf-8") as f:
                json.dump({"students": students}, f, ensure_ascii=False, indent=2)
            
            return self.calculate_monthly_price_with_discounts(student_id)
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error updating student sister status: {str(e)}"
            }

    def get_student_payment_explanation(self, student_id, group_id=None, start_date=None, end_date=None):
        try:
            student = self.get_student_by_id(student_id)
            if not student:
                return {
                    "success": False,
                    "error": f"תלמידה עם מזהה {student_id} לא נמצאה"
                }
            
            payment_result = self.calculate_student_payment_until_now_with_correct_discounts(student_id)
            
            if not payment_result.get("success"):
                print(f"DEBUG: payment_result failed: {payment_result}")
                return payment_result
            
            payments = student.get('payments', [])
            total_paid = 0
            payment_details = []
            
            for payment in payments:
                try:
                    amount = payment.get('amount', 0)
                    if isinstance(amount, str):
                        amount = float(amount) if amount.strip() else 0
                    elif isinstance(amount, (int, float)):
                        amount = float(amount)
                    else:
                        amount = 0
                    
                    if amount > 0:
                        total_paid += amount
                        payment_details.append({
                            "amount": amount,
                            "date": payment.get('date', ''),
                            "method": payment.get('payment_method', '')
                        })
                except (ValueError, AttributeError):
                    continue
            
            total_required = payment_result.get("total_payment", 0)
            total_course_payment = 0
            course_end_info = ""
            
            try:
                groups_with_dates = self.get_student_groups_with_join_dates(student_id)
                if groups_with_dates:
                    latest_end_date = ""
                    for group_info in groups_with_dates:
                        group = self.get_group_by_id(group_info["group_id"])
                        if group:
                            group_end_date = group.get("group_end_date", "")
                            if group_end_date > latest_end_date:
                                latest_end_date = group_end_date
                    
                    if latest_end_date:
                        course_periods = self.create_discount_periods_for_student(
                            student_id, 
                            datetime.strptime(latest_end_date, "%d/%m/%Y")
                        )
                        
                        for period in course_periods:
                            period_result = self.calculate_period_payment_with_discount_rules(student_id, period)
                            if period_result.get("success"):
                                total_course_payment += period_result["total_payment"]
                        
                        course_end_info = f" (עד {latest_end_date})"
            except Exception as e:
                print(f"DEBUG: Error calculating total course payment: {e}")
            
            explanation = {
                "success": True,
                "student_name": student.get("name", ""),
                "student_id": student_id,
                "calculation_period": payment_result.get("calculation_period", ""),
                "groups": student.get("groups", []),
                "num_groups": len(student.get("groups", [])),
                "has_sister": student.get("has_sister", False),
                "periods": payment_result.get("periods", []),
                "total_required": total_required,
                "total_course_payment": total_course_payment,
                "course_end_info": course_end_info,
                "payments_made": {
                    "total_paid": total_paid,
                    "payment_details": payment_details,
                    "balance": total_required - total_paid
                }
            }
            
            try:
                explanation["summary"] = self._create_payment_summary_with_correct_discounts(explanation)
            except Exception as summary_error:
                print(f"DEBUG: Error creating summary: {summary_error}")
                import traceback
                traceback.print_exc()
                explanation["summary"] = f"שגיאה ביצירת הסיכום: {str(summary_error)}"
            
            return explanation
            
        except Exception as e:
            print(f"DEBUG: Error in get_student_payment_explanation: {e}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": f"שגיאה בחישוב הסבר התשלום: {str(e)}"
            }


    def _create_payment_summary_with_correct_discounts(self, explanation):
        """Create a detailed payment summary explanation with correct discount timing"""
        try:
            student_name = explanation.get("student_name", "")
            groups = explanation.get("groups", [])
            has_sister = explanation.get("has_sister", False)
            period = explanation.get("calculation_period", "")
            student_id = explanation.get("student_id", "")
            periods = explanation.get("periods", [])
            total_required = explanation.get("total_required", 0)
            total_course_payment = explanation.get("total_course_payment", 0)
            course_end_info = explanation.get("course_end_info", "")
            
            payments_made = explanation.get("payments_made", {})
            total_paid = payments_made.get("total_paid", 0)
            balance = payments_made.get("balance", 0)
            
            summary_lines = [
                f"חישוב תשלום מפורט עבור {student_name}",
                f"תקופת החישוב: {period}",
                "",
                ":פירוט תקופות התשלום",
                "─" * 40,
            ]
            
            for i, period_data in enumerate(periods, 1):
                period_info = period_data.get("period_info", {})
                start_date = period_info.get("start_date", "")
                end_date = period_info.get("end_date", "")
                num_groups = period_info.get("num_groups", 0)
                period_groups = period_info.get("groups", [])
                monthly_price = period_data.get("monthly_price", 0)
                total_payment = period_data.get("total_payment", 0)
                discount_applies = period_info.get("discount_applies", False)
                reason = period_info.get("reason", "")
                
                summary_lines.append(f"תקופה {i}: {start_date} - {end_date}")
                summary_lines.append(f"  קבוצות: {', '.join(period_groups)} ({num_groups} קבוצות)")
                
                base_price = 180
                base_total = base_price * num_groups
                summary_lines.append(f"  מחיר בסיס: {base_total}₪ ({base_price}₪ × {num_groups})")
                
                if num_groups > 1:
                    if discount_applies:
                        groups_discount = base_total - monthly_price
                        if has_sister:
                            groups_discount -= 20  
                        summary_lines.append(f"  הנחת קבוצות מרובות: -{groups_discount}₪")
                        summary_lines.append(f"  ההנחה חלה כי: {reason}")
                    else:
                        summary_lines.append(f"  ללא הנחת קבוצות - {reason}")
                
                if has_sister:
                    summary_lines.append(f"  הנחת אחיות: -20₪")
                
                summary_lines.append(f"  מחיר חודשי סופי: {monthly_price}₪")
                
                first_month_meetings = period_data.get("first_month_meetings", 0)
                remaining_months = period_data.get("remaining_months", 0)
                
                if remaining_months == 0:
                    summary_lines.append(f"  מספר מפגשים: {first_month_meetings}")
                    if first_month_meetings < 3:
                        calculation = round((monthly_price / 4) * first_month_meetings, 2)
                        summary_lines.append(f"  חישוב: {monthly_price}₪ ÷ 4 × {first_month_meetings} = {calculation}₪")
                    else:
                        summary_lines.append(f"  תשלום מלא (3+ מפגשים): {monthly_price}₪")
                else:
                    first_month_payment = period_data.get("first_month_payment", 0)
                    remaining_payment = period_data.get("remaining_months_payment", 0)
                    summary_lines.append(f"  חודש ראשון: {first_month_meetings} מפגשים = {first_month_payment}₪")
                    summary_lines.append(f"  חודשים נוספים: {remaining_months} × {monthly_price}₪ = {remaining_payment}₪")
                
                summary_lines.append(f"  סה\"כ לתקופה: {total_payment}₪")
                summary_lines.append("")
            
            summary_lines.extend([
                ":סיכום התשלום",
                "─" * 40,
                f"סה\"כ נדרש עד כה: {total_required}₪",
            ])
            
            if total_course_payment > 0:
                summary_lines.append(f"סה\"כ לכל הקורס{course_end_info}: {total_course_payment}₪")
            
            summary_lines.extend([
                "",
                ":מצב תשלומים נוכחי",
                "─" * 40,
                f"שולם עד כה: {total_paid}₪",
            ])
            
            if balance > 0:
                summary_lines.append(f"יתרת חוב עד כה: {balance}₪")
            elif balance == 0:
                summary_lines.append("סטטוס עד כה: שולם במלואו ✓")
                
                if total_course_payment > total_required:
                    remaining_for_course = total_course_payment - total_paid
                    if remaining_for_course > 0:
                        summary_lines.append(f"נותר לשלם עד סוף הקורס: {remaining_for_course}₪")
                    else:
                        summary_lines.append("שולם גם לכל הקורס! ✓")
                else:
                    summary_lines.append("התשלום מושלם ✓")
            else:
                overpaid_amount = abs(balance)
                summary_lines.append(f"שילם יותר מהנדרש עד כה: +{overpaid_amount}₪")
                
                if total_course_payment > 0:
                    total_course_balance = total_course_payment - total_paid
                    
                    if total_course_balance > 0:
                        summary_lines.append(f"נותר לשלם עד סוף הקורס: {total_course_balance}₪")
                        summary_lines.append("סטטוס: שילם מראש חלק מהתשלומים הבאים")
                    elif total_course_balance == 0:
                        summary_lines.append("שילם את כל הקורס במלואו! ✓")
                    else:
                        summary_lines.append(f"שילם יתר על כל הקורס: {abs(total_course_balance)}₪")
                        summary_lines.append("ניתן להחזיר את העודף או לזכות לקורס הבא")
                else:
                    summary_lines.append("סטטוס: שילם מראש")
            
            return "\n".join(summary_lines)
            
        except Exception as e:
            print(f"DEBUG: Error in _create_payment_summary_with_correct_discounts: {e}")
            return f"שגיאה ביצירת הסיכום: {str(e)}"

    def _create_payment_summary_with_periods(self, explanation):
        """Legacy method - redirects to new correct discount summary"""
        return self._create_payment_summary_with_correct_discounts(explanation)

    def _create_payment_summary(self, explanation):
        """Legacy method - redirects to new correct discount summary"""
        return self._create_payment_summary_with_correct_discounts(explanation)
    
    def _create_short_summary(self, explanation):
        """Create a short summary for the card"""
        try:
            groups = explanation.get("groups", [])
            num_groups = explanation.get("num_groups", 0)
            has_sister = explanation.get("has_sister", False)
            
            total_required = explanation.get("total_required", 0)
            payments_made = explanation.get("payments_made", {})
            total_paid = payments_made.get("total_paid", 0)
            balance = payments_made.get("balance", 0)
            
            print(f"DEBUG: _create_short_summary - total_required: {total_required}")
            print(f"DEBUG: _create_short_summary - total_paid: {total_paid}")
            print(f"DEBUG: _create_short_summary - balance: {balance}")
            
            lines = []
            
            current_monthly_price = 0
            discount_status = ""
            
            periods = explanation.get("periods", [])
            print(f"DEBUG: _create_short_summary - periods count: {len(periods)}")
            
            if periods:
                current_period = periods[-1]
                current_monthly_price = current_period.get("monthly_price", 0)
                period_info = current_period.get("period_info", {})
                discount_applies = period_info.get("discount_applies", False)
                
                print(f"DEBUG: Current period monthly price: {current_monthly_price}")
                print(f"DEBUG: Discount applies: {discount_applies}")
                
                if num_groups > 1:
                    if discount_applies:
                        discount_status = "עם הנחה"
                    else:
                        discount_status = "ללא הנחה עדיין"
                else:
                    discount_status = "קבוצה אחת"
            else:
                print("DEBUG: No periods found, using fallback calculation")
                base_price = 180
                current_monthly_price = base_price * num_groups
                
                if num_groups > 1:
                    current_monthly_price = 280 if num_groups == 2 else 380
                    discount_status = "עם הנחה"
                
                if has_sister:
                    current_monthly_price = max(0, current_monthly_price - 20)
            
            if has_sister and periods:
                pass
            elif has_sister and not periods:
                current_monthly_price = max(0, current_monthly_price - 20)
            
            price_line = f"מחיר חודשי נוכחי: {current_monthly_price}₪"
            if num_groups > 1:
                price_line += f" ({num_groups} קבוצות"
                if discount_status:
                    price_line += f" - {discount_status}"
                price_line += ")"
            if has_sister:
                price_line += " + הנחת אחיות"
            
            lines.append(price_line)
            lines.append(f"סה\"כ נדרש עד כה: {total_required}₪")
            lines.append(f"שולם: {total_paid}₪")
            
            if balance > 0:
                lines.append(f"יתרת חוב: {balance}₪")
            elif balance == 0:
                lines.append("סטטוס: שולם במלואו ✓")
            else:
                lines.append(f"שילם יתר: +{abs(balance)}₪")
            
            return "\n".join(lines)
            
        except Exception as e:
            print(f"DEBUG: Error in _create_short_summary: {e}")
            import traceback
            traceback.print_exc()
            return "שגיאה בהצגת סיכום התשלום"

    