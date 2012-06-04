import sys
import threading
import time
from PySide import QtGui, QtCore
from cmonitor import *

class SystemTrayIcon(QtGui.QSystemTrayIcon):

    show_message = QtCore.Signal(str, str, int)

    def __init__(self, icon, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        self.menu = QtGui.QMenu(parent)
        exitAction = self.menu.addAction('Exit')
        exitAction.triggered.connect(self.exit)
        self.setContextMenu(self.menu)
        self.pm = ProcessMonitor()
        self.timer = Timer(10, self)
        self.timer.daemon = True
        self.timer.start()
        self.show_message.connect(self.message)
        self.setIcon(QtGui.QIcon('process.png'))


    def message(self, title, text, msecs):
        self.showMessage(title, text, QtGui.QSystemTrayIcon.Critical, msecs=msecs)


    def exit(self):
        self.pm.close()
        sys.exit(0)


class Timer(threading.Thread):
    def __init__(self, seconds, tray_icon):
        threading.Thread.__init__(self)
        self.runTime = seconds
        self.tray_icon = tray_icon


    def run(self):
        self.tray_icon.pm.connect()
        while True:
          time.sleep(self.runTime)
          procs = self.tray_icon.pm.do_work()
          self.tray_icon.setToolTip('Procesos: {0}'.format(procs))
          if int(procs) > 30:
            self.tray_icon.show_message.emit('Alerta procesos http',
                                             'Actualmente {0}'.format(procs),
                                             1000 * (self.runTime - 1))


if __name__ == '__main__':
    t0 = time.clock()
    app = QtGui.QApplication(sys.argv)
    style = app.style()
    icon = QtGui.QIcon(style.standardPixmap(QtGui.QStyle.SP_FileIcon))
    trayIcon = SystemTrayIcon(icon)
    trayIcon.show()
    app.exec_()
