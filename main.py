from random import randint
from graphics import GraphWin, Point, Text, Line, Polygon, Rectangle


# draw_penultimate functions
def draw_triangle(win, colour, top_left_x, top_left_y, shape):
    offset_x = 10
    offset_y = 20
    polygon = Polygon(
        Point(top_left_x, top_left_y),
        Point(top_left_x - offset_x, top_left_y + offset_y),
        Point(top_left_x + offset_x, top_left_y + offset_y),
    )
    if shape == "half_left":
        polygon = Polygon(
            Point(top_left_x, top_left_y),
            Point(top_left_x - offset_x, top_left_y + offset_y),
            Point(top_left_x, top_left_y + offset_y),
        )
    elif shape == "half_right":
        polygon = Polygon(
            Point(top_left_x, top_left_y),
            Point(top_left_x, top_left_y + offset_y),
            Point(top_left_x + offset_x, top_left_y + offset_y),
        )
    polygon.setFill(colour)
    polygon.setOutline(colour)
    polygon.draw(win)
    return polygon


def draw_triangle_row(win, colour, x, y):
    triangles = []
    for _ in range(5):
        triangle = draw_triangle(win, colour, x, y, "")
        triangles.append(triangle)
        x += 20
    return triangles


def draw_triangle_row_odd(win, colour, x, y):
    triangles = []
    start = 0
    end = 5

    x = x - 10
    for x_increment in range(6):
        if x_increment == start:
            triangle = draw_triangle(win, colour, x, y, "half_right")
            triangles.append(triangle)
        elif x_increment == end:
            triangle = draw_triangle(win, colour, x, y, "half_left")
            triangles.append(triangle)
        else:
            triangle = draw_triangle(win, colour, x, y, "")
            triangles.append(triangle)
        x += 20

    return triangles


def draw_penultimate(win, x, y, colour):
    pen = {"top_left_x": x, "top_left_y": y, "colour": colour, "objects": []}

    initial_x = x + 10

    x = initial_x
    for y_increment in range(5):
        if y_increment % 2 == 0:
            triangles = draw_triangle_row(win, colour, x, y)
            for triangle in triangles:
                pen["objects"].append(triangle)
        else:
            triangles = draw_triangle_row_odd(win, colour, x, y)
            for triangle in triangles:
                pen["objects"].append(triangle)
        x = initial_x
        y += 20

    return pen


# draw_final functions
def draw_line_row(win, y, initial_x, colour):
    line_row = Line(Point(initial_x, y + 20), Point(initial_x + 100, y + 20))
    line_row.setOutline(colour)
    line_row.draw(win)
    return line_row


def draw_line_column(win, x, initial_y, colour):
    line_column = Line(Point(x + 20, initial_y), Point(x + 20, initial_y + 100))
    line_column.setOutline(colour)
    line_column.draw(win)
    return line_column


def draw_text_in_block(win, x, y, block_size, colour, text_string, text_size):
    text_point = Point(x + (block_size / 2), y + (block_size / 2))
    text = Text(text_point, text_string)
    text.setFill(colour)
    text.setSize(text_size)
    text.draw(win)
    return text


def draw_final(win, x, y, colour):
    final = {"top_left_x": x, "top_left_y": y, "colour": colour, "objects": []}

    block_size = 20

    repetitions = 5

    initial_x = x
    initial_y = y

    text = "hi"
    text_size = 8

    for y_increment in range(repetitions):
        if y_increment < repetitions - 1:
            line_row = draw_line_row(win, y, initial_x, colour)
            final["objects"].append(line_row)
        for x_increment in range(repetitions):
            text_in_block = draw_text_in_block(
                win, x, y, block_size, colour, text, text_size
            )
            final["objects"].append(text_in_block)
            if x_increment < repetitions - 1:
                line_column = draw_line_column(win, x, initial_y, colour)
                final["objects"].append(line_column)

            x += block_size
        x = initial_x
        y += block_size

    return final


# draw_patchwork functions
def draw_colour_block(win, top_left_x, top_left_y, colour, size):
    colour_block = {
        "top_left_x": top_left_x,
        "top_left_y": top_left_y,
        "colour": colour,
        "objects": [],
    }
    rectangle = Rectangle(
        Point(top_left_x, top_left_y),
        Point(top_left_x + size, top_left_y + size),
    )
    rectangle.setFill(colour)
    rectangle.setOutline(colour)
    rectangle.draw(win)
    colour_block["objects"].append(rectangle)
    return colour_block


def choose_draw(
    win,
    x,
    y,
    colour,
    x_increment,
    y_increment,
    final_x_index,
    final_y_index,
    pen_x_index_lower_bound,
    pen_x_index_higher_bound,
    pen_y_index_lower_bound,
    pen_y_index_higher_bound,
):
    colour_block_size = 100

    if (
        x_increment >= pen_x_index_lower_bound
        and x_increment <= pen_x_index_higher_bound
        and y_increment >= pen_y_index_lower_bound
        and y_increment <= pen_y_index_higher_bound
    ):
        pen_objects = draw_penultimate(win, x, y, colour)
        return pen_objects
    elif x_increment <= final_x_index and y_increment >= final_y_index:
        final_objects = draw_final(win, x, y, colour)
        return final_objects
    else:
        colour_block_objects = draw_colour_block(win, x, y, colour, colour_block_size)
        return colour_block_objects


def draw_patchwork(size, sizes, colours, valid_colours):
    size_index = sizes.index(size)

    size_decrement = size_index + 3
    final_x_index = size - size_decrement
    final_y_index = size - size_decrement

    pen_x_index_lower_bound = 1
    pen_x_index_higher_bound = 1 + size_index
    pen_y_index_lower_bound = 3 + size_index
    pen_y_index_higher_bound = 3 + (size_index * 2)

    colour_split = size - 1

    win_width = int(f"{size}00")
    win_height = int(f"{size}00")
    win = GraphWin("Patchwork", win_width, win_height)
    win.setBackground("white")

    patchwork_objects = []

    x = 0
    y = 0
    initial_x = x
    for y_increment in range(size):
        for x_increment in range(size):
            if x_increment == colour_split:
                colour = colours[1]
                objects = choose_draw(
                    win,
                    x,
                    y,
                    colour,
                    x_increment,
                    y_increment,
                    final_x_index,
                    final_y_index,
                    pen_x_index_lower_bound,
                    pen_x_index_higher_bound,
                    pen_y_index_lower_bound,
                    pen_y_index_higher_bound,
                )
                patchwork_objects.append(objects)
            elif y_increment > 0 and x_increment >= colour_split:
                colour = colours[2]
                objects = choose_draw(
                    win,
                    x,
                    y,
                    colour,
                    x_increment,
                    y_increment,
                    final_x_index,
                    final_y_index,
                    pen_x_index_lower_bound,
                    pen_x_index_higher_bound,
                    pen_y_index_lower_bound,
                    pen_y_index_higher_bound,
                )
                patchwork_objects.append(objects)
            else:
                colour = colours[0]
                objects = choose_draw(
                    win,
                    x,
                    y,
                    colour,
                    x_increment,
                    y_increment,
                    final_x_index,
                    final_y_index,
                    pen_x_index_lower_bound,
                    pen_x_index_higher_bound,
                    pen_y_index_lower_bound,
                    pen_y_index_higher_bound,
                )
                patchwork_objects.append(objects)
            x += 100
        colour_split -= 1
        x = initial_x
        y += 100

    challenge(win, patchwork_objects, valid_colours)


# get_inputs functions
def check_string_is_equal_to_item_in_list(string_check, list_check):
    valid = False
    for item in list_check:
        if string_check == item:
            valid = True

    return valid


def check_colour(valid_colours, prev_colours):
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


def check_size(valid_sizes):
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
    valid_sizes = ["5", "7", "9"]
    valid_colours = ["red", "green", "blue", "magenta", "orange", "yellow", "cyan"]
    colours = []

    size = check_size(valid_sizes)
    colourOne = check_colour(valid_colours, colours)
    colours.append(colourOne)
    colourTwo = check_colour(valid_colours, colours)
    colours.append(colourTwo)
    colourThree = check_colour(valid_colours, colours)
    colours.append(colourThree)

    sizes = [int(size) for size in valid_sizes]

    return int(size), sizes, colours, valid_colours


# challenge functions
def get_patchwork_object(point, patchwork_objects):
    for patchwork_object in patchwork_objects:
        patchwork_object_x_start = patchwork_object["top_left_x"]
        patchwork_object_x_end = patchwork_object["top_left_x"] + 100
        patchwork_object_y_start = patchwork_object["top_left_y"]
        patchwork_object_y_end = patchwork_object["top_left_y"] + 100

        if (
            point.getX() > patchwork_object_x_start
            and point.getX() < patchwork_object_x_end
            and point.getY() > patchwork_object_y_start
            and point.getY() < patchwork_object_y_end
        ):
            return patchwork_object


def draw_border(win, top_left_x, top_left_y):
    lines = []

    lineTopLeftToTopRight = Line(
        Point(top_left_x, top_left_y), Point(top_left_x + 100, top_left_y)
    )
    lines.append(lineTopLeftToTopRight)
    lineTopLeftToBottomLeft = Line(
        Point(top_left_x, top_left_y), Point(top_left_x, top_left_y + 100)
    )
    lines.append(lineTopLeftToBottomLeft)
    lineTopRightToBottomRight = Line(
        Point(top_left_x + 100, top_left_y), Point(top_left_x + 100, top_left_y + 100)
    )
    lines.append(lineTopRightToBottomRight)
    lineBottomLeftToBottomRight = Line(
        Point(top_left_x, top_left_y + 100), Point(top_left_x + 100, top_left_y + 100)
    )
    lines.append(lineBottomLeftToBottomRight)

    for line in lines:
        line.draw(win)
        line.setWidth(5)

    return lines


def draw_button(
    win,
    top_left_x,
    top_left_y,
    block_colour,
    block_size,
    text_colour,
    text_size,
    text_string,
):
    block = draw_colour_block(win, top_left_x, top_left_y, block_colour, block_size)
    text = draw_text_in_block(
        win, top_left_x, top_left_y, block_size, text_colour, text_string, text_size
    )
    block_object = block["objects"][0]

    return [block_object, text]


def draw_buttons(win):
    button_size = 30
    button_colour = "black"

    text_size = 6
    text_colour = "white"

    ok_button_objects = draw_button(
        win, 0, 0, button_colour, button_size, text_colour, text_size, "OK"
    )
    close_button_objects = draw_button(
        win,
        win.getWidth() - button_size,
        0,
        button_colour,
        button_size,
        text_colour,
        text_size,
        "CLOSE",
    )

    return [ok_button_objects, close_button_objects]


def undraw_buttons(buttons_objects):
    for button_object in buttons_objects[0]:
        button_object.undraw()
    for button_object in buttons_objects[1]:
        button_object.undraw()


def undraw_borders(borders):
    for border in borders:
        for line in border:
            line.undraw()


def draw_border_selected(win, point, patchwork_objects, selected_objects, borders):
    patchwork_object = get_patchwork_object(point, patchwork_objects)
    if patchwork_object is not None:
        selected_objects.append(patchwork_object)
        border = draw_border(
            win, patchwork_object["top_left_x"], patchwork_object["top_left_y"]
        )
        borders.append(border)


def draw_final_selected(win, selected_objects):
    finals = []
    for selected_object in selected_objects:
        for obj in selected_object["objects"]:
            obj.undraw()
        final = draw_final(
            win,
            selected_object["top_left_x"],
            selected_object["top_left_y"],
            selected_object["colour"],
        )
        finals.append(final)
    return finals


def draw_pen_selected(win, selected_objects):
    pens = []
    for selected_object in selected_objects:
        for obj in selected_object["objects"]:
            obj.undraw()
        pen = draw_penultimate(
            win,
            selected_object["top_left_x"],
            selected_object["top_left_y"],
            selected_object["colour"],
        )
        pens.append(pen)
    return pens


def draw_colour_block_selected(win, selected_objects):
    colour_blocks = []
    for selected_object in selected_objects:
        for obj in selected_object["objects"]:
            obj.undraw()
        block = draw_colour_block(
            win,
            selected_object["top_left_x"],
            selected_object["top_left_y"],
            selected_object["colour"],
            100,
        )
        colour_blocks.append(block)
    return colour_blocks


def draw_four_colour_block_random_selected(win, selected_objects, valid_colours):
    four_colour_blocks = []
    for selected_object in selected_objects:
        for obj in selected_object["objects"]:
            obj.undraw()
        valid_colours_len = len(valid_colours) - 1
        colour_block = {
            "top_left_x": selected_object["top_left_x"],
            "top_left_y": selected_object["top_left_y"],
            "colour": valid_colours[randint(0, valid_colours_len)],
            "objects": [],
        }

        block_one = draw_colour_block(
            win,
            selected_object["top_left_x"],
            selected_object["top_left_y"],
            valid_colours[randint(0, valid_colours_len)],
            50,
        )
        block_two = draw_colour_block(
            win,
            selected_object["top_left_x"] + 50,
            selected_object["top_left_y"],
            valid_colours[randint(0, valid_colours_len)],
            50,
        )
        block_three = draw_colour_block(
            win,
            selected_object["top_left_x"],
            selected_object["top_left_y"] + 50,
            valid_colours[randint(0, valid_colours_len)],
            50,
        )
        block_four = draw_colour_block(
            win,
            selected_object["top_left_x"] + 50,
            selected_object["top_left_y"] + 50,
            valid_colours[randint(0, valid_colours_len)],
            50,
        )

        colour_block["objects"].append(block_one["objects"][0])
        colour_block["objects"].append(block_two["objects"][0])
        colour_block["objects"].append(block_three["objects"][0])
        colour_block["objects"].append(block_four["objects"][0])

        four_colour_blocks.append(colour_block)
    return four_colour_blocks


def colour_selected(key, selected_objects, valid_colours):
    for colour in valid_colours:
        if key == colour[0]:
            for selected_object in selected_objects:
                for obj in selected_object["objects"]:
                    obj.setFill(colour)
                    obj.setOutline(colour)


def remove_patchwork_from_list(patchwork, patchwork_list):
    new_list = []
    for patch_dict in patchwork_list:
        if (
            patchwork["top_left_x"] == patch_dict["top_left_x"]
            and patchwork["top_left_y"] == patch_dict["top_left_y"]
        ):
            pass
        else:
            new_list.append(patch_dict)
    return new_list


def challenge(win, patchwork_objects, valid_colours):
    selected_objects = []
    borders = []

    selection_mode = True
    edit_mode = False
    closed = False

    buttons_objects = draw_buttons(win)

    while not closed:
        while selection_mode:
            undraw_buttons(buttons_objects)
            buttons_objects = draw_buttons(win)

            point = win.getMouse()

            if (
                point.getX() > 0
                and point.getX() <= 30
                and point.getY() > 0
                and point.getY() <= 30
            ):
                selection_mode = False
                edit_mode = True
                break

            if (
                point.getX() > win.getWidth() - 30
                and point.getX() <= win.getWidth()
                and point.getY() > 0
                and point.getY() <= 30
            ):
                closed = True
                break

            draw_border_selected(
                win, point, patchwork_objects, selected_objects, borders
            )

        while edit_mode:
            undraw_buttons(buttons_objects)
            key = win.getKey()

            if key == "s":
                edit_mode = False
                selection_mode = True
            elif key == "p":
                pens = draw_pen_selected(win, selected_objects)
                for pen in pens:
                    patchwork_objects = remove_patchwork_from_list(
                        pen, patchwork_objects
                    )
                    patchwork_objects.append(pen)
                    selected_objects = remove_patchwork_from_list(pen, selected_objects)
                    selected_objects.append(pen)
            elif key == "f":
                finals = draw_final_selected(win, selected_objects)
                for final in finals:
                    patchwork_objects = remove_patchwork_from_list(
                        final, patchwork_objects
                    )
                    patchwork_objects.append(final)
                    selected_objects = remove_patchwork_from_list(
                        final, selected_objects
                    )
                    selected_objects.append(final)
            elif key == "q":
                colour_blocks = draw_colour_block_selected(win, selected_objects)
                for colour_block in colour_blocks:
                    patchwork_objects = remove_patchwork_from_list(
                        colour_block, patchwork_objects
                    )
                    patchwork_objects.append(colour_block)
                    selected_objects = remove_patchwork_from_list(
                        colour_block, selected_objects
                    )
                    selected_objects.append(colour_block)
            elif key == "x":
                four_colour_blocks = draw_four_colour_block_random_selected(
                    win, selected_objects, valid_colours
                )
                for four_colour_block in four_colour_blocks:
                    patchwork_objects = remove_patchwork_from_list(
                        four_colour_block, patchwork_objects
                    )
                    patchwork_objects.append(four_colour_block)
                    selected_objects = remove_patchwork_from_list(
                        four_colour_block, selected_objects
                    )
                    selected_objects.append(four_colour_block)
                selected_objects = []
            elif key == "d":
                selected_objects = []
                undraw_borders(borders)
            else:
                colour_selected(key, selected_objects, valid_colours)


# main
def main():
    size, sizes, colours, valid_colours = get_inputs()
    draw_patchwork(size, sizes, colours, valid_colours)


main()
