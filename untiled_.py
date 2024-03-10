import sqlite3
from PyQt5 import QtWidgets, QtCore
import untiled
import subprocess

class ChangePasswordDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Зміна паролю")
        
        layout = QtWidgets.QVBoxLayout(self)
        
        self.account_combo = QtWidgets.QComboBox(self)
        self.fill_accounts_combo()
        layout.addWidget(self.account_combo)
        
        self.old_password_edit = QtWidgets.QLineEdit(self)
        self.old_password_edit.setPlaceholderText("Старий пароль")
        layout.addWidget(self.old_password_edit)
        
        self.new_password_edit = QtWidgets.QLineEdit(self)
        self.new_password_edit.setPlaceholderText("Новий пароль")
        layout.addWidget(self.new_password_edit)
        
        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def fill_accounts_combo(self):
        # З'єднуємося з базою даних
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        # Виконуємо запит до бази даних щоб отримати список акаунтів
        cursor.execute('SELECT login FROM users')
        accounts = cursor.fetchall()
        # Додаємо отримані акаунти до списку
        for account in accounts:
            self.account_combo.addItem(account[0])

    def get_data(self):
        return (
            self.account_combo.currentText(),
            self.old_password_edit.text(),
            self.new_password_edit.text()
        )

class ChangeAccountDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Зміна акаунту")
        
        layout = QtWidgets.QVBoxLayout(self)
        
        self.old_account_edit = QtWidgets.QLineEdit(self)
        self.old_account_edit.setPlaceholderText("Старий акаунт")
        layout.addWidget(self.old_account_edit)
        
        self.old_password_edit = QtWidgets.QLineEdit(self)
        self.old_password_edit.setPlaceholderText("Пароль")
        layout.addWidget(self.old_password_edit)
        
        self.new_account_edit = QtWidgets.QLineEdit(self)
        self.new_account_edit.setPlaceholderText("Новий акаунт")
        layout.addWidget(self.new_account_edit)
        
        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_data(self):
        return (
            self.old_account_edit.text(),
            self.old_password_edit.text(),
            self.new_account_edit.text()
        )

class profil(QtWidgets.QMainWindow, untiled.Ui_MainWindow):
    def __init__(self):
        super(profil, self).__init__()
        # Ініціалізуємо інтерфейс
        self.setupUi(self)
        # Встановлюємо текст та параметри елементів інтерфейсу
        self.label.setText('Виберіть дію')
        self.pushButton.setText('Змінити пароль')
        self.pushButton_2.setText('Змінити назву акаунту')
        self.pushButton_3.setText('Створення профілю')
        self.pushButton_4.setText('Видалити акаунт')
        self.pushButton_5.setText('Перегляд профілю')
        
        # Під'єднуємо кнопки до відповідних методів
        self.pushButton.clicked.connect(self.change_password_dialog)
        self.pushButton_2.clicked.connect(self.change_account_dialog)
        self.pushButton_3.clicked.connect(self.open_profile_file)
        self.pushButton_4.clicked.connect(self.delete_account_dialog)
        self.pushButton_5.clicked.connect(self.open_profile_file)

    def open_profile_file(self):
        subprocess.Popen(["python", "prof_1.py"])

    def change_password_dialog(self):
        dialog = ChangePasswordDialog(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            account, old_password, new_password = dialog.get_data()
            self.change_password(account, old_password, new_password)

    def change_account_dialog(self):
        dialog = ChangeAccountDialog(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            old_account, old_password, new_account = dialog.get_data()
            self.change_account(old_account, old_password, new_account)

    def change_password(self, account, old_password, new_password):
        # З'єднуємося з базою даних
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        # Виконуємо запит до бази даних, щоб отримати поточний пароль для вказаного облікового запису
        cursor.execute('SELECT password FROM users WHERE login = ?', (account,))
        correct_password = cursor.fetchone()[0]
        
        # Перевіряємо, чи введений старий пароль співпадає з поточним паролем
        if old_password == correct_password:
            # Код для оновлення паролю в базі даних
            print("Акаунт:", account)
            print("Новий пароль:", new_password)
            # Оновлюємо пароль в базі даних
            cursor.execute('UPDATE users SET password = ? WHERE login = ?', (new_password, account))
            db.commit()
            QtWidgets.QMessageBox.information(self, "Зміна паролю", "Пароль успішно змінено!")
        else:
            # Пароль введено неправильно
            QtWidgets.QMessageBox.warning(self, "Помилка", "Введено неправильний старий пароль!")

    def change_account(self, old_account, old_password, new_account):
        # З'єднуємося з базою даних
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        # Виконуємо запит до бази даних, щоб перевірити існування введеного облікового запису та його відповідність до введеного паролю
        cursor.execute('SELECT password FROM users WHERE login = ?', (old_account,))
        correct_password = cursor.fetchone()
        
        if correct_password:
            # Обліковий запис і пароль введені правильно, тепер ми можемо змінити назву облікового запису
            # Перевіряємо, чи нова назва акаунту є унікальною
            cursor.execute('SELECT * FROM users WHERE login = ?', (new_account,))
            existing_account = cursor.fetchone()
            if existing_account:
                QtWidgets.QMessageBox.warning(self, "Помилка", "Така назва акаунту вже існує!")
            else:
                # Перевіряємо, чи існує акаунт зі старою назвою
                cursor.execute('SELECT * FROM users WHERE login = ?', (old_account,))
                old_account_exists = cursor.fetchone()
                if not old_account_exists:
                    QtWidgets.QMessageBox.warning(self, "Помилка", "Такого акаунту не існує!")
                else:
                    cursor.execute('UPDATE users SET login = ? WHERE login = ? AND password = ?', (new_account, old_account, old_password))
                    db.commit()
                    QtWidgets.QMessageBox.information(self, "Зміна акаунту", "Назва акаунту успішно змінена!")
        else:
            # Введено неправильний обліковий запис або пароль
            QtWidgets.QMessageBox.warning(self, "Помилка", "Введено неправильний обліковий запис або пароль!")

    def delete_account_dialog(self):
        account, ok = QtWidgets.QInputDialog.getText(self, 'Видалення акаунту', 'Введіть назву акаунту:')
        if ok:
            password, ok = QtWidgets.QInputDialog.getText(self, 'Видалення акаунту', 'Введіть пароль:', QtWidgets.QLineEdit.Password)
            if ok:
                # Перевірка пароля у базі даних
                if self.check_password(account, password):
                    reply = QtWidgets.QMessageBox.question(self, 'Видалення акаунту', f"Ви впевнені, що хочете видалити акаунт {account}?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                    if reply == QtWidgets.QMessageBox.Yes:
                        self.delete_account(account, password)
                else:
                    QtWidgets.QMessageBox.warning(self, "Помилка", "Введено неправильний пароль!")

    def check_password(self, account, password):
        # З'єднуємося з базою даних
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        # Виконуємо запит до бази даних, щоб перевірити пароль
        cursor.execute('SELECT * FROM users WHERE login = ? AND password = ?', (account, password))
        account_exists = cursor.fetchone()
        if account_exists:
            return True
        else:
            return False

    def delete_account(self, account, password):
        print("Акаунт:", account)
        print("Пароль:", password)
        # З'єднуємося з базою даних
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        # Виконуємо запит до бази даних, щоб перевірити існування введеного облікового запису та його відповідність до введеного паролю
        cursor.execute('SELECT * FROM users WHERE login = ? AND password = ?', (account, password))
        account_exists = cursor.fetchone()
        if account_exists:
            cursor.execute('DELETE FROM users WHERE login = ? AND password = ?', (account, password))
            db.commit()
            QtWidgets.QMessageBox.information(self, "Видалення акаунту", f"Акаунт {account} успішно видалений!")
        else:
            QtWidgets.QMessageBox.warning(self, "Помилка", "Введено неправильний обліковий запис або пароль!")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = profil()
    window.show()
    sys.exit(app.exec_())
