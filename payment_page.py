# payment_page.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton

class PaymentPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.addWidget(QLabel("עמוד תשלומים"))

        back_btn: QPushButton  = QPushButton("חזרה לעמוד הראשי")
        back_btn.clicked.connect(self.go_home)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def go_home(self):
        self.stacked_widget.setCurrentIndex(0)
