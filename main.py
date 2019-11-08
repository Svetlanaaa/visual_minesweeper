from tkinter import *
from tkinter.messagebox import *
from functools import partial
from tkinter import filedialog as fd
import sapper


class VisualSapper:
    def __init__(self):
        self.x = 0      # number of rows
        self.y = 0      # number of columns
        self.z = 0      # number of bombs
        self.sapper = sapper.Sapper()
        self.buttons = []   # list of buttons - cells of playing field
        self.unopened_bombs = 0

        # creating a menu
        menu = Menu(root)
        root.config(menu=menu)

        item = Menu(menu, tearoff=0)
        menu.add_cascade(label='Меню', menu=item)
        item.add_command(label="Сохранить игру", command=self.save_game)
        item.add_command(label="Открыть игру", command=self.open_game)
        item.add_command(label="Правила игры", command=self.open_rules)
        item.add_separator()
        item.add_command(label="Выход", command=lambda: root.quit())

        # creating a frame for settings
        settings = Frame(root, width=750, bg='mint cream')
        Label(settings, text="Размеры игрового поля", bg='mint cream', font="Arial 12" ).grid(row=0, column=0, columnspan=10)
        Label(settings, text="X = ",bg='mint cream', font="Arial 12").grid(row=1, column=0, sticky="e")
        Label(settings, text="Y = ",bg='mint cream', font="Arial 12").grid(row=2, column=0, sticky="e")
        Label(settings, text="Число бомб = ",bg='mint cream', font="Arial 12").grid(row=3, column=0, sticky="e")

        self.entry_x = Entry(settings, width=5)
        self.entry_x.grid(row=1, column=1, sticky="w")
        self.entry_y = Entry(settings, width=5)
        self.entry_y.grid(row=2, column=1, sticky="w")
        self.entry_z = Entry(settings, width=5)
        self.entry_z.grid(row=3, column=1, sticky="w")

        button = Button(settings, text="Новая игра", bg='LightCyan2', font="Arial 10")
        button.bind("<Button-1>", self.init_table)
        button.grid(row=5, column=0, columnspan=4)
        settings.pack(side=RIGHT, fill=Y)

        # a frame for playing field
        self.game_table = None

    # reading a file with saved game
    def read_file(self):
        file_name = fd.askopenfilename()
        f = open(file_name)
        self.x = int(f.readline())
        self.y = int(f.readline())
        self.z = int(f.readline())
        self.unopened_bombs = int(f.readline())
        table = f.readline()
        hidden_table = f.readline()
        ht, t = [], []
        for i in range(self.x):
            ht.append([])
            t.append([])
            for j in range(self.y):
                ind = i * self.y + j
                ht[i].append(self.read_char(hidden_table, ind))
                t[i].append(self.read_char(table, ind))
        f.close()
        return ht, t

    def read_char(self, table, i):
        ch = table[i]
        if ch == ' ' or ch == '*':
            return ch
        else:
            return int(ch)

    # creating playing field by buttons
    def create_game_field(self):
        self.game_table = Frame(root)

        for _ in range(self.x):
            self.buttons.append([Button(self.game_table, width=1, heigh=1, bg='LightCyan') for i in range(self.y)])
        for i in range(self.x):
            for j in range(self.y):
                b = self.buttons[i][j]
                b.configure(text=self.sapper.table[i][j])
                b.bind("<Button-1>", partial(self.open_cell, i, j))
                b.bind("<Button-3>", partial(self.set_bomb, i, j))
                b.grid(row=i, column=j, columnspan=1, rowspan=1)

        change_win_size(root, self.y * 36 + 230, [150, self.x * 28][self.x * 28 >= 150])

        self.game_table.pack(side=LEFT, anchor=NW)
        self.update_buttons()

    # cleaning playing field for new game
    def clean_field(self):
        if self.game_table:
            self.game_table.pack_forget()
        self.buttons = []

    # opening saved game
    def open_game(self):
        hidden_table, table = self.read_file()

        self.clean_field()
        self.sapper = sapper.Sapper(hidden_table, table, self.unopened_bombs)
        self.create_game_field()

    # saving information about game
    def save_game(self):
        file_name = fd.asksaveasfilename(filetypes=(("TXT files", "*.txt"), ("All files", "*.*") ))
        f = open(file_name, 'w')
        s = self.sapper.save_game()
        s = str(self.x) +'\n' + str(self.y) + '\n' + str(self.z) + '\n' + str(self.unopened_bombs) + '\n'+ s
        f.write(s)
        f.close()

    # generate random game
    def init_table(self, event):
        self.clean_field()
        self.sapper.new_game()
        try:
            self.x = int(self.entry_x.get())
            self.y = int(self.entry_y.get())
            self.z = int(self.entry_z.get())
            self.unopened_bombs = self.z
        except ValueError:
            showerror("Ошибка!", "Заполните поля.")

        try:
            if 35 < self.x < 1 or 35 < self.y < 1 or self.x * self.y < self.z < 1:
                showerror("Ошибка!", "Введите корректные параметры игры.")
            else:
                self.sapper.init_table(self.x, self.y, self.z)
                self.create_game_field()
        except ValueError:
            showerror("Ошибка!", "Параметры игры должны быть числами.")

    # blocking buttons after winning or losing
    def block_buttons(self):
        for i in range(self.x):
            for j in range(self.y):
                self.buttons[i][j].configure(state=DISABLED)

    def update_buttons(self, end=False):
        if not end:
            table = self.sapper.table
        else:
            table = self.sapper.hidden_table
        for i in range(len(self.buttons)):
            for j in range(len(self.buttons[0])):
                self.buttons[i][j].configure(text=table[i][j])

    def open_cell(self, i, j, event):
        if self.buttons[i][j]['state'] == 'disabled':
            return
        result = self.sapper.left_click(i, j)
        if result == -1:
            showinfo("БУУУУУМ!", "Вы проиграли...")
            self.update_buttons(True)
            self.block_buttons()
        else:
            self.update_buttons()

    def set_bomb(self, i, j, event):
        if self.buttons[i][j]['state'] == 'disabled':
            return
        self.z, self.unopened_bombs, result = self.sapper.right_click(self.z, self.unopened_bombs, i, j)
        if result == -1:
            showerror("Ошибка", "Вы уже использовали все доступные метки бомб. "
                                "Уберите метку из другой ячейки, чтобы добавить в другое место.")
        else:
            if self.unopened_bombs == 0:
                showinfo("Поздравляем!", "Вы выиграли!")
                self.update_buttons(True)
                self.block_buttons()
            else:
                if result == 0:
                    self.update_buttons()
                    showinfo("Поздравляем!",
                             "Вы успешно убрали метку бомбы. У вас осталось " + str(self.z) + " свободных меток.")
                else:
                    showinfo("Поздравляем!",
                             "Вы успешно установили метку бомбы. У вас осталось " + str(self.z) + " свободных меток.")
                    self.update_buttons()

    def open_rules(self):
        win = Toplevel(root)
        win.title('Правила')
        l = Label(win, text='«Сапер» — компьютерная игра-головоломка.\n Игровое поле разделено на ячейки, часть которых заминированы.\n'
                        'Целью игры является как можно быстрее исследовать минное поле, не сдетонировав ни одной мины.\n'
                            'Для открытия ячейки нажмите левой кнопкой мыши на выбранную ячейку.\n'
                        'Чтобы установить или снять метку бомбы - нажмите на ячейку правой кнопкой мыши.\nВ случае ошибки и открытия ячейки с бомбой, произойдет взрыв,'
                        ' и игра будет окончена.\nЧисло в ячейке показывает, сколько мин скрыто вокруг данной ячейки.\n'
                            'Это число поможет понять вам, где находятся безопасные ячейки, а где находятся бомбы.\n'
                            'Чтобы победить, отметьте все ячейки с бомбами при помощи меток.\nУдачи!')
        l.configure(width=100, height=150, justify=CENTER, bg='mint cream', font="Arial 12")
        l.pack()
        change_win_size(win, 1000, 250)


def change_win_size(win, x, y):
    default_x = root.winfo_screenwidth() // 2
    default_y = root.winfo_screenheight() //2
    win.geometry("%dx%d+%d+%d" % (x, y, default_x - x//2, default_y - y//2))


root = Tk()
root.title('Сапер')
root.configure(background='mint cream')
change_win_size(root, 230, 150)

s = VisualSapper()

root.mainloop()