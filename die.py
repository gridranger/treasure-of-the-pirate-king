from random import randrange
from time import sleep
from tkinter import Canvas, RIDGE


class Die(Canvas):
    def __init__(self, master, size, color, secondary_color, last_roll):
        Canvas.__init__(self, master=master, width=size, height=size, bd=1, relief=RIDGE)
        self._current_value = last_roll
        self._size = size
        self._color = color
        self._secondary_color = secondary_color
        self._dot_list = []
        self._dot_locations = [[(5, 5)],
                               [(2, 2), (8, 8)],
                               [(8, 2), (5, 5), (2, 8)],
                               [(2, 2), (2, 8), (8, 2), (8, 8)],
                               [(5, 5), (2, 2), (2, 8), (8, 2), (8, 8)],
                               [(2, 2), (2, 8), (8, 2), (8, 8), (2, 5), (8, 5)]]
        self.x = self.y = self.c = self._size / 2
        self._show()
        self._dot_radius = self._size / 10
        self._show_dots()

    def _show(self):
        self.create_rectangle(self.x - self.c + 2, self.y - self.c + 2, self.x + self.c + 2, self.y + self.c + 2,
                              fill=self._color, width=0)
    def _show_dots(self):
        for dot_x, dot_y in self._dot_locations[self._current_value - 1]:
            self._dot_list.append(
                self.create_oval((dot_x - 1) * self._dot_radius + 2, (dot_y - 1) * self._dot_radius + 2,
                                 (dot_x + 1) * self._dot_radius + 2, (dot_y + 1) * self._dot_radius + 2,
                                 fill=self._secondary_color))

    def torol(self):
        "törli a gombócokat"
        for gomboc in self._dot_list:
            self.delete(gomboc)


    def dob(self):
        "elvégzi a dobást"
        for i in range(6):
            self.torol()
            self._current_value = randrange(6) + 1
            self._show_dots()
            self.update_idletasks()
            sleep(0.075)
        return self._current_value

    def export_ertek(self):
        "Átadja a kocka értékét."
        return self._current_value
