# Задание-2, вариант-1
# Даны три целых числа. Выбрать из них те, которые принадлежат интервалу
# [1,3]

num_1 = 2
num_2 = 12
num_3 = 1
print(*[num for num in (num_1, num_2, num_3) if num in range(1, 4)])
