import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QStackedWidget, QHBoxLayout
from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint
from PyQt5.QtGui import QIcon
from add_student_page import AddStudentPage
from groups_page import GroupsPage
from attendance_page import AttendancePage
from payment_page import PaymentPage
from PyQt5.QtCore import QSize

def set_button_style(btn):
    btn.setStyleSheet("""
        background-color: #f48fb1;
        color: white;
        font-size: 16px;
        padding: 12px;
        border-radius: 12px;
        border: none;
        transition: all 0.3s ease;
    """)
    btn.setIconSize(QSize(30, 30))
    btn.setFixedHeight(50)

    animation = QPropertyAnimation(btn, b"pos")
    animation.setDuration(1000)
    animation.setStartValue(QPoint(0, 0))
    animation.setEndValue(QPoint(200, 0))

    btn.clicked.connect(animation.start)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('זה הריקוד שלך')
        self.setGeometry(100, 100, 500, 350)

        self.stack = QStackedWidget(self)

        self.home_page = self.create_home_page()
        self.groups_page = GroupsPage(self.stack)
        self.attendance_page = AttendancePage(self.stack)
        self.payment_page = PaymentPage(self.stack)
        self.add_student_page = AddStudentPage(self.stack)

        self.stack.addWidget(self.home_page)         # index 0
        self.stack.addWidget(self.groups_page)      # index 1
        self.stack.addWidget(self.attendance_page)   # index 2
        self.stack.addWidget(self.payment_page)      # index 3
        self.stack.addWidget(self.add_student_page)  # index 4

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)

    def create_home_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        label = QLabel('זה הריקוד שלך, הבית המקצועי לבלט')
        label.setStyleSheet("font-size: 24px; color: #d81b60; font-weight: bold;")
        layout.addWidget(label, alignment=Qt.AlignCenter)

        btn1 = QPushButton('הצגת קבוצות והוספת תלמידות')
        btn2 = QPushButton('נוכחות')
        btn3 = QPushButton('תשלומים')

        btn1.setIcon(QIcon.fromTheme("user-group"))
        btn2.setIcon(QIcon.fromTheme("checkmark"))
        btn3.setIcon(QIcon.fromTheme("credit-card"))

        set_button_style(btn1)
        set_button_style(btn2)
        set_button_style(btn3)

        for i, btn in enumerate((btn1, btn2, btn3), start=1):
            btn: QPushButton
            btn.clicked.connect(lambda _, x=i: self.stack.setCurrentIndex(x))

        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addWidget(btn3)

        page.setLayout(layout)
        return page

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
