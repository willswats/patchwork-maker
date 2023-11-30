from graphics import GraphWin, Point, Text, Line


def draw_patch(win, colour):
    size = 20
    initial_x = 0

    x = 0
    y = 0
    for _ in range(5):
        for _ in range(5):
            text_point = Point(x + (size / 2), y + (size / 2))
            text = Text(text_point, "hi!")
            text.setFill(colour)
            text.setSize(8)
            text.draw(win)

            x += size
        x = initial_x
        y += size

    y = 20
    for _ in range(4):
        line_row = Line(Point(0, y), Point(100, y))
        line_row.setOutline(colour)
        line_row.draw(win)
        y += 20

    x = 20
    for _ in range(4):
        line_row = Line(Point(x, 0), Point(x, 100))
        line_row.setOutline(colour)
        line_row.draw(win)
        x += 20


def draw_patchwork():
    win = GraphWin("Draw Patch", 300, 200)
    draw_patch(win, "red")
    win.getMouse()


draw_patchwork()
