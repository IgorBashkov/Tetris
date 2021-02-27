import numpy as np
from itertools import cycle


class Piece:
    mapper = {
        'I': (((0, 4), (1, 4), (2, 4), (3, 4)),
              ((0, 3), (0, 4), (0, 5), (0, 6))),
        'S': (((0, 4), (0, 5), (1, 3), (1, 4)),
              ((1, 4), (1, 5), (0, 4), (2, 5))),
        'Z': (((0, 4), (0, 5), (1, 5), (1, 6)),
              ((0, 5), (1, 5), (1, 4), (2, 4))),
        'L': (((0, 4), (1, 4), (2, 4), (2, 5)),
              ((0, 5), (1, 5), (1, 4), (1, 3)),
              ((0, 4), (0, 5), (1, 5), (2, 5)),
              ((0, 5), (0, 6), (0, 4), (1, 4))),
        'J': (((0, 5), (1, 5), (2, 5), (2, 4)),
              ((1, 5), (0, 5), (0, 4), (0, 3)),
              ((0, 5), (0, 4), (1, 4), (2, 4)),
              ((0, 4), (1, 4), (1, 5), (1, 6))),
        'O': (((0, 4), (1, 4), (1, 5), (0, 5)),),
        'T': (((0, 4), (1, 4), (2, 4), (1, 5)),
              ((0, 4), (1, 3), (1, 4), (1, 5)),
              ((0, 5), (1, 5), (2, 5), (1, 4)),
              ((0, 4), (0, 5), (0, 6), (1, 5)))
    }

    def __init__(self, name='O'):
        self.size = (4, 10)
        self.array = np.zeros(self.size, dtype=bool)
        self.rotator = cycle(Piece.mapper[name])
        self.cursor_x = 0
        self.cursor_y = -1
        self.board_x_left = 0
        self.board_x_right = 0
        self.max_y = 10
        self.board_y = 10
        self.floor = self.size[0]
        self.real_width = self.size[1]
        self.turn()
        # self.get_board_y()

    def get_board_y(self):
        self.board_y = self.max_y - self.floor - 1

    def turn(self):
        self.array[np.nonzero(self.array)] = False
        for i in next(self.rotator):
            self.array[i] = True
        self.board_x_left = 0 - min(np.nonzero(self.array)[1])
        self.board_x_right = self.size[1] - max(np.nonzero(self.array)[1]) - 1
        self.floor = max(np.nonzero(self.array)[0])
        self.real_width = max(np.nonzero(self.array)[1]) - min(np.nonzero(self.array)[1])
        self.get_board_y()
        self.down()

    def left(self):
        if self.board_x_left != self.cursor_x:
            self.cursor_x -= 1
        self.down()

    def right(self):
        if self.cursor_x != self.board_x_right:
            self.cursor_x += 1
        self.down()

    def down(self):
        if self.cursor_y != self.board_y:
            self.cursor_y += 1

    """def move(self, direction):
        move_dict = {
            'rotate': self.turn,
            'down': self.down,
            'left': self.left,
            'right': self.right,
        }
        if self.cursor_y != self.board_y:
            move_dict[direction]()"""

    def __repr__(self):
        return '\n'.join([' '.join(map(lambda e: '-' if not e else '0', i)) for i in self.array])


class Field:
    def __init__(self, width=10, height=5):
        self.width = width
        self.height = height
        self.field = np.zeros((height, width), dtype=bool)
        self.result = np.copy(self.field)
        self.piece = Piece()
        self.stop = False
        self.over = False

    def add_piece(self, piece):
        self.piece = piece
        self.stop = False
        self.piece.max_y = self.height
        self.piece.get_board_y()
        self.update()

    def clear_field(self):
        self.field[np.nonzero(self.field)] = False

    def add_piece_from_input(self):
        self.add_piece(Piece(input()))

    def command(self, command):
        move_dict = {
            'rotate': self.piece.turn,
            'down': self.piece.down,
            'left': self.piece.left,
            'right': self.piece.right,
            'piece': self.add_piece_from_input,
        }
        if not self.stop or command == 'piece':  # self.piece.cursor_y != self.piece.board_y:
            move_dict[command]()

    def remove_complete(self):
        for n, line in enumerate(self.result):
            if np.zeros(line):
                pass


    def update(self):
        self.clear_field()
        if not self.stop:
            for n, i in enumerate(range(self.piece.cursor_y, self.piece.cursor_y + self.piece.size[0])):
                for m, j in enumerate(range(self.piece.cursor_x, self.piece.cursor_x + self.piece.size[1])):
                    self.field[i % self.height, j % self.width] = self.piece.array[n, m]
        if np.nonzero(self.field[-1])[0].size > 0 or np.nonzero(self.field[:-1] & self.result[1:])[0].size > 0:
            self.result = self.field | self.result
            self.clear_field()
            self.stop = True
            if np.nonzero(self.result[0])[0].size > 0:
                self.over = True

    def __repr__(self):
        return '\n'.join([' '.join(map(lambda e: '-' if not e else '0', i)) for i in self.field | self.result])


def run():
    field_size = tuple(map(int, input().split()))
    # print()

    field = Field(*field_size)

    print(field, end='\n\n')
    # field.add_piece_from_input()
    # print(field, end='\n\n')
    command = input()
    while command != 'exit' and not field.over:
        field.command(command)
        field.update()
        print(field, end='\n\n', sep='')
        command = input()
    if field.over:
        print(field, end='\n\n', sep='')
        print('Game Over!')


if __name__ == '__main__':
    run()
