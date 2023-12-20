import tkinter

from .log import Log
from .vec2 import Vec2


class Window:
    
    def __init__(self, width, height, caption="lsys.py") -> None:
        self.width = width
        self.height = height
        self.caption = caption

        self._wnd = tkinter.Tk()
        self._wnd.minsize(width, height)
        self._wnd.maxsize(width, height)

        self._canvas = tkinter.Canvas(master=self._wnd, width=width, height=height, background="white")
        self._canvas.pack()


    def update(self) -> None:
        self._wnd.update()


    def mainloop(self):
        self._wnd.mainloop()

    
    def draw_point(self, pos: Vec2, radius, color) -> None:
        self._canvas.create_oval(int(pos.x - radius), int(-1 * (pos.y - radius)),
                                 int(pos.x + radius), int(-1 * (pos.y + radius)),
                                 fill=color, width=0)


    def draw_line(self, p1: Vec2, p2: Vec2, width, color) -> None:
        self._canvas.create_line(int(p1.x), int(-1 * p1.y), int(p2.x), int(-1 * p2.y), width=width, fill=color)


    def draw_polygon(self, points, color):
        self._canvas.create_polygon([(int(e.x), int(-1 * e.y)) for e in points], width=0, fill=color)

