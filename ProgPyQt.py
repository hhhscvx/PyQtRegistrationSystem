import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox


class CorrectError(Exception):  # Ошибка, вызывающаяся при некорректном вводе данных
    pass


class LoginError(Exception):  # Ошибка, вызывающаяся при отсутствии данного пользователя в базе данных
    pass


class PasswordError(Exception):  # Ошибка, вызывающаяся при проблемах с паролем
    pass


class Authorization(QMainWindow):  # Класс авторизации
    def __init__(self):
        super().__init__()
        uic.loadUi('authorization.ui', self)
        self.auth_window()  # Открытие окна авторизации

    def auth(self):
        con = sqlite3.connect('registration.db')  # Подключение к БД для логина
        con2 = sqlite3.connect('registration.db')  # Подключение к БД для пароля
        cur = con.cursor()
        cur2 = con2.cursor()
        sql_text = f"SELECT * FROM passwords WHERE user_login = '{self.aut_login.text()}'"
        sql_pw_text = f"SELECT user_password FROM passwords WHERE user_login = '{self.aut_login.text()}' AND user_password = '{self.aut_password.text()}'"
        res2 = cur2.execute(sql_pw_text)
        result = cur.execute(sql_text)
        try:
            if self.aut_login.text() == '' or self.aut_password.text() == '':  # Проверка на заполненность полей
                raise CorrectError
            elif result.fetchone() is None:  # Проверка, существует ли данный пользователь в БД
                raise LoginError
            elif res2.fetchone() is None:  # Проверка, верный ли пароль
                raise PasswordError
            else:
                self.error_label.setText('Успешная авторизация!')
        except CorrectError:
            self.error_message('Все поля должны быть заполнены!')  # Уведомление о незаполненности полей
        except LoginError:
            self.error_message('Такого пользователя не существует.')  # Уведомление о неверном логине
        except PasswordError:
            self.error_message('Неправильный пароль.')  # Уведомление о неправильном пароле
        con.close()

    def error_message(self, errortext):  # Метод вызова уведомления с ошибкой
        error = QMessageBox()
        error.setWindowTitle('Ошибка')
        error.setText(errortext)
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        error.exec_()

    def auth_window(self):  # Метод открытия окна авторизации
        self.aut_comeBtn.clicked.connect(self.auth)
        self.aut_regBtn.clicked.connect(self.reg_window)
        self.aut_password_2.hide()
        self.aut_comeBtn.move(160, 280)
        self.aut_regBtn.move(170, 340)
        self.aut_comeBtn.setText('Войти')
        self.aut_regBtn.setText('Создать аккаунт')
        self.aut_label.setText('Авторизация')
        self.setWindowTitle('Авторизация')

    def reg_window(self):  # Метод открытия окна регистрации
        self.rs = Registration()
        self.rs.show()
        self.hide()


class Registration(QMainWindow):  # Класс регистрации
    def __init__(self):
        super().__init__()
        uic.loadUi('authorization.ui', self)
        self.registration_window()  # Открытие окна регистрации

    def metod(self):  # Метод проверки на корректность введенных данных
        try:
            if self.aut_login.text() == '' or self.aut_password.text() == '' or self.aut_password_2.text() == '':  # Проверка на заполненность полей
                raise CorrectError
            elif self.aut_password.text() != self.aut_password_2.text():
                raise PasswordError
            else:
                self.login_check()  # Проверка занят ли логин

        except CorrectError:
            self.error_message2('Все поля должны быть заполнены!')
        except LoginError:
            self.error_message2('Такой логин уже занят!')
        except PasswordError:
            self.error_message2('Пароли должны совпадать!')  # Уведомление о несовпадении паролей

    def db_add_user(self):  # Метод добавления данных о пользователе в БД
        con = sqlite3.connect('registration.db')
        cur = con.cursor()
        cur.execute(
            f"INSERT INTO passwords (user_login, user_password) VALUES ('{self.aut_login.text()}', '{self.aut_password.text()}')")
        con.commit()
        cur.close()
        con.close()
        self.error_label.setText('Успешная регистрация!')

    def login_check(self):  # Проверка занят ли логин
        self.con2 = sqlite3.connect('registration.db')
        self.cur2 = self.con2.cursor()
        self.sql_text = f"SELECT user_login FROM passwords WHERE user_login = '{self.aut_login.text()}'"
        self.result = self.cur2.execute(self.sql_text)
        self.flag_found = False
        for elem in self.result:
            if elem[0] == self.aut_login.text():
                self.flag_found = True
        if not self.flag_found:
            self.db_add_user()
        else:
            raise LoginError

    def error_message2(self, errortext2):  # Метод вызова уведомления с ошибкой
        error = QMessageBox()
        error.setWindowTitle('Ошибка')
        error.setText(errortext2)
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        error.exec_()

    def registration_window(self):  # Метод открытия окна регистрации
        self.aut_comeBtn.clicked.connect(self.metod)
        self.aut_password_2.show()
        self.aut_regBtn.clicked.connect(self.authorization_window)
        self.aut_comeBtn.move(160, 340)
        self.aut_regBtn.move(170, 400)
        self.aut_comeBtn.setText('Зарегистрировать')
        self.aut_regBtn.setText('Войти в аккаунт')
        self.aut_label.setText('Регистрация')
        self.setWindowTitle('Регистрация')

    def authorization_window(self):  # Метод открытия окна авторизации
        self.aut = Authorization()
        self.aut.show()
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    au = Authorization()
    au.show()
    sys.exit(app.exec_())
