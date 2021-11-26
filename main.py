import sys
import datetime
import pandas as pd
import math
import statistics
from PyQt5 import QtWidgets
from forming_GRP import Ui_GRP



app = QtWidgets.QApplication(sys.argv)
GRP = QtWidgets.QWidget()
ui = Ui_GRP()
ui.setupUi(GRP)
GRP.show()


class Inpxlsx():

    def inp_first_file(self):
        global final_data_1
        name1 = ui.lineEdit.text()
        final_data_1 = pd.read_excel(name1)
        print(name1,final_data_1.shape)

    ui.pushButton.clicked.connect(inp_first_file)

    def inp_second_file(self):
        global final_data_2
        name2 = ui.lineEdit_2.text()
        final_data_2 = pd.read_excel(name2)
        print(name2,final_data_2.shape)

    ui.pushButton_2.clicked.connect(inp_second_file)

    def inp_third_file(self):
        global final_data_3
        name3 = ui.lineEdit_3.text()
        final_data_3 = pd.read_excel(name3)
        print(name3,final_data_3.shape)

    ui.pushButton_3.clicked.connect(inp_third_file)

    def process(self):
        global final_data_1, final_data_2, final_data_3







sys.exit(app.exec_())


