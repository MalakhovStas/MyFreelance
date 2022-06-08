"""
Задание:
    Разработать программный модуль «Учет успеваемости студентов».
    Программный модуль предназначен для оперативного учета успеваемости
    студентов в сессию деканом, заместителями декана и сотрудниками деканата.
    Сведения об успеваемости студентов должны храниться в течение всего срока
    их обучения и использоваться при составлении справок о прослушанных
    курсах и приложений к диплому.
"""
import pickle
import random
import sqlite3


def get_id() -> str:
    """Генерирует случайным образом id пользователя, проверяет его на уникальность и возвращает id."""
    while True:
        is_id = f'{random.randint(0, 99999):05}'
        if not Db_utils.select_id(is_id):
            return is_id


def input_data_default() -> tuple:
    """Для ввода общих данных пользователей."""
    name = input('Введите имя: ')
    surname = input('Введите фамилию: ')
    age = input('Введите возраст: ')
    return name, surname, age


class Db_utils:
    """Класс методов для работы с базой данных."""

    path_db = 'database.db'

    @classmethod
    def create_table(cls) -> None:
        with sqlite3.connect(cls.path_db) as database:
            cursor = database.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS users(user_id TEXT PRIMARY KEY, user TEXT)""")
            database.commit()

    @classmethod
    def delete_user(cls, user_id: str) -> None:
        with sqlite3.connect(cls.path_db) as database:
            cursor = database.cursor()
            cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id, ))
            database.commit()

    @classmethod
    def insert_user(cls, user_id: str, new_user: bytes) -> None:
        with sqlite3.connect(cls.path_db) as database:
            cursor = database.cursor()
            cursor.execute("INSERT INTO users(user_id, user) VALUES (?, ?)", (user_id, new_user))
            database.commit()

    @classmethod
    def update_user(cls, user_id: str, up_user: bytes) -> None:
        with sqlite3.connect(cls.path_db) as database:
            cursor = database.cursor()
            cursor.execute("UPDATE users SET user = ? WHERE user_id = ?", (up_user, user_id))
            database.commit()

    @classmethod
    def select_id(cls, is_id: str) -> str | None:
        with sqlite3.connect(cls.path_db) as database:
            cursor = database.cursor()
            cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (is_id,))
            user_id = cursor.fetchone()
            if user_id:
                return user_id[0]
            else:
                return None

    @classmethod
    def select_user(cls, user_id: str) -> bytes | None:
        with sqlite3.connect(cls.path_db) as database:
            cursor = database.cursor()
            cursor.execute("SELECT user FROM users WHERE user_id = ?", (user_id,))
            user_data = cursor.fetchone()
            if user_data:
                return user_data[0]
            else:
                return None


class Admin:
    """Класс описывающий администратора."""

    def __init__(self, name: str, surname: str, age: str, admin_id: str, password: str) -> None:
        self.name = name
        self.surname = surname
        self.age = age
        self.admin_id = admin_id
        self.password = password
        Db_utils.insert_user(self.admin_id, pickle.dumps(self))

    def __str__(self) -> str:
        return f'Администратор: {self.surname} {self.name}, возраст: {self.age}'

    @staticmethod
    def add_deans(name: str, surname: str, age: str, position: str):
        """Создаёт и добавляет сотрудника деканата в базу данных."""
        new_dean = DeansOfficeEmployee(name, surname, age, position)
        return f'\n{new_dean}\nУспешно добавлен, его id: {new_dean.deans_id}.\n'

    @staticmethod
    def add_teacher(name: str, surname: str, age: str, subject: str):
        """Создаёт и добавляет преподавателя в базу данных."""
        new_teacher = Teacher(name, surname, age, subject)
        return f'\n{new_teacher}\nУспешно добавлен, его id: {new_teacher.teacher_id}.\n'

    @staticmethod
    def add_student(name: str, surname: str, age: str, faculty: str, department: str):
        """Создаёт и добавляет студента в базу данных."""
        new_student = Student(name, surname, age, faculty, department)
        return f'\n{new_student}\nУспешно добавлен, его id: {new_student.student_id}.\n'

    @staticmethod
    def add_admin(name: str, surname: str, age: str, admin_id: str, password: str):
        # TODO написать метод добавления администратора
        pass

    @staticmethod
    def del_user(user_id):
        Db_utils.delete_user(user_id)
        return '\nПользователь удалён из базы данных.\n'

    def admin_interface(self):
        """Интерфейс пользователя - администратор."""

        password = input('Введите пароль для доступа в систему: ').lower()
        if password != self.password:
            print('Пароль неверный!!!')
            return

        else:
            while True:
                action = input('Введите номер действия:\n\t1.Добавить сотрудника деканата\n\t'
                               '2.Добавить преподавателя\n\t3.Добавить студента\n\t'
                               '4.Удалить пользователя\n\tЧтобы выйти введите - q\n -> : ').lower()
                if action == '1':
                    name, surname, age = input_data_default()
                    position = input('Введите должность: ')
                    print(self.add_deans(name, surname, age, position))

                elif action == '2':
                    name, surname, age = input_data_default()
                    subject = input('Введите название предмета: ')
                    print(self.add_teacher(name, surname, age, subject))

                elif action == '3':
                    name, surname, age = input_data_default()
                    faculty = input('Введите факультет: ')
                    department = input('Введите кафедру: ')
                    print(self.add_student(name, surname, age, faculty, department))

                elif action == '4':
                    data_is_user = Db_utils.select_user(input('Введите id пользователя: '))
                    if data_is_user:
                        is_user = pickle.loads(data_is_user)
                        pos, is_id = ('сотрудника деканата', is_user.deans_id) \
                            if (type(is_user) == DeansOfficeEmployee) \
                            else ('преподавателя', is_user.teacher_id) if (type(is_user) == Teacher) \
                            else ('студента', is_user.student_id) if (type(is_user) == Student) \
                            else ('администратора', is_user.admin_id)

                        if input(f'Подтвердите удаление {pos}: {is_user.name} {is_user.surname}\n -> y/n: ') == 'y':
                            print(self.del_user(is_id))
                        else:
                            print('Удаление отменено.')
                    else:
                        print('id в базе не обнаружен.')

                elif action in 'q':
                    print(f'До свидания!{self.name} {self.surname}\n')
                    break


class DeansOfficeEmployee:
    """Класс описывающий сотрудника деканата."""

    def __init__(self, name: str, surname: str, age: str, position: str) -> None:
        self.name = name
        self.surname = surname
        self.age = age
        self.position = position
        self.deans_id = get_id()
        Db_utils.insert_user(self.deans_id, pickle.dumps(self))

    def __str__(self) -> str:
        return f'Сотрудник деканата: {self.surname} {self.name}\n' \
               f'Возраст: {self.age}\nДолжность: {self.position}'

    @staticmethod
    def get_student_progress(student_id: str) -> str:
        """Возвращает успеваемость по предметам конкретного студента."""

        return pickle.loads(Db_utils.select_user(student_id)).get_my_progress()

    def deans_interface(self) -> None:
        """Интерфейс пользователя - сотрудник деканата."""

        while True:
            action = input('Введите номер действия:'
                           '\n\t1.Посмотреть успеваемость студента\n\tЧтобы выйти введите - q\n -> : ').lower()
            if action == '1':
                data_student = Db_utils.select_user(input('Введите id студента: '))
                if data_student:
                    student = pickle.loads(data_student)
                    if student and type(student) is Student:
                        print(self.get_student_progress(student.student_id))
                    else:
                        print('Указанный id не принадлежит студенту.')
                else:
                    print('id в базе не обнаружен.')

            elif action in 'q':
                print(f'До свидания!{self.name} {self.surname}\n')
                break


class Teacher:
    """Класс описывающий преподавателя."""

    def __init__(self, name: str, surname: str, age: str, subject: str) -> None:
        self.name = name
        self.surname = surname
        self.age = age
        self.subject = subject
        self.teacher_id = get_id()
        Db_utils.insert_user(self.teacher_id, pickle.dumps(self))

    def __str__(self) -> str:
        return f'Преподаватель: {self.surname} {self.name}\nВозраст: {self.age}\nПредмет: {self.subject}'

    def set_rate(self, student_id: str, rate: str) -> None:
        """Метод позволяющий преподавателю поставить оценку студенту."""

        data = Db_utils.select_user(student_id)
        if data:
            student = pickle.loads(data)

            if self.subject in student.my_rate.keys():
                student.my_rate.get(self.subject).append(rate)
            else:
                student.my_rate[self.subject] = [rate]

            Db_utils.update_user(student.student_id, pickle.dumps(student))

    def teacher_interface(self) -> None:
        """Интерфейс пользователя - преподаватель."""

        while True:
            action = input('Введите номер действия:'
                           '\n\t1.Поставить оценку студенту\n\tЧтобы выйти введите - q\n -> : ').lower()
            if action == '1':
                data_student = Db_utils.select_user(input('Введите id студента: '))
                if data_student:
                    student = pickle.loads(data_student)

                    if student and type(student) is Student:
                        rate = input('Введите оценку: ')
                        self.set_rate(student.student_id, rate)
                        print('Оценка сохранена.')
                    else:
                        print('Указанный id не принадлежит студенту.')

                else:
                    print('id в базе не обнаружен.')

            elif action in 'q':
                print(f'До свидания!{self.name} {self.surname}\n')
                break


class Student:
    """Класс описывающий студента."""

    def __init__(self, name: str, surname: str, age: str, faculty: str, department: str) -> None:
        self.student_id = get_id()
        self.name = name
        self.surname = surname
        self.age = age
        self.faculty = faculty
        self.department = department
        self.my_rate = {}
        Db_utils.insert_user(self.student_id, pickle.dumps(self))

    def __str__(self) -> str:
        return f'Студент: {self.surname} {self.name}\nВозраст: {self.age}' \
               f'\nФакультет: {self.faculty}\nКафедра: {self.department}'

    def get_my_progress(self) -> str:
        """Метод возвращает информацию о студенте и его успеваемость в виде строки."""
        line = f'{self.__str__()}\nУспеваемость:\n'
        for subject in self.my_rate.keys():
            line += f'    {subject}: {self.my_rate.get(subject)}\n'
        return line

    def student_interface(self) -> None:
        """Интерфейс пользователя - студент."""
        print(self.get_my_progress())


if __name__ == '__main__':

    Db_utils.create_table()
    # admin = Admin('Admin', 'Admin', '99', admin_id='12345', password='admin')
    # Для создания нового файла БД(старый удалить) раскомментировать строку выше, входные данные admin
    # изменить на ваше усмотрение, для повторного и последующих запусков закомментировать строку admin
    # для исключения конфликта уникальности id

    while True:
        data_user = Db_utils.select_user(input('Введите ваш id: '))
        if data_user:
            user = pickle.loads(data_user)
            print(f'Здравствуйте! {user.name} {user.surname}\n')

            if type(user) is Admin:
                user.admin_interface()

            elif type(user) is DeansOfficeEmployee:
                user.deans_interface()

            elif type(user) is Teacher:
                user.teacher_interface()

            elif type(user) is Student:
                user.student_interface()
        else:
            print('id в базе не обнаружен.')
