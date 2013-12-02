# -*- coding: utf-8 -*-
from PyQt4.QtGui import QMainWindow, QListWidgetItem, QMessageBox, QHeaderView
from ui_mainwindow import Ui_MainWindow
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QPalette, QColor
import model

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, app):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.app = app
        self.pbDt.clicked.connect(self.onBtnDt)
        self.pbEvent.clicked.connect(self.onBtnEvent)

    def _genModel(self):
        queue_size = int(self.leQueueSize.text())
        gen_exp = float(self.leGenExpVal.text())
        proc_exp = float(self.leProcExpVal.text())
        proc_half_range = float(self.leProcDiap.text())
        eps = float(self.leEps.text())
        with_return = self.rbWithReturn.isChecked()
        return model.Model(gen_exp, proc_exp, proc_half_range, queue_size, eps, with_return)

    def _output(self, model_time, rejected, logs):
        self.teLog.clear()
        for l in logs:
            self.teLog.appendPlainText(l)
        self.teLog.appendPlainText("Необработано: %d заявок" % rejected)

    def onBtnDt(self):
        self._output(*self._genModel().run_dt(float(self.leDeltaT.text()), int(self.leTicketsNum.text())))

    def onBtnEvent(self):
        self._output(*self._genModel().run_event(int(self.leTicketsNum.text())))
