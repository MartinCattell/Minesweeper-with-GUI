from tkinter import *

main_window = Tk()


class MineButton(object):
    def __init__(self):
        self.button = Button(main_window)


button_1 = MineButton()
button_1.button.grid(row=0)

button_2 = MineButton()
button_2.button.grid(row=0, column=1)

button_2 = MineButton()
button_2.button.grid(row=1)

button_2 = MineButton()
button_2.button.grid(row=1, column=1)















main_window.mainloop()
