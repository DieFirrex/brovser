import sqlite3
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QLineEdit
import project_1_ui

db = sqlite3.connect('database.db')
cursor = db.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users(
    login TEXT,
    password TEXT
)''')
db.commit()

class PasswordValidator:
    @staticmethod
    def is_valid(password):
        if len(password) < 8:
            return False
        
        if password.isalpha():
            return False

        return True

def read_profile_data(username):
    try:
        with open('profile.txt', 'r') as file:
            lines = file.readlines()
            profile_data = {}
            current_username = None
            for line in lines:
                if line.startswith("Account:"):
                    current_username = line.split(":")[1].strip()
                    profile_data[current_username] = {}
                elif current_username:
                    key, value = line.strip().split(':')
                    profile_data[current_username][key.strip()] = value.strip()
            return profile_data.get(username)  # Return profile data for the given username
    except FileNotFoundError:
        return None

class ProfileDialog(QtWidgets.QDialog):
    def __init__(self, profile_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Профіль')
        self.resize(300, 200)

        layout = QtWidgets.QVBoxLayout(self)

        name_label = QtWidgets.QLabel(f'Ім\'я: {profile_data["Name"]}')  # Update key to "Name"
        layout.addWidget(name_label)

        age_label = QtWidgets.QLabel(f'Вік: {profile_data["Age"]}')  # Update key to "Age"
        layout.addWidget(age_label)

        description_label = QtWidgets.QLabel(f'Опис: {profile_data["Description"]}')  # Update key to "Description"
        layout.addWidget(description_label)

class AccountsWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Список акаунтів')
        self.resize(300, 200)

        layout = QtWidgets.QVBoxLayout(self)

        self.accounts_list = QtWidgets.QListWidget()
        layout.addWidget(self.accounts_list)

        self.load_accounts()

    def load_accounts(self):
        cursor.execute('SELECT login FROM users')
        accounts = cursor.fetchall()
        for account in accounts:
            self.accounts_list.addItem(account[0])

class Register(QtWidgets.QMainWindow, project_1_ui.Ui_MainWindow):
    def __init__(self):
        super(Register, self).__init__()
        self.setupUi(self)
        self.label.setText('')
        self.label_2.setText('Реєстрація')
        self.lineEdit.setPlaceholderText('Введіть Логін')
        self.lineEdit_2.setPlaceholderText('Введіть Пароль')
        self.pushButton.setText('Реєстрація')
        self.pushButton_2.setText('Вхід')
        self.pushButton_4.setText('Показати акаунти')
        self.pushButton_3.setText('Мій профіль')  # Added button for profile
        self.setWindowTitle('Реєстрація')

        self.pushButton.pressed.connect(self.register_account) 
        self.pushButton_2.pressed.connect(self.login)
        self.pushButton_4.clicked.connect(self.show_accounts)
        self.pushButton_3.clicked.connect(self.show_profile)  # Connect to show profile

    def show_accounts(self):
        self.accounts_window = AccountsWindow()
        self.accounts_window.show()

    def login(self):
        self.login = Login()
        self.login.show()
        self.hide()

    def show_profile(self):
        username = self.lineEdit.text().strip()  # Get the username from the input field
        profile_data = read_profile_data(username)  # Read profile data for the provided username
        if profile_data:
            profile_dialog = ProfileDialog(profile_data, parent=self)
            profile_dialog.exec_()
        else:
            QtWidgets.QMessageBox.warning(self, "Помилка", "Не вдалося знайти профіль для цього акаунту.")

    def register_account(self):
        login = self.lineEdit.text().strip()  # Видаляємо пробіли з початку і кінця рядка
        password = self.lineEdit_2.text().strip()  # Видаляємо пробіли з початку і кінця рядка

        if login and password:  # Перевіряємо, чи рядки не порожні
            if PasswordValidator.is_valid(password):
                # Питаємо користувача, чи він впевнений у використанні ненадійного пароля
                reply = QMessageBox.question(self, 'Ненадійний пароль', 
                    'Ви впевнені, що хочете використати такий ненадійний пароль?', 
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    # Перевіряємо, чи існує вже акаунт з таким логіном
                    cursor.execute('SELECT * FROM users WHERE login=?', (login,))
                    existing_user = cursor.fetchone()
                    if existing_user:
                        QtWidgets.QMessageBox.warning(self, "Помилка", "Користувач з таким логіном вже існує.")
                    else:
                        cursor.execute('INSERT INTO users (login, password) VALUES (?, ?)', (login, password))
                        db.commit()
                        # After successful registration, show profile
                        profile_data = read_profile_data(login)  # Read profile data for the registered user
                        if profile_data:
                            profile_dialog = ProfileDialog(profile_data, parent=self)
                            profile_dialog.exec_()
                        else:
                            QtWidgets.QMessageBox.warning(self, "Помилка", "Не вдалося знайти профіль для цього акаунту.")
            else:
                QtWidgets.QMessageBox.warning(self, "Помилка", "Ви впевнені, що хочете використати такий ненадійний пароль?")
                return
        else:
            QtWidgets.QMessageBox.warning(self, "Помилка", "Будь ласка, введіть логін та пароль.")

class Login(QtWidgets.QMainWindow, project_1_ui.Ui_MainWindow):
    def __init__(self):
        super(Login, self).__init__()
        self.setupUi(self)
        self.label.setText('')
        self.label_2.setText('Логін')
        self.lineEdit.setPlaceholderText('Введіть логін')
        self.lineEdit_2.setPlaceholderText('Введіть пароль')
        self.pushButton.setText('Вхід')
        self.pushButton_2.setText('Реєстрація')
        self.pushButton_4.setText('Показати акаунти')
        self.pushButton_3.setText('Мій профіль')  # Added button for profile
        self.setWindowTitle('Вхід')

        self.pushButton_4.clicked.connect(self.show_accounts)
        self.pushButton.pressed.connect(self.login_attempt)
        self.pushButton_2.pressed.connect(self.reg)
        self.pushButton_3.clicked.connect(self.show_profile)  # Connect to show profile

        self.logged_in = False

    def show_accounts(self):
        if self.logged_in:
            self.accounts_window = AccountsWindow()
            self.accounts_window.show()
        else:
            QtWidgets.QMessageBox.warning(self, "Помилка", "Будь ласка, увійдіть в систему для перегляду акаунтів.")

    def reg(self):
        if self.logged_in:
            self.reg = Register()
            self.reg.show()
            self.hide()
        else:
            self.label.setText('Спочатку увійдіть в систему!')

    def show_profile(self):
        if self.logged_in:
            username = self.lineEdit.text().strip()  # Get the logged-in username
            profile_data = read_profile_data(username)  # Read profile data for the logged-in user
            if profile_data:
                profile_dialog = ProfileDialog(profile_data, parent=self)
                profile_dialog.exec_()
            else:
                QtWidgets.QMessageBox.warning(self, "Помилка", "Не вдалося знайти профіль для цього акаунту.")
        else:
            QtWidgets.QMessageBox.warning(self, "Помилка", "Спочатку увійдіть в систему!")

    def login_attempt(self):
        user_login = self.lineEdit.text().strip()  # Видаляємо пробіли з початку і кінця рядка
        user_password = self.lineEdit_2.text().strip()  # Видаляємо пробіли з початку і кінця рядка

        if user_login and user_password:  # Перевіряємо, чи рядки не порожні
            cursor.execute(f'SELECT * FROM users WHERE login="{user_login}" AND password="{user_password}"')
            existing_user = cursor.fetchone()

            if existing_user:
                self.logged_in = True
                import subprocess
                subprocess.Popen(["python", "okno.py"])
            else:
                reply = QtWidgets.QMessageBox.question(self, 'Реєстрація нового акаунту', 
                    'Користувача з таким логіном і паролем не знайдено. Бажаєте зареєструвати новий акаунт?',
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.Yes:
                    self.reg = Register()
                    self.reg.show()
                    self.hide()
        else:
            QtWidgets.QMessageBox.warning(self, "Помилка", "Будь ласка, введіть логін та пароль.")

def is_logged_in():
    return hasattr(Login, 'logged_in') and Login.logged_in

App = QtWidgets.QApplication([])
window = Login()
window.show()
App.exec()
