import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QInputDialog
from prof_ import Ui_MainWindow
import sqlite3

class ProfileApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.label.setText("Введіть ім'я")
        self.label_2.setText("Введіть вік")
        self.label_3.setText("Опис себе")
        self.label_4.setText("Редагування профілю")
        self.pushButton.setText('Зберегти')
        self.pushButton.clicked.connect(self.save_profile)

    def save_profile(self):
        name = self.lineEdit.text()
        age = self.spinBox.value()
        description = self.textEdit.toPlainText()

        if name and description:
            # Запит користувача для вибору акаунту
            account, ok = QInputDialog.getText(self, 'Вибір акаунту', 'Введіть назву акаунту:')
            if ok:
                # Збереження профілю разом з вказаною ​​інформацією про акаунт
                with open("profile.txt", "w") as file:
                    file.write(f"Account: {account}\n")
                    file.write(f"Name: {name}\n")
                    file.write(f"Age: {age}\n")
                    file.write(f"Description: {description}\n")

                QMessageBox.information(self, "Saved", "Your profile has been saved successfully!")
        else:
            QMessageBox.warning(self, "Error", "Name and description are required!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ProfileApp()
    window.show()
    sys.exit(app.exec_())
