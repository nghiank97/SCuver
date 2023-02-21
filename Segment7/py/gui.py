
from cProfile import label
import sys
from tracemalloc import start
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtGui,QtCore,QtWidgets
from PyQt5.QtGui import QDoubleValidator

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PyQt5.QtOpenGL import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class Segment7:
    def __init__(self,*args,**kwargs):
        self.Amax = kwargs['A']
        self.Vmax = kwargs['V']
        self.Jmax = kwargs['J']
        self.index = kwargs['t']

        self.q0 = 0
        self.qf = 0

        self.T = 0
        self.t1 = 0
        self.t3 = 0
        self.t2 = 0
        self.t4 = 0
        self.t5 = 0
        self.t6 = 0

        self.position = 0
        self.velocity = 0
        self.acceleration = 0
        self.t = 0
        self.finish = 0
        self.delta_q = 0
        self.sign = 1

        

    def get_data(self,t):
        if 0<=t and t<= self.t1:
            self.position = t*t*t*self.a1/6 + t*t*self.b1/2 + t*self.c1 +self.d1
            self.velocity = t*t*self.a1/2 + t*self.b1 + self.c1
            self.acceleration = t*self.a1 + self.b1

        elif self.t1<t and t<= self.t2:
            self.position = t*t*t*self.a2/6 + t*t*self.b2/2 + t*self.c2 +self.d2
            self.velocity = t*t*self.a2/2 + t*self.b2 + self.c2
            self.acceleration = t*self.a2 + self.b2

        elif self.t2<t and t<= self.t3:
            self.position = t*t*t*self.a3/6 + t*t*self.b3/2 + t*self.c3 +self.d3
            self.velocity = t*t*self.a3/2 + t*self.b3 + self.c3
            self.acceleration = t*self.a3 + self.b3

        elif self.t3<t and t<= self.t4:
            self.position = t*t*t*self.a4/6 + t*t*self.b4/2 + t*self.c4 +self.d4
            self.velocity = t*t*self.a4/2 + t*self.b4 + self.c4
            self.acceleration = t*self.a4 + self.b4

        elif self.t4<t and t<= self.t5:
            self.position = t*t*t*self.a5/6 + t*t*self.b5/2 + t*self.c5 +self.d5
            self.velocity = t*t*self.a5/2 + t*self.b5 + self.c5
            self.acceleration = t*self.a5 + self.b5

        elif self.t5<t and t<= self.t6:
            self.position = t*t*t*self.a6/6 + t*t*self.b6/2 + t*self.c6 +self.d6
            self.velocity = t*t*self.a6/2 + t*self.b6 + self.c6
            self.acceleration = t*self.a6 + self.b6

        elif self.t6<t and t<= self.T:  
            self.position = t*t*t*self.a7/6 + t*t*self.b7/2 + t*self.c7 +self.d7
            self.velocity = t*t*self.a7/2 + t*self.b7 + self.c7
            self.acceleration = t*self.a7 + self.b7
        else:
            self.position = self.delta_q
            self.velocity = 0
            self.acceleration = 0
        
        if self.sign == 1:
            self.position = self.position + self.q0
        else:
            self.position = self.qf - self.position
            self.velocity = -self.velocity
            self.acceleration = -self.acceleration
            

    def set_velocity(self):
        return self.velocity

    def set_position(self):
        return self.position

    def set_acceleration(self):
        return self.acceleration

    def operation(self,*args,**kwargs):
        delta = kwargs['qf']-self.qf
        if (delta != 0) and (self.t >= self.T or self.t == 0):
        
            self.q0 = kwargs['q0']
            self.qf = kwargs['qf']

            if self.qf - self.q0 >= 0:
                self.sign = 1
            else:
                self.sign = -1

            self.delta_q = abs(self.qf - self.q0)

            self.Amax = kwargs['A']
            self.Vmax = kwargs['V']
            self.Jmax = kwargs['J']

            self.Amax = self.Vmax**2/self.delta_q + 200

            a = self.Amax*self.Amax*self.Vmax / (self.delta_q*self.Amax - self.Vmax*self.Vmax)

            self.Jmax = a + 200

            print(self.Jmax)

            self.a1 = self.Jmax
            self.a2 = 0
            self.a3 = -self.Jmax
            self.a4 = 0
            self.a5 = -self.Jmax
            self.a6 = 0
            self.a7 = self.Jmax

            self.T = (self.Amax/self.Jmax) + (self.Vmax/self.Amax) + (self.delta_q/self.Vmax)
            
            self.t1 = self.Amax/self.Jmax
            self.t3 = self.t1 + (self.Vmax/self.Amax)
            self.t2 = self.t3 - self.t1

            print(self.t3, self.T/2)

            self.t4 = self.T - self.t3
            self.t5 = self.T - self.t2
            self.t6 = self.T - self.t1

            self.b1 = 0
            self.b2 = self.Amax
            self.b3 = self.Amax + self.Jmax*self.t2
            self.b4 = 0
            self.b5 = self.Jmax*self.t4
            self.b6 = -self.Amax
            self.b7 = -self.Amax - self.Jmax*self.t6

            self.c1 = 0
            self.c2 = ((self.a1*self.t1**2)/2 + self.b1*self.t1 + self.c1) - ((self.a2*self.t1**2)/2 + self.b2*self.t1)
            self.c3 = ((self.a2*self.t2**2)/2 + self.b2*self.t2 + self.c2) - ((self.a3*self.t2**2)/2 + self.b3*self.t2)
            self.c4 = ((self.a3*self.t3**2)/2 + self.b3*self.t3 + self.c3) - ((self.a4*self.t3**2)/2 + self.b4*self.t3)
            self.c5 = ((self.a4*self.t4**2)/2 + self.b4*self.t4 + self.c4) - ((self.a5*self.t4**2)/2 + self.b5*self.t4)
            self.c6 = ((self.a5*self.t5**2)/2 + self.b5*self.t5 + self.c5) - ((self.a6*self.t5**2)/2 + self.b6*self.t5)
            self.c7 = ((self.a6*self.t6**2)/2 + self.b6*self.t6 + self.c6) - ((self.a7*self.t6**2)/2 + self.b7*self.t6)

            self.d1 = self.q0
            self.d2 = ((self.a1*self.t1**3)/6 + (self.b1*self.t1**2)/2 + self.c1*self.t1 + self.d1) - ((self.a2*self.t1**3)/6 + (self.b2*self.t1**2)/2 + self.c2*self.t1)
            self.d3 = ((self.a2*self.t2**3)/6 + (self.b2*self.t2**2)/2 + self.c2*self.t2 + self.d2) - ((self.a3*self.t2**3)/6 + (self.b3*self.t2**2)/2 + self.c3*self.t2)
            self.d4 = ((self.a3*self.t3**3)/6 + (self.b3*self.t3**2)/2 + self.c3*self.t3 + self.d3) - ((self.a4*self.t3**3)/6 + (self.b4*self.t3**2)/2 + self.c4*self.t3)
            self.d5 = ((self.a4*self.t4**3)/6 + (self.b4*self.t4**2)/2 + self.c4*self.t4 + self.d4) - ((self.a5*self.t4**3)/6 + (self.b5*self.t4**2)/2 + self.c5*self.t4)
            self.d6 = ((self.a5*self.t5**3)/6 + (self.b5*self.t5**2)/2 + self.c5*self.t5 + self.d5) - ((self.a6*self.t5**3)/6 + (self.b6*self.t5**2)/2 + self.c6*self.t5)
            self.d7 = ((self.a6*self.t6**3)/6 + (self.b6*self.t6**2)/2 + self.c6*self.t6 + self.d6) - ((self.a7*self.t6**3)/6 + (self.b7*self.t6**2)/2 + self.c7*self.t6)

            self.t = 0
            self.finish = 0

        if self.t < self.T:
            self.t+= self.index
            self.get_data(self.t)
        else:
            self.finish = 1
            self.get_data(self.t)

class ParameterForm(QtWidgets.QWidget):
    def __init__(self,*args,**kwargs):
        super(ParameterForm,self).__init__()

        name = QtWidgets.QLabel(text=kwargs['name'])
        name.setAlignment(QtCore.Qt.AlignCenter)

        self.value_la =QtWidgets.QLineEdit(text=str(kwargs['value']))
        self.value_la.setValidator(QDoubleValidator())
        self.value_la.setAlignment(QtCore.Qt.AlignCenter)

        unit = QtWidgets.QLabel(text=kwargs['unit'])
        unit.setAlignment(QtCore.Qt.AlignCenter)

        box = QtWidgets.QHBoxLayout(self)
        box.addWidget(name)
        box.addWidget(self.value_la)
        box.addWidget(unit)

    def get_value(self):
        return float(self.value_la.text())

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class MainWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()

        self.setWindowTitle("SEGMENT 7")

        self.start_point = ParameterForm(name="Start", value=0, unit=" ")
        self.end_point = ParameterForm(name="End", value=260, unit=" ")

        self.a_max = ParameterForm(name="Amax", value=200, unit=" ")
        self.v_max = ParameterForm(name="Vmax", value=120, unit=" ")
        self.j_max = ParameterForm(name="Jmax", value=1000, unit=" ")

        self.load_bt = QtWidgets.QPushButton(text="LOAD")
        self.load_bt.clicked.connect(self.update_plot)

        box_la = QtWidgets.QVBoxLayout()
        box_la.addWidget(self.start_point)
        box_la.addWidget(self.end_point)
        box_la.addWidget(self.a_max)
        box_la.addWidget(self.v_max)
        box_la.addWidget(self.j_max)
        box_la.addWidget(self.load_bt)

        self.graphics = MplCanvas(self, width=5, height=4, dpi=100)

        box = QtWidgets.QHBoxLayout(self)
        box.addLayout(box_la)
        box.addWidget(self.graphics)

        self.segment_7 = Segment7(A=self.a_max.get_value(), V=self.v_max.get_value(), J=self.j_max.get_value(), t=0.01)

    def update_plot(self):
        self.graphics.axes.clear()

        time = []
        position = []
        velocity = []
        acceleration = []
        
        while(1):
            self.segment_7.operation(q0=self.start_point.get_value(),qf= self.end_point.get_value(),A=self.a_max.get_value(),V=self.v_max.get_value(),J=self.j_max.get_value())

            t = round(self.segment_7.t, 3)
            p = round(self.segment_7.position, 3)
            v = round(self.segment_7.velocity, 3)
            a = round(self.segment_7.acceleration, 3)

            time.append(t)
            position.append(p)
            velocity.append(v)
            acceleration.append(a)
            if (self.segment_7.finish == 1):
                self.segment_7.qf = 0
                self.segment_7.q0 = 0
                break

        self.graphics.axes.plot(time, position, label="P ")
        self.graphics.axes.plot(time, velocity, label="V ")
        self.graphics.axes.plot(time, acceleration, label="A ")
        self.graphics.axes.legend()
        
        self.graphics.axes.set_xlim([0, round(self.segment_7.T, 3)])
        self.graphics.axes.grid(True)
        self.graphics.draw()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())