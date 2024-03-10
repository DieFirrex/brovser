import subprocess
from PyQt5 import QtWidgets
import pr2

class okno(QtWidgets.QMainWindow, pr2.Ui_MainWindow):
    def __init__(self):
        super(okno, self).__init__()
        # Ініціалізуємо інтерфейс
        self.setupUi(self)
        # Встановлюємо текст та параметри елементів інтерфейсу
        self.label.setText('Виберіть дію')
        self.pushButton.setText('Браузер')
        self.pushButton_2.setText('Управління')
        
        # Під'єднуємо кнопки до відповідних методів
        self.pushButton.pressed.connect(self.open_browser)
        self.pushButton_2.pressed.connect(self.akaunt)

    def open_browser(self):
        # Відкриття файлу brauser.py у програмі редагування (за замовчуванням)
        subprocess.Popen(['python', 'brauser.py'])

    def akaunt(self):
        subprocess.Popen(['python', 'untiled_.py'])

App = QtWidgets.QApplication([])
window = okno()
window.show()
App.exec()
