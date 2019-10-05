from tkinter import *
from random import randint
import keyboard


class Game(object):
    play_again = True
    restart = False
    flagged_number = 0

    def __init__(self, height=15, width=15, percent=20):
        self.window = Tk()
        self.window.title("Minesweeper")
        self.mine_frame = Frame(self.window)
        self.height = height
        self.width = width
        self.percent = percent
        self.mine_field = []
        self.mines_list = []
        self.timer = -1
        self.is_timer = 1
        self.checked_list = []

        self.mine_number = int(self.height * self.width * self.percent / 100)
        self.covered = self.height * self.width

        game_frame = Frame(self.window)
        game_frame.grid(row=0, column=0, sticky=W)
        new_game_button = Button(game_frame, text="New Game", command=self.game_starter, padx=9)
        restart_game_button = Button(game_frame, text="Restart Game", command=self.restart_game)
        quit_game_button = Button(game_frame, text="Quit Game", command=self.quit_game, padx=9)
        new_game_button.pack(anchor="w")
        restart_game_button.pack(anchor="w")
        quit_game_button.pack(anchor="w")

        options_frame = Frame(self.window)
        options_frame.grid(row=0, column=1, sticky=E)
        height_label = Label(options_frame, text="Height (1-30)", anchor="e")
        width_label = Label(options_frame, text="Width (1-60)", anchor="e")
        percent_label = Label(options_frame, text="Percentage (1-99)", anchor="e")
        self.height_entry = Entry(options_frame, width=5)
        self.width_entry = Entry(options_frame, width=5)
        self.percent_entry = Entry(options_frame, width=5)
        height_label.grid(row=0, column=0, sticky=E)
        width_label.grid(row=1, column=0, sticky=E)
        percent_label.grid(row=2, column=0, sticky=E)
        self.height_entry.grid(row=0, column=1, sticky=E)
        self.width_entry.grid(row=1, column=1, sticky=E)
        self.percent_entry.grid(row=2, column=1, sticky=E)

        self.height_entry.bind("<Return>", self.height_changer)
        self.width_entry.bind("<Return>", self.width_changer)
        self.percent_entry.bind("<Return>", self.percent_changer)

        self.number_bar = Label(self.window, text="Number of mines: "+str(self.mine_number).zfill(3), relief=SUNKEN, bd=1)
        self.flagged_bar = Label(self.window, text="Mines flagged: "+str(self.flagged_number).zfill(3), relief=SUNKEN, bd=1)
        self.covered_bar = Label(self.window, text="Spaces covered: "+str(self.covered).zfill(3), relief=SUNKEN, bd=1)
        self.timer_bar = Label(self.window, text="Time (secs): "+str(self.timer).zfill(4), relief=SUNKEN, bd=1)

    def mines_status(self):
        self.number_bar.destroy()
        self.number_bar = Label(self.window, text="Number of mines: "+str(self.mine_number).zfill(3), relief=SUNKEN, bd=1)
        self.number_bar.grid(row=3, sticky=W)

    def timer_status(self):
        self.timer += 1
        self.timer_bar = Label(self.window, text="Time (secs): "+str(self.timer).zfill(4), relief=SUNKEN, bd=1)
        self.timer_bar.grid(row=3, column=1, sticky=E)
        self.is_timer = self.window.after(1000, self.timer_status)

    def cover_status(self):
        self.covered_bar.destroy()
        self.covered_bar = Label(self.window, text="Spaces covered: "+str(self.covered).zfill(3), relief=SUNKEN, bd=1)
        self.covered_bar.grid(row=4, sticky=W)

    def flag_status(self):
        self.flagged_bar.destroy()
        self.flagged_bar = Label(self.window, text="Mines flagged: "+str(self.flagged_number).zfill(3), relief=SUNKEN, bd=1)
        self.flagged_bar.grid(row=4, column=1, sticky=E)

    def list_maker(self, minimum, maximum):
        new_list = []
        for i in range(minimum, maximum + 1):
            new_list.append(str(i))
        return new_list

    def height_changer(self, event):
        height_range = self.list_maker(2, 30)
        if self.height_entry.get() not in height_range:
            self.height = 15
            self.height_entry.delete("0", "end")
        else:
            self.height = int(self.height_entry.get())
            keyboard.press_and_release("tab")
            print(self.height)

    def width_changer(self, event):
        width_range = self.list_maker(2, 60)
        if self.width_entry.get() not in width_range:
            self.width = 15
            self.width_entry.delete("0", "end")
        else:
            self.width = int(self.width_entry.get())
            keyboard.press_and_release("tab")
            print(self.width)

    def percent_changer(self, event):
        percent_range = self.list_maker(0, 100)
        if self.percent_entry.get() not in percent_range:
            self.percent = 20
            self.percent_entry.delete("0", "end")
        else:
            self.percent = int(self.percent_entry.get())

    def boundary_getter(self):
        top_left = [0, 0]
        top_right = [0, self.width - 1]
        bottom_left = [self.height - 1, 0]
        bottom_right = [self.height - 1, self.width - 1]

        top_row = []
        for i in range(1, self.width - 1):
            top_row.append([0, i])
        bottom_row = []
        for i in range(1, self.width - 1):
            bottom_row.append([self.width - 1, i])
        left_column = []
        for i in range(1, self.height - 1):
            left_column.append([i, 0])
        right_column = []
        for i in range(1, self.height - 1):
            right_column.append([i, self.height - 1])
        return top_left, top_right, bottom_left, bottom_right, top_row, bottom_row, left_column, right_column

    def surround_mine(self, coord):
        top_left, top_right, bottom_left, bottom_right, \
                       top_row, bottom_row, left_column, right_column = self.boundary_getter()
        if coord == top_left:
            surround = [[0, 1], [1, 0], [1, 1]]
        elif coord == top_right:
            surround = [[0, self.width - 2], [1, self.width - 2], [1, self.height - 1]]
        elif coord == bottom_left:
            surround = [[self.height - 1, 1], [self.height - 2, 1], [self.height - 2, 0]]
        elif coord == bottom_right:
            surround = [[self.height - 1, self.width - 2], [self.height - 2, self.width - 2],
                        [self.height - 2, self.width - 1]]
        elif coord in top_row:
            surround = [[coord[0], coord[1] - 1], [coord[0], coord[1] + 1], [coord[0] + 1, coord[1] - 1],
                        [coord[0] + 1, coord[1]], [coord[0] + 1, coord[1] + 1]]
        elif coord in bottom_row:
            surround = [[coord[0], coord[1] - 1], [coord[0], coord[1] + 1], [coord[0] - 1, coord[1] - 1],
                        [coord[0] - 1, coord[1]], [coord[0] - 1, coord[1] + 1]]
        elif coord in left_column:
            surround = [[coord[0] + 1, coord[1]], [coord[0] - 1, coord[1]], [coord[0] - 1, coord[1] + 1],
                        [coord[0], coord[1] + 1], [coord[0] + 1, coord[1] + 1]]
        elif coord in right_column:
            surround = [[coord[0] + 1, coord[1]], [coord[0] - 1, coord[1]], [coord[0] - 1, coord[1] - 1],
                        [coord[0], coord[1] - 1], [coord[0] + 1, coord[1] - 1]]
        else:
            surround = [[coord[0], coord[1] - 1], [coord[0], coord[1] + 1], [coord[0] - 1, coord[1] - 1],
                        [coord[0] - 1, coord[1]], [coord[0] - 1, coord[1] + 1], [coord[0] + 1, coord[1] - 1],
                        [coord[0] + 1, coord[1]], [coord[0] + 1, coord[1] + 1]]
        return surround

    def mine_counter(self, coord_list):
        count = 0
        for i in coord_list:
            if i in self.mines_list:
                count += 1
        return count

    def win_switch(self):
        if self.covered == self.mine_number:
            return True

    def game_starter(self):
        self.mine_number = int(self.height * self.width * self.percent / 100)
        self.restart = False
        self.window.after_cancel(self.is_timer)
        self.mine_frame.destroy()
        self.mine_frame = Frame(self.window)
        self.mine_field = []
        for i in range(self.height):
            row_list = []
            for j in range(self.width):
                b = MineButton(i, j, self.mine_frame)
                row_list.append(b)
                row_list[j].button.grid(row=i, column=j)
            self.mine_field.append(row_list)
            print(self.mine_field)

        self.mines_list = []
        count = 0
        while count < self.mine_number:
            random_row = randint(0, self.height - 1)
            random_col = randint(0, self.width - 1)
            new_mine = [random_row, random_col]
            if new_mine not in self.mines_list:
                self.mines_list.append(new_mine)
                print(new_mine)
                count += 1

        self.flagged_number = 0
        self.flag_status()
        self.mine_number = int(self.height * self.width * self.percent / 100)
        self.mines_status()
        self.covered = self.width * self.height
        self.cover_status()
        self.checked_list = []

        self.mine_frame.grid(row=1, columnspan=2, sticky=W)
        self.timer = -1
        self.timer_status()

    def kill_game(self):
        self.window.destroy()
        self.play_again = False
        self.restart = False

    def quit_game(self):
        self.mine_frame.destroy()
        self.window.after_cancel(self.is_timer)
        self.covered_bar.destroy()
        self.flagged_bar.destroy()
        self.timer_bar.destroy()
        self.play_again = True
        self.restart = False
        self.covered = 0
        self.flagged_number = 0
        self.checked_list = []

    def restart_game(self):
        self.mine_number = int(self.height * self.width * self.percent / 100)
        self.window.after_cancel(self.is_timer)
        self.restart = True
        self.mine_frame.destroy()
        self.mine_frame = Frame(self.window)
        self.mine_field = []
        for i in range(self.height):
            row_list = []
            for j in range(self.width):
                b = MineButton(i, j, self.mine_frame)
                row_list.append(b)
                row_list[j].button.grid(row=i, column=j)
            self.mine_field.append(row_list)

        self.flagged_number = 0
        self.flag_status()
        self.mine_number = int(self.height * self.width * self.percent / 100)
        self.mines_status()
        self.covered = self.width * self.height
        self.cover_status()
        self.checked_list = []
        self.mine_frame.grid(row=1, columnspan=3)
        self.timer = -1
        self.timer_status()


class MineButton(object):

    def __init__(self, row, column, frame):
        self.row = row
        self.column = column
        self.frame = frame
        self.button = Button(frame, width=2, height=1,
                             command=lambda r=self.row, c=self.column: button_function(r, c), pady=-1)
        self.button.bind("<Button-3>", self.flag_placer)
        self.state = True  # True means button False means flag
        self.button.bind("<Enter>", self.on_enter)
        self.button.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self.button["background"] = "grey"

    def on_leave(self, event):
        self.button["background"] = "SystemButtonFace"

    def flag_placer(self, event):
        flag_image = PhotoImage(file="Flag.gif")
        if not self.state:
            self.button = Button(self.frame, width=2, height=1,
                                 command=lambda r=self.row, c=self.column: button_function(r, c), pady=-1)
            self.button.grid(row=self.row, column=self.column)
            self.button.bind("<Button-3>", self.flag_placer)
            this_game.flagged_number -= 1
            this_game.flag_status()
            self.state = True
        elif self.state:
            self.button = Label(self.frame, image=flag_image, relief=RAISED, width=18, height=17)
            self.button.image = flag_image
            self.button.grid(row=self.row, column=self.column)
            self.button.bind("<Button-3>", self.flag_placer)
            this_game.flagged_number += 1
            this_game.flag_status()
            self.state = False


def button_function(row, column):
    if [row, column] in this_game.mines_list:
        this_game.quit_game()
        boom_image = PhotoImage(file="DEAD.gif")
        this_game.mine_frame = Label(this_game.window, image=boom_image)
        this_game.mine_frame.image = boom_image
        this_game.mine_frame.grid(row=1, columnspan=2)
        return True
    else:
        this_game.checked_list.append([row, column])
        this_game.covered -= 1
        surround_list = this_game.surround_mine([row, column])
        count = this_game.mine_counter(surround_list)
        if not count_labeler(count, row, column):
            super_surround = [surround_list]
            for surr_lst in super_surround:
                for button in surr_lst:
                    if button not in this_game.checked_list:
                        new_surround = this_game.surround_mine(button)
                        new_count = this_game.mine_counter(new_surround)
                        if not count_labeler(new_count, button[0], button[1]):
                            super_surround.append(new_surround)
                        this_game.checked_list.append(button)
                        this_game.covered -= 1
        this_game.cover_status()
        if this_game.win_switch():
            this_game.quit_game()
            win_image = PhotoImage(file="NOTDEAD.gif")
            this_game.mine_frame = Label(this_game.window, image=win_image)
            this_game.mine_frame.image = win_image
            this_game.mine_frame.grid(row=1, columnspan=2)



def count_labeler(count, row, column):
    this_game.mine_field[row][column].button.grid_remove()
    number_border = GROOVE
    if count == 0:
        label0 = Label(this_game.mine_frame, text="", relief=number_border, width=2, height=1, padx=3, pady=2)
        label0.grid(row=row, column=column)
        return False
    elif count == 1:
        label1 = Label(this_game.mine_frame, text=1, fg="#2140EC", font=("none", 9, "bold"),
                       relief=number_border, width=2, height=1, padx=2)
        label1.grid(row=row, column=column)
    elif count == 2:
        label2 = Label(this_game.mine_frame, text=2, fg="#15B52F", font=("none", 9, "bold"),
                       relief=number_border, width=2, height=1, padx=2)
        label2.grid(row=row, column=column)
    elif count == 3:
        label3 = Label(this_game.mine_frame, text=3, fg="#FA4202", font=("none", 9, "bold"),
                       relief=number_border, width=2, height=1, padx=2)
        label3.grid(row=row, column=column)
    elif count == 4:
        label4 = Label(this_game.mine_frame, text=4, fg="#9B2DB6", font=("none", 9, "bold"),
                       relief=number_border, width=2, height=1, padx=2)
        label4.grid(row=row, column=column)
    elif count == 5:
        label5 = Label(this_game.mine_frame, text=5, fg="#24069E", font=("none", 9, "bold"),
                       relief=number_border, width=2, height=1, padx=2)
        label5.grid(row=row, column=column)
    elif count == 6:
        label6 = Label(this_game.mine_frame, text=6, fg="#0A6A4A", font=("none", 9, "bold"),
                       relief=number_border, width=2, height=1, padx=2)
        label6.grid(row=row, column=column)
    elif count == 7:
        label7 = Label(this_game.mine_frame, text=7, fg="#F91207", font=("none", 9, "bold"),
                       relief=number_border, width=2, height=1, padx=2)
        label7.grid(row=row, column=column)
    elif count == 8:
        label8 = Label(this_game.mine_frame, text=8, fg="#420E5A", font=("none", 9, "bold"),
                       relief=number_border, width=2, height=1, padx=2)
        label8.grid(row=row, column=column)
    return True


play_again = True
while play_again:
    this_game = Game(15, 15, 10)
    same_game = this_game
    restart = False
    while restart:
        print("restart")
        same_game.window.protocol("WM_DELETE_WINDOW", same_game.kill_game)
        same_game.window.mainloop()
        restart = same_game.restart
        play_again = same_game.play_again
    else:
        this_game.window.protocol("WM_DELETE_WINDOW", this_game.kill_game)
        this_game.window.mainloop()
        restart = this_game.restart
        play_again = this_game.play_again
