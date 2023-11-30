from graphics import GraphWin, Point, Text, Line, Polygon


def drawpatchwork():
    pass


def draw_penultimate(win, x, y, colour):
    pass


def draw_final(win, x, y, colour):
    size = 20
    initial_x = x

    line_row_y = y + 20
    for _ in range(4):
        line_row = Line(
            Point(initial_x, line_row_y), Point(initial_x + 100, line_row_y)
        )
        line_row.setOutline(colour)
        line_row.draw(win)
        line_row_y += 20

    line_column_x = x + 20
    for _ in range(4):
        line_column = Line(
            Point(line_column_x, initial_x), Point(line_column_x, initial_x + 100)
        )
        line_column.setOutline(colour)
        line_column.draw(win)
        line_column_x += 20

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


def draw_patchwork():
    win = GraphWin("Draw Patch", 500, 500)
    draw_final(win, 0, 0, "red")
    draw_penultimate(win, 100, 100, "red")
    win.getMouse()


draw_patchwork()
