import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from model import *

import model.logist as models
from model.queries import TrifonQueries


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        list_addres = list(set([i.address for i in models.Warehouse.select()])) #проверить, что эти два массива правильно построились
        list_cargo = list(set([i.kind for i in models.Cargo.select()]))

        # print(list_addres)
        # print(list_cargo)

        self.resize(800, 800)
        self.setWindowTitle("Склады и Хранилища")

        self.adding_container_title = QLabel(self)
        self.adding_container_title.move(300, 50)
        self.adding_container_title.setFixedSize(300, 30)
        self.adding_container_title.setText('Добавление контенера')

        self.adding_container_label_capacity = QLabel(self)
        self.adding_container_label_capacity.move(10, 100)
        self.adding_container_label_capacity.setFixedSize(400, 30)
        self.adding_container_label_capacity.setText('Введите вместимость контейнера')

        self.adding_container_input_capacity = QLineEdit('', self)
        self.adding_container_input_capacity.move(300, 100)
        self.adding_container_input_capacity.setFixedSize(300, 30)

        self.adding_container_label_type = QLabel(self)
        self.adding_container_label_type.move(10, 150)
        self.adding_container_label_type.setFixedSize(400, 30)
        self.adding_container_label_type.setText('Выберите тип контейнера')

        self.adding_container_type1 = QRadioButton('drawer', self)
        self.adding_container_type1.move(10, 200)
        self.adding_container_type1.setFixedSize(300, 30)

        self.adding_container_type2 = QRadioButton('barrel', self)
        self.adding_container_type2.move(10, 250)
        self.adding_container_type2.setFixedSize(300, 30)

        self.adding_container_type3 = QRadioButton('container', self)
        self.adding_container_type3.move(10, 300)
        self.adding_container_type3.setFixedSize(300, 30)

        self.adding_container_label_cargo = QLabel(self)
        self.adding_container_label_cargo.move(10, 350)
        self.adding_container_label_cargo.setFixedSize(400, 30)
        self.adding_container_label_cargo.setText('Выберите груз')

        self.adding_container_cargo = QComboBox(self)
        self.adding_container_cargo.move(10, 400)
        self.adding_container_cargo.setFixedSize(400, 30)
        self.adding_container_cargo.addItems(list_cargo)

        self.adding_button = QPushButton('Добавить контейнер', self)
        self.adding_button.move(250, 450)
        self.adding_button.setFixedSize(250, 30)
        self.adding_button.clicked.connect(self.adding)

        self.query_title = QLabel(self)
        self.query_title.move(300, 500)
        self.query_title.setFixedSize(300, 30)
        self.query_title.setText('Содержание нужных складов')

        self.query_input_volume = QPushButton('Введите минимальный объём', self)
        self.query_input_volume.move(10, 550)
        self.query_input_volume.setFixedSize(300, 30)
        self.query_input_volume.clicked.connect(self.get_volume)

        self.query_label_volume = QLabel(self)
        self.query_label_volume.move(400, 550)
        self.query_label_volume.setFixedSize(300, 30)

        self.query_label_adress = QLabel(self)
        self.query_label_adress.move(10, 600)
        self.query_label_adress.setFixedSize(300, 30)
        self.query_label_adress.setText('Выберите страну')

        self.query_addres = QComboBox(self)
        self.query_addres.move(10, 650)
        self.query_addres.setFixedSize(400, 30)
        self.query_addres.addItems(list_addres)

        self.query_button = QPushButton('Найти все подходящие склады', self)
        self.query_button.move(200, 700)
        self.query_button.setFixedSize(350, 30)
        self.query_button.clicked.connect(self.query)

        self.table = QTableView(self)
        self.table.move(40, 750)
        self.table.setFixedSize(600, 250)

        self.init_model()

    def adding(self):
        dict = {}
        try:
            dict['capacity'] = int(self.adding_container_input_capacity.text())
            if (self.adding_container_type1.isChecked()):
                dict['kind'] = 'drawer'
            elif (self.adding_container_type2.isChecked()):
                dict['kind'] = 'barrel'
            elif (self.adding_container_type3.isChecked()):
                dict['kind'] = 'container'
            else:
                1 / 0
            dict['cargo'] = self.adding_container_cargo.currentText()
            models.Container.create ( # проверить, что действительно что-то добавляется в БД
                kind = dict['kind'],
                capacity = dict['capacity'],
                cargo = dict['cargo'],
            )
        except:
            QErrorMessage(self).showMessage('Заполните все поля корректно')

    def get_volume(self):
        text, ok = QInputDialog.getInt(self, 'Минимальный объём', 'Введите минимальный объём:')
        if ok:
            self.query_label_volume.setText('Минимальный объём: ' + str(text))

    def query(self):
        dict = {}
        try:
            dict['capacity'] = int(self.query_label_volume.text()[19:])
            dict['address'] = self.query_addres.currentText()
            myQuery = TrifonQueries.get_mass_cap_kind_by_country_and_volume(dict['address'], dict['capacity']) # проверить правильно ли всё проходит
            print("get_mass_cap_kind_by_country_and_volume", myQuery)
            print("get_mass_cap_kind_by_country_and_volume", list(myQuery))
            self.init_model(myQuery)
        except Exception as e:
            QErrorMessage(self).showMessage('Заполните все поля корректно'+str(e))

    def init_model(self, data=[]):
        self.model = QStandardItemModel(0, 3, self.table) # проверить заполнение таблицы
        self.model.setHeaderData(0, Qt.Horizontal, u"Вид контейнера")
        self.model.setHeaderData(1, Qt.Horizontal, u"Вместимость контейнера")
        self.model.setHeaderData(2, Qt.Horizontal, u"Масса груза")
        self.table.setModel(self.model)
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 200)
        for item in data:
            self.addSightModel(item)

    def addSightModel(self, item):
        self.model.insertRow(0)
        self.model.setData(self.model.index(0, 0), item["kind"])
        self.model.setData(self.model.index(0, 1), item["capacity"])
        self.model.setData(self.model.index(0, 2), item["mass"])

def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
