import chardet
import csv


def get_encoding(file):
    with open(file, 'rb') as f:
        tmp = chardet.detect(f.read())
        return tmp['encoding']


# with open("craft.recipes.csv", encoding='utf-8') as r_file:
#     # Создаем объект reader, указываем символ-разделитель ","
#     file_reader = csv.reader(r_file, delimiter=",")
#     # Счетчик для подсчета количества строк и вывода заголовков столбцов
#     count = 0
#     # Считывание данных из CSV файла
#     for row in file_reader:
#         print(row)
#         if count == 0:
#             # Вывод строки, содержащей заголовки для столбцов
#             print(f'Файл содержит столбцы: {", ".join(row)}')
#         else:
#             # Вывод строк
#             print(f'    {row[0]} - {row[1]} и он родился в {row[2]} году.')
#         count += 1
#     print(f'Всего в файле {count} строк.')






with open('craft.recipes.csv', 'r', encoding='utf-8') as file:
    data = file.read()

print(data)

print(get_encoding('craft.recipes.csv'))