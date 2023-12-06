from random import randint
from graphics import GraphWin, Point, Text, Line, Polygon, Rectangle


# draw_penultimate functions
def draw_triangle(win, colour, x, y, shape):
    offset_x = 10
    offset_y = 20
    polygon = Polygon(
        Point(x, y),
        Point(x - offset_x, y + offset_y),
        Point(x + offset_x, y + offset_y),
    )
    if shape == "half_left":
        polygon = Polygon(
            Point(x, y),
            Point(x - offset_x, y + offset_y),
            Point(x, y + offset_y),
        )
    elif shape == "half_right":
        polygon = Polygon(
            Point(x, y),
            Point(x, y + offset_y),
            Point(x + offset_x, y + offset_y),
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
    pen = {"x": x, "y": y, "colour": colour, "objects": []}

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
    final = {"x": x, "y": y, "colour": colour, "objects": []}

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
def draw_colour_block(win, x, y, colour, size):
    colour_block = {
        "x": x,
        "y": y,
        "colour": colour,
        "objects": [],
    }
    rectangle = Rectangle(
        Point(x, y),
        Point(x + size, y + size),
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
    size = 100

    for patchwork_object in patchwork_objects:
        patchwork_object_x_start = patchwork_object["x"]
        patchwork_object_x_end = patchwork_object["x"] + size
        patchwork_object_y_start = patchwork_object["y"]
        patchwork_object_y_end = patchwork_object["y"] + size

        if (
            point.getX() > patchwork_object_x_start
            and point.getX() < patchwork_object_x_end
            and point.getY() > patchwork_object_y_start
            and point.getY() < patchwork_object_y_end
        ):
            return patchwork_object


def draw_border(win, x, y):
    size = 100
    line_width = 5

    lines = []
    lineTopLeftToTopRight = Line(Point(x, y), Point(x + size, y))
    lines.append(lineTopLeftToTopRight)
    lineTopLeftToBottomLeft = Line(Point(x, y), Point(x, y + size))
    lines.append(lineTopLeftToBottomLeft)
    lineTopRightToBottomRight = Line(Point(x + size, y), Point(x + size, y + size))
    lines.append(lineTopRightToBottomRight)
    lineBottomLeftToBottomRight = Line(Point(x, y + size), Point(x + size, y + size))
    lines.append(lineBottomLeftToBottomRight)

    for line in lines:
        line.draw(win)
        line.setWidth(line_width)

    return lines


def draw_button(
    win,
    x,
    y,
    block_colour,
    block_size,
    text_colour,
    text_size,
    text_string,
):
    block = draw_colour_block(win, x, y, block_colour, block_size)
    text = draw_text_in_block(
        win, x, y, block_size, text_colour, text_string, text_size
    )

    block_object = block["objects"][0]
    button = {
        "x": block["x"],
        "y": block["y"],
        "colour": block_colour,
        "objects": [block_object, text],
    }

    return button


def draw_buttons(win, size):
    button_colour = "black"
    text_size = 6
    text_colour = "white"

    ok_button = draw_button(
        win, 0, 0, button_colour, size, text_colour, text_size, "OK"
    )
    close_button = draw_button(
        win,
        win.getWidth() - size,
        0,
        button_colour,
        size,
        text_colour,
        text_size,
        "CLOSE",
    )

    return [ok_button, close_button]


def undraw_buttons(buttons):
    for button_object in buttons[0]["objects"]:
        button_object.undraw()
    for button_object in buttons[1]["objects"]:
        button_object.undraw()


def undraw_borders(borders):
    for border in borders:
        for line in border:
            line.undraw()


def draw_border_selected(win, point, patchwork_objects, selected_objects, borders):
    patchwork_object = get_patchwork_object(point, patchwork_objects)
    if patchwork_object is not None:
        if patchwork_object in selected_objects:
            return
        selected_objects.append(patchwork_object)
        border = draw_border(win, patchwork_object["x"], patchwork_object["y"])
        borders.append(border)


def undraw_selected_objects(selected_objects):
    for selected_object in selected_objects:
        for obj in selected_object["objects"]:
            obj.undraw()


def draw_final_selected(win, selected_objects):
    finals = []
    undraw_selected_objects(selected_objects)
    for selected_object in selected_objects:
        final = draw_final(
            win,
            selected_object["x"],
            selected_object["y"],
            selected_object["colour"],
        )
        finals.append(final)
    return finals


def draw_pen_selected(win, selected_objects):
    pens = []
    undraw_selected_objects(selected_objects)
    for selected_object in selected_objects:
        pen = draw_penultimate(
            win,
            selected_object["x"],
            selected_object["y"],
            selected_object["colour"],
        )
        pens.append(pen)
    return pens


def draw_colour_block_selected(win, selected_objects):
    colour_blocks = []
    undraw_selected_objects(selected_objects)
    for selected_object in selected_objects:
        block = draw_colour_block(
            win,
            selected_object["x"],
            selected_object["y"],
            selected_object["colour"],
            100,
        )
        colour_blocks.append(block)
    return colour_blocks


def get_random_colour(colours):
    colours_max_index = len(colours) - 1
    colour = colours[randint(0, colours_max_index)]
    return colour


def draw_four_colour_block_random_selected(win, selected_objects, valid_colours):
    size = 50
    four_colour_blocks = []
    undraw_selected_objects(selected_objects)

    for selected_object in selected_objects:
        colours = []
        for _ in range(4):
            colours.append(get_random_colour(valid_colours))

        colour_block = {
            "x": selected_object["x"],
            "y": selected_object["y"],
            "colour": colours[0],
            "objects": [],
        }

        block_one = draw_colour_block(
            win,
            selected_object["x"],
            selected_object["y"],
            colours[0],
            size,
        )
        block_two = draw_colour_block(
            win,
            selected_object["x"] + size,
            selected_object["y"],
            colours[1],
            size,
        )
        block_three = draw_colour_block(
            win,
            selected_object["x"],
            selected_object["y"] + size,
            colours[2],
            size,
        )
        block_four = draw_colour_block(
            win,
            selected_object["x"] + size,
            selected_object["y"] + size,
            colours[3],
            size,
        )

        colour_block["objects"].append(block_one["objects"][0])
        colour_block["objects"].append(block_two["objects"][0])
        colour_block["objects"].append(block_three["objects"][0])
        colour_block["objects"].append(block_four["objects"][0])

        four_colour_blocks.append(colour_block)
    return four_colour_blocks


def colour_selected(key, selected_objects, valid_colours):
    for colour in valid_colours:
        first_letter_of_colour = colour[0]
        if key == first_letter_of_colour:
            for selected_object in selected_objects:
                for obj in selected_object["objects"]:
                    obj.setFill(colour)
                    obj.setOutline(colour)


def remove_identical_x_and_y_patchwork_from_list(patchwork, patchwork_list):
    new_list = []
    for patch_obj in patchwork_list:
        if patchwork["x"] == patch_obj["x"] and patchwork["y"] == patch_obj["y"]:
            pass
        else:
            new_list.append(patch_obj)
    return new_list


def update_patchwork_objects_and_selected_objects_lists(
    new_patchworks, patchwork_objects, selected_objects
):
    for new_patchwork in new_patchworks:
        patchwork_objects = remove_identical_x_and_y_patchwork_from_list(
            new_patchwork, patchwork_objects
        )
        patchwork_objects.append(new_patchwork)
        selected_objects = remove_identical_x_and_y_patchwork_from_list(
            new_patchwork, selected_objects
        )
        selected_objects.append(new_patchwork)
    return patchwork_objects, selected_objects


def challenge(win, patchwork_objects, valid_colours):
    selected_objects = []
    borders = []

    selection_mode = True
    edit_mode = False
    closed = False

    buttons_size = 30
    buttons = draw_buttons(win, buttons_size)

    while not closed:
        while selection_mode:
            undraw_buttons(buttons)
            buttons = draw_buttons(win, buttons_size)

            point = win.getMouse()

            if (
                point.getX() > buttons[0]["x"]
                and point.getX() <= buttons[0]["x"] + buttons_size
                and point.getY() > buttons[0]["y"]
                and point.getY() <= buttons[0]["y"] + buttons_size
            ):
                selection_mode = False
                edit_mode = True
                break

            if (
                point.getX() > buttons[1]["x"]
                and point.getX() <= buttons[1]["x"] + buttons_size
                and point.getY() > buttons[1]["y"]
                and point.getY() <= buttons[1]["y"] + buttons_size
            ):
                closed = True
                break

            draw_border_selected(
                win, point, patchwork_objects, selected_objects, borders
            )

        while edit_mode:
            undraw_buttons(buttons)
            key = win.getKey()

            if key == "s":
                edit_mode = False
                selection_mode = True
            elif key == "p":
                pens = draw_pen_selected(win, selected_objects)
                (
                    patchwork_objects,
                    selected_objects,
                ) = update_patchwork_objects_and_selected_objects_lists(
                    pens, patchwork_objects, selected_objects
                )
            elif key == "f":
                finals = draw_final_selected(win, selected_objects)
                (
                    patchwork_objects,
                    selected_objects,
                ) = update_patchwork_objects_and_selected_objects_lists(
                    finals, patchwork_objects, selected_objects
                )
            elif key == "q":
                colour_blocks = draw_colour_block_selected(win, selected_objects)
                (
                    patchwork_objects,
                    selected_objects,
                ) = update_patchwork_objects_and_selected_objects_lists(
                    colour_blocks, patchwork_objects, selected_objects
                )
            elif key == "x":
                four_colour_blocks = draw_four_colour_block_random_selected(
                    win, selected_objects, valid_colours
                )
                (
                    patchwork_objects,
                    selected_objects,
                ) = update_patchwork_objects_and_selected_objects_lists(
                    four_colour_blocks, patchwork_objects, selected_objects
                )
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
