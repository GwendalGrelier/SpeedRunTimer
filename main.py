import sys
import threading
import time
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import keyboard


def secondsToText(secs):
    """ Converts a number of sec to the format hh:mm:ss

        :param secs: The number of seconds to convert
        :type secs: int
        :return: The formated converted time
        :rtype: str
    """
    days = secs // 86400
    hours = int((secs - days * 86400) // 3600)
    minutes = int((secs - days * 86400 - hours * 3600) // 60)
    seconds = int(secs - days * 86400 - hours * 3600 - minutes * 60)
    text = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return text


class MainWindow(QMainWindow):
    def __init__(self, screenWidth):
        super(MainWindow, self).__init__()
        self.elapsed_time_in_sec = 0
        self.timerIsStarted = False
        self.timerIsPaused = False
        self.initUi(screenWidth, screenHeight)


    def initUi(self, maxWidth):
        """ Creates the main window
        
            Creates and displays the window at the top right of the screen,
            it will stay on top of the desktop, is frameless and has a transparent backgound
            
            :param maxWidth: Max width of the current screen, in pixels
            :type maxWidth: int
            :return: None
        """
        self.setGeometry(maxWidth-150, -50, 150, 150)
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
        keyboard.add_hotkey('del', self.toggleTimer)
        keyboard.add_hotkey('shift + del', self.resetTimer)


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

    window = MainWindow(rect.width())
    sys.exit(app.exec_())
