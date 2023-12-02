from graphics import GraphWin, Point, Text, Line, Polygon, Rectangle


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
    initial_y = y

    for _ in range(4):
        line_column = Line(Point(x + 20, y), Point(x + 20, y + 100))
        line_column.setOutline(colour)
        line_column.draw(win)
        x += size
    x = initial_x

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
    y = initial_y
    x = initial_x

    for _ in range(4):
        line_row = Line(Point(initial_x, y + 20), Point(initial_x + 100, y + 20))
        line_row.setOutline(colour)
        line_row.draw(win)
        y += size
    x = initial_x


def draw_colour_block(win, top_left_x, top_left_y, colour):
    rectangle = Rectangle(
        Point(top_left_x, top_left_y), Point(top_left_x + 100, top_left_y + 100)
    )
    rectangle.setFill(colour)
    rectangle.setOutline(colour)
    rectangle.draw(win)


def draw_patchwork():
    win = GraphWin("Draw Patch", 500, 500)

    x = 0
    y = 0
    initial_x = x
    final_y = 2
    final_x = 2
    pen_x = 1
    pen_y = 3
    yellow = 4
    red = 4
    colour = "blue"
    for y_increment in range(5):
        for x_increment in range(5):
            if x_increment == yellow:
                colour = "yellow"
                if y_increment == pen_y and x_increment == pen_x:
                    draw_penultimate(win, x, y, colour)
                elif y_increment >= final_y and x_increment <= final_x:
                    draw_final(win, x, y, colour)
                else:
                    draw_colour_block(win, x, y, colour)
            elif y_increment > 0 and x_increment >= red:
                colour = "red"
                if y_increment == pen_y and x_increment == pen_x:
                    draw_penultimate(win, x, y, colour)
                elif y_increment >= final_y and x_increment <= final_x:
                    draw_final(win, x, y, colour)
                else:
                    draw_colour_block(win, x, y, colour)
            else:
                colour = "blue"
                if y_increment == pen_y and x_increment == pen_x:
                    draw_penultimate(win, x, y, colour)
                elif y_increment >= final_y and x_increment <= final_x:
                    draw_final(win, x, y, colour)
                else:
                    draw_colour_block(win, x, y, colour)
            x += 100
        yellow -= 1
        red -= 1
        x = initial_x
        y += 100
    draw_penultimate(win, 100, 0, "red")
    win.getMouse()


def main():
    draw_patchwork()


main()
