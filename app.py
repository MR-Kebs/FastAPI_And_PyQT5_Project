import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton


class CurrencyConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Конвертер валют без СМС и регистрации")
        self.setMinimumWidth(350)
        self.build_ui()
        self.setStyleSheet("""
        QWidget { background-color: #17181c; }  
        QLabel { color: orange; }              
        QPushButton { background-color: orange; color: black;}             
        QLineEdit { background-color: orange; color: black;}       
        QComboBox { background-color: orange; color: black;}     
        QComboBox QAbstractItemView { background-color: orange; color: black;} 
                           
""")
        
    def build_ui(self):
        layout = QVBoxLayout()


        layout.addWidget(QLabel("Сумма:"))
        self.amount_input = QLineEdit()
        layout.addWidget(self.amount_input)


        currencies = ["USD", "EUR", "RUB", "GBP", "JPY", "CNY"]
        row = QHBoxLayout()




        self.from_box = QComboBox()
        self.from_box.addItems(currencies)
        self.to_box = QComboBox()
        self.to_box.addItems(currencies)
        self.to_box.setCurrentIndex(1)




        row.addWidget(QLabel("Из:"))
        row.addWidget(self.from_box)
        row.addWidget(QLabel("В:"))
        row.addWidget(self.to_box)
        layout.addLayout(row)




        btn = QPushButton("Конвертировать")
        btn.clicked.connect(self.convert)
        layout.addWidget(btn)




        self.result_label = QLabel("")
        layout.addWidget(self.result_label)
        self.setLayout(layout)

    def convert(self):
        amount = self.amount_input.text()
        from_c = self.from_box.currentText()
        to_c = self.to_box.currentText()

        try:
            response = requests.get("http://127.0.0.1:8000/convert", params={
                "from_currency": from_c,
                "to_currency": to_c,
                "amount": amount
            })

            if response.status_code == 200:
                data = response.json()
                self.result_label.setText(
                    f"{data['amount']} {data['from']} = {data['result']} {data['to']}\n"
                    f"Курс: 1 {data['from']} = {data['rate']} {data['to']}"
                )
            else:
                self.result_label.setText(f"Ошибка: {response.json()['detail']}")

        except Exception as e:
            self.result_label.setText(f"Сервер недоступен: {e}")

app = QApplication(sys.argv)
window = CurrencyConverter()
window.show()
sys.exit(app.exec_())