from tkinter import *

main_window = Tk()


class MineButton(object):
    def __init__(self):
        self.button = Button(main_window, width=2, height=1)





def create_grid(width, height):
    grid_list = []
    for i in range(height):
        row_list = []
        for j in range(width):
            b = MineButton()
            row_list.append(b)
            row_list[j].button.grid(row=i, column=j)
        grid_list.append(row_list)
    return grid_list


create_grid(10, 10)












main_window.mainloop()
