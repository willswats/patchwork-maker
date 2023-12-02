from graphics import GraphWin, Point, Text, Line, Polygon


def draw_triangle(win, colour, top_x, top_y, shape):
    offset_x = 10
    offset_y = 20
    polygon = Polygon(
        Point(top_x, top_y),
        Point(top_x - offset_x, top_y + offset_y),
        Point(top_x + offset_x, top_y + offset_y),
    )
    if shape == "half_left":
        polygon = Polygon(
            Point(top_x, top_y),
            Point(top_x - offset_x, top_y + offset_y),
            Point(top_x, top_y + offset_y),
        )
    elif shape == "half_right":
        polygon = Polygon(
            Point(top_x, top_y),
            Point(top_x, top_y + offset_y),
            Point(top_x + offset_x, top_y + offset_y),
        )
    polygon.setFill(colour)
    polygon.setOutline(colour)
    polygon.draw(win)


def draw_triangle_row_odd(win, colour, x, y):
    start = 0
    end = 5

    line_row_x = x - 10
    for x_increment in range(6):
        if x_increment == start:
            draw_triangle(win, colour, line_row_x, y, "half_right")
        elif x_increment == end:
            draw_triangle(win, colour, line_row_x, y, "half_left")
        else:
            draw_triangle(win, colour, line_row_x, y, "")
        line_row_x += 20


def draw_triangle_row(win, colour, x, y):
    line_row_x = x
    for _ in range(5):
        draw_triangle(win, colour, line_row_x, y, "")
        line_row_x += 20


def drawpatchwork():
    pass


def draw_penultimate(win, x, y, colour):
    initial_x = x + 10

    line_row_x = initial_x
    line_row_y = y
    for y_increment in range(5):
        if y_increment % 2 == 0:
            draw_triangle_row(win, colour, line_row_x, line_row_y)
        else:
            draw_triangle_row_odd(win, colour, line_row_x, line_row_y)
        line_row_x = initial_x
        line_row_y += 20


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
    draw_penultimate(win, 100, 0, "red")
    win.getMouse()


draw_patchwork()
