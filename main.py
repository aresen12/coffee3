from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QComboBox, QLineEdit, QListWidget, QListWidgetItem, \
    QTableWidget, QTableWidgetItem, QWidget, QSpinBox, QTextEdit
import sys
from PyQt5 import uic
import sqlite3


class Coffee(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        uic.loadUi('main.ui', self)
        self.poisk_btn: QPushButton
        self.tableWidget: QTableWidget
        self.poisk_btn.clicked.connect(self.coffee)
        self.red_btn: QPushButton
        self.red_btn.clicked.connect(self.set_elem)
        self.create_btn: QPushButton
        self.create_btn.clicked.connect(self.new)
        conn = sqlite3.connect('coffee.sqlite')
        curr = conn.cursor()
        res = curr.execute('''SELECT * FROM information''').fetchall()
        conn.close()
        self.tableWidget.setColumnCount(len(res[0]))
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', "название", "Степень обжарки", "Состояние", "описание", "цена", "обьём"])
        self.tableWidget.setRowCount(0)
        for i in range(len(res)):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(res[i]):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.clicked.connect(self.set_elem)

    def coffee(self):
        self.comboBox: QComboBox
        self.poisk: QLineEdit
        self.listWidget: QListWidget
        if self.poisk.text() == "":
            return None
        else:
            text = self.poisk.text()
        bd = sqlite3.connect("coffee.sqlite")
        curr = bd.cursor()
        if self.comboBox.currentText() == 'Объем':
            res = curr.execute(f'''SELECT * FROM information
                                    WHERE volum = {text}''').fetchall()
        elif self.comboBox.currentText() == 'Название':
            res = curr.execute(f'''SELECT * FROM information
                                    WHERE name = "{text}"''').fetchall()
        elif self.comboBox.currentText() == 'Степень обжарки':
            res = curr.execute(f'''SELECT * FROM information
                                    WHERE degree = {text}''').fetchall()
        else:
            res = curr.execute(f'''SELECT * FROM information
                                    WHERE condition = "{text}"''').fetchall()
        bd.close()
        self.listWidget.clear()
        for i in res:
            word = ''
            for elem in range(1, len(i)):
                word += str(i[elem]) + ", "
            self.listWidget.addItem(QListWidgetItem(word))
        if res == list():
            self.listWidget.addItem(QListWidgetItem("Ничего не найденно!"))

    def new(self):
        self.form = Form(is_new=-1)
        self.form.show()

    def set_elem(self):
        self.id: QSpinBox
        conn = sqlite3.connect('coffee.sqlite')
        curr = conn.cursor()
        print(self.id.text())
        res = curr.execute(f'''SELECT * FROM information
        where ID = {int(self.id.text())}''').fetchone()
        conn.close()
        if res is None:
            return None
        print(res)
        self.form = Form(name=res[1], condition=res[3], price=res[5], degree=res[2], volum=res[-1], taste=res[4])
        self.form.show()

    def create_coffee(self):
        self.form.condition: QComboBox
        self.form.name: QLineEdit
        self.form.save_btn: QPushButton
        self.form.price: QLineEdit
        self.form.volum: QLineEdit
        self.form.degree: QLineEdit
        conn = sqlite3.connect("coffee.sqlite")
        curr = conn.cursor()
        curr.execute(
            f'''INSERT INTO information(name, degree, condition, taste, prise, volum) VALUES("{self.form.name.text()}", 
{int(self.form.degree.text())}, '{self.form.condition.currentText()}', "{self.form.taste.toPlainText()}", 
{int(self.form.price.text())}, {int(self.form.volum.text())})''')
        conn.commit()
        conn.close()
        self.form.close()
        self.init_ui()

    def save(self):
        self.id: QSpinBox
        self.form.condition: QComboBox
        self.form.name: QLineEdit
        self.form.save_btn: QPushButton
        self.form.price: QLineEdit
        self.form.volum: QLineEdit
        self.form.degree: QLineEdit
        self.form.taste: QTextEdit
        conn = sqlite3.connect("coffee.sqlite")
        curr = conn.cursor()
        curr.execute(f'''UPDATE information
                        SET name = "{self.form.name.text()}", prise = {int(self.form.price.text())}, 
                        degree = {int(self.form.degree.text())}, condition = '{self.form.condition.currentText()}',
                         volum = {int(self.form.volum.text())}, taste = '{self.form.taste.toPlainText()}'
                        where id = {int(self.id.text())}''')
        conn.commit()
        conn.close()
        self.form.close()
        self.init_ui()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class Form(QWidget):
    def __init__(self, name="", condition=None, degree='0', price='0', volum='0', is_new=None, taste=''):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.condition: QComboBox
        self.name: QLineEdit
        self.save_btn: QPushButton
        self.price: QLineEdit
        self.volum: QLineEdit
        self.name.setText(name)
        self.degree: QLineEdit
        self.degree.setText(str(degree))
        self.volum.setText(str(volum))
        self.name.setText(str(name))
        self.price.setText(str(price))
        self.taste: QTextEdit
        self.taste.setText(str(taste))
        if is_new is None:
            self.save_btn.clicked.connect(ex.save)
        else:
            self.save_btn.clicked.connect(ex.create_coffee)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Coffee()
    sys.excepthook = except_hook
    ex.show()
    sys.exit(app.exec())
