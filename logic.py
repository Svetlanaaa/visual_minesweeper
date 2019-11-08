import random


class Sapper:
    def __init__(self, ht=[], t=[], n=0):
        self.hidden_table = ht
        self.table = t
        self.undiscovered_bombs = n

    def new_game(self):
        self.hidden_table = []
        self.table = []
        self.undiscovered_bombs = 0

    # setting n_bombs bombs to hidden_table by random index
    def set_bombs(self, n_bombs):
        n = 0
        while n < n_bombs:
            x0 = random.randint(0, len(self.hidden_table) - 1)
            y0 = random.randint(0, len(self.hidden_table[0]) - 1)
            if self.hidden_table[x0][y0] != '*':
                self.hidden_table[x0][y0] = '*'
                n += 1
                self.update_cells_around_bomb(x0, y0)

    def update_cells_around_bomb(self, x0, y0):
        x = len(self.hidden_table)
        y = len(self.hidden_table[0])
        if x0 - 1 > -1:
            for j0 in range(y0 - 1, y0 + 2):
                if -1 < j0 < y and self.hidden_table[x0 - 1][j0] != '*':
                    self.hidden_table[x0 - 1][j0] += 1
        if x0 + 1 < x:
            for j0 in range(y0 - 1, y0 + 2):
                if -1 < j0 < y and self.hidden_table[x0 + 1][j0] != '*':
                    self.hidden_table[x0 + 1][j0] += 1
        if y0 - 1 > -1 and self.hidden_table[x0][y0 - 1] != '*':
            self.hidden_table[x0][y0 - 1] += 1
        if y0 + 1 < y and self.hidden_table[x0][y0 + 1] != '*':
            self.hidden_table[x0][y0 + 1] += 1

    def generate_hidden_table(self, n_bombs):
        self.set_bombs(n_bombs)

    def init_table(self,x,y,z):
        for i in range(x):
            self.hidden_table.append([0 for j in range(y)])
            self.table.append([' ' for j in range(y)])

        self.generate_hidden_table(z)
        return z

    def cells_around(self, i, j):
        x = len(self.hidden_table)
        y = len(self.hidden_table[0])
        res = []
        ind = [i-1, j, i-1, j-1, i-1, j+1, i+1, j, i+1, j-1, i+1, j+1, i, j-1, i, j+1]
        for k in range(0, len(ind), 2):
            i0, j0= ind[k:k+2]
            if 0 <= i0 < x and 0 <= j0 < y:
                res += [i0, j0]
        return res

    def open(self, i, j):
        if self.table[i][j] != ' ':
            return
        else:
            if self.hidden_table[i][j] == 0:
                cells = self.cells_around(i, j)
                while len(cells):
                    i0 = cells.pop(0)
                    j0 = cells.pop(0)
                    if self.table[i0][j0] != ' ': continue   #if has been opened
                    else:
                        self.table[i0][j0] = self.hidden_table[i0][j0]
                        if self.table[i0][j0] == 0:
                            cells += self.cells_around(i0,j0)
            else:
                self.table[i][j] = self.hidden_table[i][j]

    # open cell
    def left_click(self, x, y):
        if self.hidden_table[x][y] == '*':
            return -1
        else:
            self.open(x, y)
            return 1

    # set or set off flag of bomb
    def right_click(self, n, undiscovered_bombs, x, y):
        if self.table[x][y] == '*':              # set off flag of bomb
            n += 1
            if self.hidden_table[x][y] == '*': undiscovered_bombs += 1
            self.table[x][y] = ' '
            return n, undiscovered_bombs, 0
        else:
            if n != 0:                      # set flag of bomb
                n -= 1
                if self.hidden_table[x][y] == '*': undiscovered_bombs -= 1
                self.table[x][y] = '*'
                return n, undiscovered_bombs, 1
            else:
                return n, undiscovered_bombs, -1

    # get information about game for saving
    def save_game(self):
        res = ''
        for i in range(len(self.table)):
            for j in range(len(self.table[0])):
                res += str(self.table[i][j])
        res += '\n'
        for i in range(len(self.hidden_table)):
            for j in range(len(self.hidden_table[0])):
                res += str(self.hidden_table[i][j])
        return res
