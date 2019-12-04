import sys
import threading
import time
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import keyboard


class setInterval :
    def __init__(self,interval,action) :
        self.interval=interval
        self.action=action
        self.stopEvent=threading.Event()
        thread=threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self) :
        nextTime=time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()) :
            nextTime+=self.interval
            self.action()

    def cancel(self) :
        self.stopEvent.set()

def secondsToText(secs):
    days = secs // 86400
    hours = int((secs - days * 86400) // 3600)
    minutes = int((secs - days * 86400 - hours * 3600) // 60)
    seconds = int(secs - days * 86400 - hours * 3600 - minutes * 60)
    text = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return text


class MainWindow(QMainWindow):
    def __init__(self, screenWidth, screenHeight):
        super(MainWindow, self).__init__()
        self.elapsed_time_in_sec = 0
        self.timerIsStarted = False
        self.timerIsPaused = False
        self.initUi(screenWidth, screenHeight)


    def initUi(self, maxWidth, maxHeight):
        print(maxWidth)
        print(maxHeight)
        self.setGeometry(maxWidth-150, -50, 300, 300)
        self.setWindowTitle("SpeedRun counter")
        self.setWindowFlags(Qt.FramelessWindowHint |
                            Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        font = QFont()
        font.setFamily("Helvetica")
        font.setPointSize(25)

        self.label = QLabel("00:00:00", self)
        self.label.setFont(font)
        self.label.setStyleSheet('color: white')
        self.label.resize(self.width(), self.height())
        self.show()
        keyboard.add_hotkey('²', self.toggleTimer)
        keyboard.add_hotkey('shift + ²', self.resetTimer)


    def startTimer(self):
        self.label.setStyleSheet('color: white')
        self.init_timer = time.time()
        self.set_interval(self.updateTime, 1)


    def updateTime(self):
        self.elapsed_time_in_sec += 1
        new_time = secondsToText(self.elapsed_time_in_sec)
        self.label.setText(str(new_time))


    def toggleTimer(self):
        if self.timerIsStarted == False:
            self.timerIsStarted = True
            self.startTimer()
        elif self.timerIsPaused:
            self.set_interval(self.updateTime, 1)
            self.timerIsPaused = False
        else:
            self.t.cancel()
            self.timerIsPaused = True
            self.timeAtPause = time.time()


    def resetTimer(self):
        self.t.cancel()
        new_time = secondsToText(self.elapsed_time_in_sec)
        self.label.setText(str(new_time))
        self.label.setStyleSheet('color: red')
        self.elapsed_time_in_sec = 0
        self.timerIsStarted = False
        self.timerIsPaused = False


    def set_interval(self, func, ms):
        def func_wrapper():
            self.set_interval(func, ms/1)
            func()
        self.t = threading.Timer(ms, func_wrapper)
        self.t.start()
        return self.t





if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Get screen dimension to set the counter position
    screen = app.primaryScreen()
    rect = screen.availableGeometry()
    rect.width(), rect.height()

    window = MainWindow(rect.width(), rect.height())
    sys.exit(app.exec_())
