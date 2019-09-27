from tkinter import *
from random import randint

main_window = Tk()


class MineButton(object):
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.button = Button(main_window, width=2, height=1, command=lambda r=self.row, c=self.column: button_function(r, c))



grid_width = 15
grid_height = 15
bomb_percentage = 2


def bomb_number(height, width, percent):
    number = int(height*width * percent/100)
    return number


def create_grid(height, width):
    grid_list = []
    for i in range(height):
        row_list = []
        for j in range(width):
            b = MineButton(i, j)
            row_list.append(b)
            row_list[j].button.grid(row=i, column=j)
        grid_list.append(row_list)
    return grid_list


def plant_mines(height, width, percent):
    number = bomb_number(height, width, percent)
    mines_list = []
    count = 0
    while count < number:
        random_row = randint(0, height-1)
        random_col = randint(0, width-1)
        new_mine = [random_row, random_col]
        if new_mine not in mines_list:
            mines_list.append(new_mine)
            count += 1
    return mines_list


def boundary_getter(height, width):
    top_left = [0, 0]
    top_right = [0, width - 1]
    bottom_left = [height - 1, 0]
    bottom_right = [height - 1, width - 1]

    top_row = []
    for i in range(1, width - 1):
        top_row.append([0, i])

    bottom_row = []
    for i in range(1, width - 1):
        bottom_row.append([width - 1, i])

    left_column = []
    for i in range(1, height - 1):
        left_column.append([i, 0])

    right_column = []
    for i in range(1, height - 1):
        right_column.append([i, height - 1])
    return top_left, top_right, bottom_left, bottom_right, top_row, bottom_row, left_column, right_column


def surround_mine(coord, height, width):
    top_left, top_right, bottom_left, bottom_right, top_row, bottom_row, left_column, right_column = boundary_getter(height, width)
    if coord == top_left:
        surround = [[0, 1], [1, 0], [1, 1]]
    elif coord == top_right:
        surround = [[0, width - 2], [1, width - 2], [1, height - 1]]
    elif coord == bottom_left:
        surround = [[height - 1, 1], [height - 2, 1], [height - 2, 0]]
    elif coord == bottom_right:
        surround = [[height - 1, width - 2], [height - 2, width - 2], [height - 2, width - 1]]
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


grid = create_grid(grid_height, grid_width)
mines_list = plant_mines(grid_height, grid_width, bomb_percentage)



def button_function(row, column):
    label0 = Label(main_window, text="")
    label1 = Label(main_window, text=1, fg="#FF8C00")
    label2 = Label(main_window, text=2, fg="#FF0000")
    label3 = Label(main_window, text=3, fg="#006400")
    label4 = Label(main_window, text=4, fg="#008B8B")
    label5 = Label(main_window, text=5, fg="#191970")
    label6 = Label(main_window, text=6, fg="#8B4513")
    label7 = Label(main_window, text=7, fg="#696969")
    label8 = Label(main_window, text=8, fg="#000000")
    count = 0
    surround_list = surround_mine([row, column], grid_height, grid_width)
    for i in surround_list:
        if i in mines_list:
            count += 1
    grid[row][column].button.grid_remove()
    if count == 0:
        label0.grid(row=row, column=column)
    if count == 1:
        label1.grid(row=row, column=column)
    if count == 2:
        label2.grid(row=row, column=column)
    if count == 3:
        label3.grid(row=row, column=column)
    if count == 4:
        label4.grid(row=row, column=column)
    if count == 5:
        label5.grid(row=row, column=column)
    if count == 6:
        label6.grid(row=row, column=column)
    if count == 7:
        label7.grid(row=row, column=column)
    if count == 8:
        label8.grid(row=row, column=column)











print(mines_list)






main_window.mainloop()
