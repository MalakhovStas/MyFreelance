# Разработать программный модуль «Учет успеваемости студентов».
# Программный модуль предназначен для оперативного учета успеваемости
# студентов в сессию деканом, заместителями декана и сотрудниками деканата.
# Сведения об успеваемости студентов должны храниться в течение всего срока
# их обучения и использоваться при составлении справок о прослушанных
# курсах и приложений к диплому.
import pickle
import random

import db_utils

db_utils.create_table()


def get_id() -> str:
    """Генерирует случайным образом id пользователя, проверяет его на уникальность и возвращает id."""
    while True:
        is_id = random.randint(0, 99999)
        if not db_utils.select_id(is_id):
            return f'{is_id:05}'


class Admin:
    def __init__(self, name, surname, login, password):
        self.name = name
        self.surname = surname
        self.admin_id = 55555
        self.login = login
        self.password = password
        db_utils.insert_user(user_id=self.admin_id, user=pickle.dumps(self))
        print(f'{self}\n')

    def add_deans(self, name, surname, age, position):
        new_dean = DeansOfficeEmployee(name, surname, age, position)
        return f'Сотрудник деканата добавлен успешно id: {new_dean.deans_id}'

    def add_teacher(self, name, surname, age, subject):
        Teacher(name, surname, age, subject)

    def add_student(self, name, surname, age, faculty, department):
        Student(name, surname, age, faculty, department)


class DeansOfficeEmployee:
    """Класс описывающий сотрудника деканата."""

    def __init__(self, name: str, surname: str, age: int, position: str) -> None:
        self.name = name
        self.surname = surname
        self.age = age
        self.position = position
        self.deans_id = get_id()
        db_utils.insert_user(user_id=self.deans_id, user=pickle.dumps(self))
        print(f'{self}\n')

    def __str__(self) -> str:
        return f'Сотрудник деканата: {self.surname} {self.name}\n' \
               f'id: {self.deans_id}\n' \
               f'Возраст: {self.age}\n' \
               f'Должность: {self.position}'

    def get_student_progress(self, student_id: str) -> str:
        """Возвращает успеваемость по предметам конкретного студента."""
        return pickle.loads(db_utils.select_user(student_id)).get_my_progress()


class Teacher:
    """Класс описывающий преподавателя."""

    def __init__(self, name: str, surname: str, age: int, subject: str) -> None:
        self.name = name
        self.surname = surname
        self.age = age
        self.subject = subject

        self.teacher_id = get_id()
        db_utils.insert_user(user_id=self.teacher_id, user=pickle.dumps(self))
        print(f'{self}\n')

    def __str__(self) -> str:
        return f'Преподаватель: {self.surname} {self.name}\n' \
               f'id: {self.teacher_id}\nВозраст: {self.age}\nПредмет: {self.subject}'

    def set_rate(self, student_id: str, rate: str) -> None:
        """Метод позволяющий преподавателю поставить оценку студенту."""
        data = db_utils.select_user(student_id)
        if data:
            student = pickle.loads(data)

            if self.subject in student.my_rate.keys():
                student.my_rate.get(self.subject).append(rate)
                print('2я оценка')
            else:
                print('1я оценка')
                student.my_rate[self.subject] = [rate]

            db_utils.update_user(student.student_id, pickle.dumps(student))

        # self.subject.students[student_id].append(rate)


class Student:
    """Класс описывающий студента."""

    def __init__(self, name: str, surname: str, age: int, faculty: str, department: str) -> None:
        self.student_id = get_id()
        self.name = name
        self.surname = surname
        self.age = age
        self.faculty = faculty
        self.department = department
        self.my_rate = {}
        db_utils.insert_user(user_id=self.student_id, user=pickle.dumps(self))

        print(f'{self}\n')

    def get_my_progress(self) -> str:
        line = f'{self.__str__()}\nУспеваемость:\n'
        for subject in self.my_rate.keys():
            line += f'    {subject}: {self.my_rate.get(subject)}\n'
        return line

    def __str__(self) -> str:
        return f'Студент: {self.surname} {self.name}\nid: {self.student_id}\nВозраст: {self.age}\n' \
               f'Факультет: {self.faculty}\nКафедра: {self.department}'


# class Subject:
#     """Класс описывающий курс, предмет, приложение."""
#
#     def __init__(self, name) -> None:
#         self.name = name
#
#     def __str__(self) -> str:
#         return f'{self.name}'


if __name__ == '__main__':

    # maths = Subject('Математика')
    # russian = Subject('Русский язык')
    # english = Subject('Английский язык')
    # program = Subject('Программирование')
    admin = Admin('Пётр', 'Петров', login='admin', password='admin')
    dean = DeansOfficeEmployee('Иван', 'Иванов', 50, 'Декан')
    teach = Teacher('Юлия', 'Андреева', 30, 'Программирование')
    stud = Student('Семён', 'Семёнов', 20, 'Прикладное программирование', 'python')


    while True:
        user = db_utils.select_user(input('Введите ваш id: '))

        if user:
            user = pickle.loads(user)
            print(f'Здравствуйте! {user.name} {user.surname}\n')

            if type(user) is Admin:
                action = input('Выберите действие:\n1.Добавить сотрудника деканата\n'
                               '2.Добавить преподавателя\n3.Добавить студента\n : ')
                if action == '1':
                    name = input('Введите имя: ')
                    surname = input('Введите фамилию: ')
                    age = int(input('Введите возраст: '))
                    position = input('Введите должность: ')
                    print(user.add_deans(name, surname, age, position))

            elif type(user) is DeansOfficeEmployee:
                student = pickle.loads(db_utils.select_user(input('Введите id студента: ')))

                if student and type(student) is Student:
                    print(user.get_student_progress(student_id=student.student_id))
                else:
                    print('id в базе не обнаружен.')

            elif type(user) is Teacher:
                data = db_utils.select_user(input('Введите id студента: '))
                if data:
                    student = pickle.loads(data)
                    rate = input('Введите оценку: ')
                    user.set_rate(student_id=student.student_id, rate=rate)
                    print('Оценка сохранена')
                else:
                    print('id в базе не обнаружен.')

            elif type(user) is Student:
                print(user.get_my_progress())

        else:
            print('id в базе не обнаружен.')


    # class Department:
    #     """Класс описывающий кафедру."""
    #
    #     def __init__(self, name) -> None:
    #         self.name = name
    #         self.subjects = []
    #         # db_utils.insert_depatment(self.name, pickle.dumps([]))
    #         # self.subjects = pickle.loads(db_utils.select_dep_subjects(self.name))
    #
    #     # def set_subject(self, subject):
    #     #     subjects = pickle.loads(db_utils.select_dep_subjects(self.name))
    #     # db_utils.update_depatment(self.name, pickle.dumps(self.subjects.append(subject)))
    #
    #     def __str__(self) -> str:
    #         return f'Кафедра: {self.name}\n    Список предметов: {[subj.name for subj in self.subjects]}'

    # def get_all_students_progress(self):
    #     """Возвращает список всех студентов и их успеваемость по предметам."""
    #     line = ''
    #     for student_id in users.keys():
    #         line += users[student_id].get_my_progress()
    #     return line
#
# class Faculty:
#     """Класс описывающий факультет."""
#
#     def __init__(self, name) -> None:
#         self.name = name
#         self.departments = []
#
#     def __str__(self) -> str:
#         return f'Факультет: {self.name}\n    Список кафедр: {self.departments}'
#
#
