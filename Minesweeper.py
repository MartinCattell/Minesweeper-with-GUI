from tkinter import *

main_window = Tk()


class MineButton(object):
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.button = Button(main_window, width=2, height=1)






def create_grid(width, height):
    grid_list = []
    for i in range(height):
        row_list = []
        for j in range(width):
            b = MineButton(i, j)
            b.button.bind("<Button-1>", button_function)
            row_list.append(b)
            row_list[j].button.grid(row=i, column=j)
        grid_list.append(row_list)
    return grid_list







def button_function(event):
    label = Label(main_window, text=1)
    grid[0][0].button.grid_remove()
    label.grid(row=0)

grid = create_grid(10, 10)













main_window.mainloop()
