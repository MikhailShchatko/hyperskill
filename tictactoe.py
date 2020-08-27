import random


class CellUpdateException(Exception):
    pass


class GameBoard:
    win_lines = [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)],
    ]

    def __init__(self, cells, player_1, player_2):
        self.player_1 = player_1
        self.player_2 = player_2
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        cells = cells.replace('_', ' ')
        cell_gen = (cell for cell in cells)
        for i in range(3):
            for j in range(3):
                self.board[i][j] = next(cell_gen)

    def __str__(self):
        out = ''
        edge = '---------'
        out += edge + '\n'
        for i in range(3):
            out += '| ' + ' '.join(self.board[i]) + ' |\n'
        out += edge
        return out

    def get_side(self):
        if str(self).count('X') == str(self).count('O'):
            return 'X'
        else:
            return 'O'

    def update_cell(self, x, y):
        if any(value not in range(1, 4) for value in (x, y)):
            raise CellUpdateException('Coordinates should be from 1 to 3!')
        if self.board[3 - y][x - 1] == ' ':
            self.board[3 - y][x - 1] = self.get_side()
        else:
            raise CellUpdateException('This cell is occupied! Choose another one!')

    def move_possible(self, x, y):
        if any(value not in range(1, 4) for value in (x, y)):
            return False
        if self.board[3 - y][x - 1] != ' ':
            return False
        return True

    def next_player_gen(self):
        while True:
            yield self.player_1
            yield self.player_2

    def get_game_status(self):
        if any(all(self.board[x][y] == 'X' for x, y in line) for line in self.win_lines):
            game_status = 'X wins'
        elif any(all(self.board[x][y] == 'O' for x, y in line) for line in self.win_lines):
            game_status = 'O wins'
        elif all(all(cell != ' ' for cell in line) for line in self.board):
            game_status = 'Draw'
        else:
            game_status = 'Game not finished'
        return game_status


def make_move_user(game_board):
    turn_completed = False
    while not turn_completed:
        try:
            x, y = map(int, input('Enter the coordinates: ').split())
            game_board.update_cell(x, y)
            turn_completed = True
        except CellUpdateException as e:
            print(e)
        except ValueError:
            print('You should enter numbers!')


def make_move_easy(game_board):
    turn_completed = False
    while not turn_completed:
        x = random.randint(1, 3)
        y = random.randint(1, 3)
        if game_board.move_possible(x, y):
            game_board.update_cell(x, y)
            turn_completed = True


def make_move_medium(game_board):
    final_x, final_y = -1, -1
    current_side = game_board.get_side()
    opposite_side = 'X' if current_side == 'O' else 'O'

    for win_line in game_board.win_lines:
        line = [game_board.board[x][y] for x, y in win_line]
        if line.count(current_side) == 2 and line.count(' ') == 1:
            final_x, final_y = win_line[line.index(' ')]
            break

    if final_x == -1 and final_y == -1:
        for win_line in game_board.win_lines:
            line = [game_board.board[x][y] for x, y in win_line]
            if line.count(opposite_side) == 2 and line.count(' ') == 1:
                final_x, final_y = win_line[line.index(' ')]
                break

    if final_x != -1 and final_y != -1:
        game_board.update_cell(final_y + 1, 3 - final_x)
    else:
        make_move_easy(game_board)


def make_move_hard(game_board):
    pass


def is_command_valid(command):
    available_players = ['user', 'easy', 'medium', 'hard']
    if command == 'exit':
        return True
    command_parts = command.split()
    if len(command_parts) != 3:
        return False
    if command_parts[0] == 'start' \
            and command_parts[1] in available_players \
            and command_parts[2] in available_players:
        return True
    return False


def main():
    while True:
        command = input('Input command: ')
        if not is_command_valid(command):
            print('Bad parameters!')
            continue
        if command == 'exit':
            break
        else:
            _, player_1, player_2 = command.split()

            cells = '_________'
            game_board = GameBoard(cells, player_1, player_2)
            player = game_board.next_player_gen()
            print(game_board)

            while game_board.get_game_status() == 'Game not finished':
                current_player = next(player)
                if current_player == 'user':
                    make_move_user(game_board)
                else:
                    print(f'Making move level "{current_player}"')
                if current_player == 'easy':
                    make_move_easy(game_board)
                if current_player == 'medium':
                    make_move_medium(game_board)
                if current_player == 'hard':
                    make_move_hard(game_board)
                print(game_board)
            print(game_board.get_game_status())


if __name__ == '__main__':
    main()
