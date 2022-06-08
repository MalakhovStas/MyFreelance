import random


class Cell:
    def __init__(self, number, value=' '*5):
        self.number = number
        self.value = value


class Board:
    def __init__(self):
        self.dict_cells = {}
        for number_cell in range(1, 10):
            cell = Cell(number_cell)
            self.dict_cells[number_cell] = cell

    def view_board(self):
        line = "-" * 5 + "|" + "-" * 5 + "|" + "-" * 5
        print(f'\n{self.dict_cells[1].value}|{self.dict_cells[2].value}|{self.dict_cells[3].value}\n{line}\n'
              f'{self.dict_cells[4].value}|{self.dict_cells[5].value}|{self.dict_cells[6].value}\n{line}\n'
              f'{self.dict_cells[7].value}|{self.dict_cells[8].value}|{self.dict_cells[9].value}\n')

    def win_lines(self):
        win_lines = {'row_1': [self.dict_cells[1], self.dict_cells[2], self.dict_cells[3]],
                     'row_2': [self.dict_cells[4], self.dict_cells[5], self.dict_cells[6]],
                     'row_3': [self.dict_cells[7], self.dict_cells[8], self.dict_cells[9]],
                     'column_1': [self.dict_cells[1], self.dict_cells[4], self.dict_cells[7]],
                     'column_2': [self.dict_cells[2], self.dict_cells[5], self.dict_cells[8]],
                     'column_3': [self.dict_cells[3], self.dict_cells[6], self.dict_cells[9]],
                     'diagonal_1': [self.dict_cells[1], self.dict_cells[5], self.dict_cells[9]],
                     'diagonal_2': [self.dict_cells[3], self.dict_cells[5], self.dict_cells[7]],
                     }
        return win_lines


class Player:
    def __init__(self, name):
        self.name = name
        self.board = Board()
        self.num_step = 0

    def game(self):
        print(f'Привет, {self.name}, первый ход мой!')
        self.board.dict_cells[self.machine_logic()].value = '  0  '
        self.board.view_board()
        self.num_step += 1
        while True:
            while True:
                answer = int(input(f'В какую клетку пойдёте, {self.name}? '))
                if self.board.dict_cells[answer].value.isspace():
                    self.board.dict_cells[answer].value = '  x  '
                    if self.result() == 'stop game':
                        return
                    break
                else:
                    print(f'Клетка занята, {self.name} выберите другую клетку.')
            comp_move = self.machine_logic()
            print(f'А я пойду в {comp_move}-ую клетку.')
            self.board.dict_cells[comp_move].value = '  0  '
            if self.result() == 'stop game':
                return
            self.board.view_board()

    def machine_logic(self):
        if self.num_step == 0:
            return random.choice(range(1, 10))
        for i_num in range(4):
            for name_win_line, list_cells in self.board.win_lines().items():
                count_x, count_0, empty_cell = 0, 0, []
                for i_cell in list_cells:
                    if i_cell.value == '  0  ':
                        count_0 += 1
                    elif i_cell.value == '  x  ':
                        count_x += 1
                    else:
                        empty_cell.append(i_cell)
                if i_num == 0 and count_0 == 2 and empty_cell:
                    return empty_cell[0].number
                elif i_num == 1 and count_x == 2 and empty_cell:
                    return empty_cell[0].number
                elif i_num == 2 and count_0 == 1 and count_x == 0 and empty_cell:
                    return random.choice(empty_cell).number
                elif i_num == 3 and count_0 == 1 and count_x == 1 and empty_cell:
                    return empty_cell[0].number


    def result(self):
        for name_win_line, list_cells in self.board.win_lines().items():
            cnt_x, cnt_0 = 0, 0
            for i_cell in list_cells:
                if i_cell.value == '  0  ':
                    cnt_0 += 1
                elif i_cell.value == '  x  ':
                    cnt_x += 1
                if cnt_x == 3:
                    print(f'Поздравляю с победой {self.name}!')
                    for new_cell in list_cells:
                        new_cell.value = '  \033[34mx\033[0m  '
                    self.board.view_board()
                    return 'stop game'
                elif cnt_0 == 3:
                    print(f'Вы проиграли, {self.name}.')
                    for new_cell in list_cells:
                        new_cell.value = '  \033[31m0\033[0m  '
                    self.board.view_board()
                    return 'stop game'
        if not [val for val in self.board.dict_cells.values() if val.value == ' '*5]:
            self.board.view_board()
            print('Игра окончена - победила дружба!')
            return 'stop game'


my_player = Player('Сергей')
my_player.game()
