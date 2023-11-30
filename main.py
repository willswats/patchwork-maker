from graphics import GraphWin, Point, Text, Line


def draw_patch(win, x, y, colour):
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
    win = GraphWin("Draw Patch", 300, 200)
    x = 20
    y = 20
    draw_patch(win, x, y, "red")
    win.getMouse()


draw_patchwork()
