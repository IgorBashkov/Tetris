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
        self.turn()

    def turn(self):
        self.array[np.nonzero(self.array)] = False
        for i in next(self.rotator):
            self.array[i] = True
        self.board_x_left = 0 - min(np.nonzero(self.array)[1])
        self.board_x_right = self.size[1] - max(np.nonzero(self.array)[1]) - 1
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
        self.cursor_y += 1

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

    def add_piece_from_input(self):
        self.piece = Piece(input())
        self.stop = False
        self.update()

    def command(self, command):
        move_dict = {
            'rotate': self.piece.turn,
            'down': self.piece.down,
            'left': self.piece.left,
            'right': self.piece.right,
            'piece': self.add_piece_from_input,
            'break': self.remove_complete,
        }
        if not self.stop or command in ('piece', 'break'):
            move_dict.get(command, self.pass_method)()
        self.update()

    def remove_complete(self):
        for n, line in enumerate(self.result):
            if line.all():
                self.result[n] = False
                self.result[1:n+1] = self.result[0:n]

    @staticmethod
    def pass_method():
        pass

    def update(self):
        self.field[:] = False
        if not self.stop:
            # this loop require rewriting
            for n, i in enumerate(range(self.piece.cursor_y, self.piece.cursor_y + self.piece.size[0])):
                for m, j in enumerate(range(self.piece.cursor_x, self.piece.cursor_x + self.piece.size[1])):
                    self.field[i % self.height, j % self.width] = self.piece.array[n, m]
        if self.field[-1].any() or (self.field[:-1] & self.result[1:]).any():
            self.result = self.field | self.result
            self.field[:] = False
            self.stop = True
            if self.result[0].any():
                self.over = True

    def __repr__(self):
        return '\n'.join([' '.join(map(lambda e: '-' if not e else '0', i)) for i in self.field | self.result])


def run():
    field = Field(*tuple(map(int, input().split())))
    print(field, end='\n\n')
    command = input()
    while command != 'exit' and not field.over:
        field.command(command)
        print(field, end='\n\n', sep='')
        command = input()
    if field.over:
        print(field, end='\n\n', sep='')
        print('Game Over!')


if __name__ == '__main__':
    run()
