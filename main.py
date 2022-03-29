import numpy as np
import matplotlib.pyplot as plt
import sympy as sym
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap

def fn(x):
    return (x**2+3*x)*np.cos(3*x)

def symbol_integral(xmin, xmax):
    x = sym.symbols('x')
    f = (2*sym.cos(x)+3*sym.sin(x))/(2*sym.sin(x)-3*sym.cos(x))**3
    sym_integral = sym.integrate(f, x)
    print(sym_integral)
    num_integral = sym_integral.evalf(subs={x: xmax}) - sym_integral.evalf(subs={x: xmin})
    return num_integral

def rect_integral(f, xmin, xmax, n):
    dx = (xmax-xmin)/n
    area = 0
    x = xmin
    for i in range(n):
        area += dx*f(x)
        x += dx
    return area

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.acceptDrops()
        self.setWindowTitle("Интегрирование функции")

        self.label1 = QLabel(self)
        self.label2 = QLabel(self)

        self.button = QPushButton("Построение графика", self)
        self.button.clicked.connect(self.btnstate)

        self.lineEd = QLineEdit("0.0001", self)

        self.grid = QGridLayout()
        self.grid.addWidget(self.button, 0, 1)
        self.grid.addWidget(self.lineEd, 0, 0)
        self.grid.addWidget(self.label1, 1, 0)
        self.grid.addWidget(self.label2, 1, 1)

        self.setLayout(self.grid)
        self.show()

    def btnstate(self):
        xmin = -10
        xmax = 10
        n = int((float(abs(xmin)) + float(abs(xmax)))/(float(self.lineEd.text())))
        xarray = np.linspace(xmin, xmax, n)
        yarray = fn(xarray)

        fig1, ax1 = plt.subplots(1)
        ax1.plot(xarray, yarray)
        ax1.grid()
        ax1.set_xlabel('x')
        ax1.set_ylabel('График функции.')
        plt.savefig("f(x).png")
        self.pixmap = QPixmap('f(x).png')
        self.label1.setPixmap(self.pixmap)
        self.label2.setText("Численное решение = {} \n \n Аналитическое решение = {}".format(rect_integral(fn, xmin, xmax, n), symbol_integral(xmin, xmax)))


if __name__=="__main__":

    App = QApplication(sys.argv)

    window = Window()

    sys.exit(App.exec())


