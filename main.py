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


def draw_triangle_row(win, colour, x, y):
    for _ in range(5):
        draw_triangle(win, colour, x, y, "")
        x += 20


def draw_triangle_row_odd(win, colour, x, y):
    start = 0
    end = 5

    x = x - 10
    for x_increment in range(6):
        if x_increment == start:
            draw_triangle(win, colour, x, y, "half_right")
        elif x_increment == end:
            draw_triangle(win, colour, x, y, "half_left")
        else:
            draw_triangle(win, colour, x, y, "")
        x += 20


def draw_penultimate(win, x, y, colour):
    initial_x = x + 10

    x = initial_x
    for y_increment in range(5):
        if y_increment % 2 == 0:
            draw_triangle_row(win, colour, x, y)
        else:
            draw_triangle_row_odd(win, colour, x, y)
        x = initial_x
        y += 20


def draw_final(win, x, y, colour):
    size = 20
    initial_x = x
    initial_y = y

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
        line_column = Line(Point(x + 20, y), Point(x + 20, y + 100))
        line_column.setOutline(colour)
        line_column.draw(win)
        x += size
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


def choose_draw(
    win,
    x,
    y,
    colour,
    x_increment,
    y_increment,
    final_x_index,
    final_y_index,
    pen_x_indexes,
    pen_y_indexes,
):
    pen_x_index_lower_bound = pen_x_indexes[0]
    pen_x_index_higher_bound = pen_x_indexes[1]
    pen_y_index_lower_bound = pen_y_indexes[0]
    pen_y_index_higher_bound = pen_y_indexes[1]

    if (
        x_increment >= pen_x_index_lower_bound
        and x_increment <= pen_x_index_higher_bound
        and y_increment >= pen_y_index_lower_bound
        and y_increment <= pen_y_index_higher_bound
    ):
        draw_penultimate(win, x, y, colour)
    elif x_increment <= final_x_index and y_increment >= final_y_index:
        draw_final(win, x, y, colour)
    else:
        draw_colour_block(win, x, y, colour)


def draw_patchwork(size, colours):
    win_width = 500
    win_height = 500

    x = 0
    y = 0
    initial_x = x

    final_x_index = 2
    final_y_index = 2

    pen_x_indexes = [1, 1]
    pen_y_indexes = [3, 3]

    colour_split = 4

    if size == 7:
        win_width = 700
        win_height = 700

        final_x_index = final_x_index + 1
        final_y_index = final_y_index + 1

        pen_x_indexes = [pen_x_indexes[0], pen_x_indexes[1] + 1]
        pen_y_indexes = [pen_y_indexes[0] + 1, pen_y_indexes[1] + 2]

        colour_split = colour_split + 2
    elif size == 9:
        win_width = 900
        win_height = 900

        final_x_index = final_x_index + 2
        final_y_index = final_y_index + 2

        pen_x_indexes = [pen_x_indexes[0], pen_x_indexes[1] + 2]
        pen_y_indexes = [pen_y_indexes[0] + 2, pen_y_indexes[1] + 4]

        colour_split = colour_split + 4

    win = GraphWin("Patchwork", win_width, win_height)
    win.setBackground("white")

    for y_increment in range(size):
        for x_increment in range(size):
            if x_increment == colour_split:
                colour = colours[1]
                choose_draw(
                    win,
                    x,
                    y,
                    colour,
                    x_increment,
                    y_increment,
                    final_x_index,
                    final_y_index,
                    pen_x_indexes,
                    pen_y_indexes,
                )
            elif y_increment > 0 and x_increment >= colour_split:
                colour = colours[2]
                choose_draw(
                    win,
                    x,
                    y,
                    colour,
                    x_increment,
                    y_increment,
                    final_x_index,
                    final_y_index,
                    pen_x_indexes,
                    pen_y_indexes,
                )
            else:
                colour = colours[0]
                choose_draw(
                    win,
                    x,
                    y,
                    colour,
                    x_increment,
                    y_increment,
                    final_x_index,
                    final_y_index,
                    pen_x_indexes,
                    pen_y_indexes,
                )
            x += 100
        colour_split -= 1
        x = initial_x
        y += 100
    win.getMouse()


def check_string_is_equal_to_item_in_list(string_check, list_check):
    valid = False
    for item in list_check:
        if string_check == item:
            valid = True

    return valid


def check_colour(prev_colours):
    valid_colours = ["red", "green", "blue", "magenta", "orange", "yellow", "cyan"]
    valid_colours_string = ", ".join(valid_colours)
    while True:
        colour = (
            input(f"Enter patchwork colour ({valid_colours_string}): ").lower().strip()
        )

        colour_valid = check_string_is_equal_to_item_in_list(colour, valid_colours)
        colour_exists = check_string_is_equal_to_item_in_list(colour, prev_colours)
        if not colour_valid:
            print(f"Invalid colour. Valid colours: {valid_colours_string}")
        elif colour_exists:
            print("The colour you entered has previously been entered.")
        else:
            return colour


def check_size():
    valid_sizes = ["5", "7", "9"]
    valid_sizes_string = ", ".join(valid_sizes)
    while True:
        size = (
            input(f"Enter the patchwork size ({valid_sizes_string}): ").lower().strip()
        )

        valid_size = check_string_is_equal_to_item_in_list(size, valid_sizes)
        if not valid_size:
            print(f"Invalid size. Valid sizes: {valid_sizes_string}")
        else:
            return size


def get_inputs():
    colours = []

    size = check_size()
    colourOne = check_colour(colours)
    colours.append(colourOne)
    colourTwo = check_colour(colours)
    colours.append(colourTwo)
    colourThree = check_colour(colours)
    colours.append(colourThree)

    return int(size), colours


def main():
    size, colours = get_inputs()
    draw_patchwork(size, colours)


main()
