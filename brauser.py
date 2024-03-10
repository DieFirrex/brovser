import sys  # Модуль sys використовується для доступу до функцій, пов'язаних з інтерпретатором Python
from PyQt5.QtCore import *  # PyQt5.QtCore містить базові класи для роботи з подіями та таймерами
from PyQt5.QtWidgets import *  # PyQt5.QtWidgets містить класи віджетів та інші елементи інтерфейсу користувача
from PyQt5.QtWebEngineWidgets import *  # PyQt5.QtWebEngineWidgets містить класи для роботи з веб-двигуном Qt WebEngine

# Використовуємо клас QMainWindow з PyQt5 для створення вікна
# до конструктора QMainWindow
class MainWindow(QMainWindow):

        # Створюємо головне вікно додатку та ініціалізуємо його
        # Передаємо *args та **kwargs, щоб передати будь-які додаткові аргументи та ключові слова
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        # Ініціалізуємо браузер та встановлюємо URL за замовчуванням
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://google.com"))

        # Встановлюємо браузер як центральний віджет у головному вікні
        self.setCentralWidget(self.browser)
        
        # Створюємо панель інструментів для навігації
        navtb = QToolBar()
        self.addToolBar(navtb)

        # Додаємо кнопку "Назад" та підключаємо її до методу навігації назад
        back_btn = QAction("Назад", self)
        back_btn.triggered.connect(self.browser.back)
        navtb.addAction(back_btn)

        # Додаємо кнопку "Вперед" та підключаємо її до методу навігації вперед
        next_btn = QAction("Вперед", self)
        next_btn.triggered.connect(self.browser.forward)
        navtb.addAction(next_btn)

        # Додаємо кнопку "Перезапустити" та підключаємо її до методу перезавантаження сторінки
        reload_btn = QAction("Перезагрузити", self)
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)

        # Створюємо поле введення URL-адреси та підключаємо його до методу переходу за URL
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        # Відображаємо головне вікно
        self.show()

        # Підключаємо сигнали зміни URL та завершення завантаження сторінки до відповідних методів
        self.browser.urlChanged.connect(self.update_urlbar)
        self.browser.loadFinished.connect(self.update_title)

    # Метод для оновлення заголовка вікна з урахуванням назви сторінки
    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle("% s - Браузер від Андрія" % title)

    # Метод для навігації за введеним URL
    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("https")
        self.browser.setUrl(q)

    # Метод для оновлення адресного рядка з поточним URL
    def update_urlbar(self, q):
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

# Створюємо та запускаємо додаток
app = QApplication(sys.argv)
window = MainWindow()
app.exec_()
