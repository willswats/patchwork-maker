from graphics import GraphWin, Point, Text, Rectangle


def draw_patch(win, x, y, colour):
    size = 20
    initial_x = x

    for _ in range(5):
        for _ in range(5):
            top_left = Point(x, y)
            bottom_right = Point(x + size, y + size)

            rectangle = Rectangle(top_left, bottom_right)
            rectangle.setOutline(colour)
            rectangle.draw(win)

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
    draw_patch(win, 0, 0, "blue")
    draw_patch(win, 100, 0, "blue")
    draw_patch(win, 200, 0, "blue")
    draw_patch(win, 0, 100, "blue")
    draw_patch(win, 100, 100, "blue")
    draw_patch(win, 200, 100, "blue")
    win.getMouse()


draw_patchwork()
