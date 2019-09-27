from tkinter import *

main_window = Tk()


class MineButton(object):
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.button = Button(main_window, width=2, height=1, command=lambda r = self.row, c=self.column: button_function(r, c))






def create_grid(width, height):
    grid_list = []
    for i in range(height):
        row_list = []
        for j in range(width):
            b = MineButton(i, j)
            row_list.append(b)
            row_list[j].button.grid(row=i, column=j)
        grid_list.append(row_list)
    return grid_list


grid = create_grid(15, 15)


def button_function(row, column):
    label = Label(main_window, text=1)
    grid[row][column].button.grid_remove()
    label.grid(row=row, column=column)













main_window.mainloop()
