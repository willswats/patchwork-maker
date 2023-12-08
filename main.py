from random import randint
from graphics import GraphWin, Point, Text, Line, Polygon, Rectangle


# draw_penultimate functions
def draw_triangle(win, x, y, colour, shape):
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


def draw_triangle_row(win, x, y, colour):
    triangles = []

    repetitions = 5
    x_addition = 20

    for _ in range(repetitions):
        triangle = draw_triangle(win, x, y, colour, "")
        triangles.append(triangle)
        x += x_addition

    return triangles


def draw_triangle_row_odd(win, x, y, colour):
    triangles = []

    start = 0
    end = 5
    repetitions = 6
    x_addition = 20

    x = x - 10
    for x_increment in range(repetitions):
        if x_increment == start:
            triangle = draw_triangle(win, x, y, colour, "half_right")
            triangles.append(triangle)
        elif x_increment == end:
            triangle = draw_triangle(win, x, y, colour, "half_left")
            triangles.append(triangle)
        else:
            triangle = draw_triangle(win, x, y, colour, "")
            triangles.append(triangle)
        x += x_addition

    return triangles


def draw_penultimate_patch(win, x, y, colour):
    patch = {"x": x, "y": y, "colour": colour, "objects": []}

    initial_x = x + 10
    repetitions = 5
    y_addition = 20

    x = initial_x
    for y_increment in range(repetitions):
        if y_increment % 2 == 0:
            triangles = draw_triangle_row(win, x, y, colour)
            for triangle in triangles:
                patch["objects"].append(triangle)
        else:
            triangles = draw_triangle_row_odd(win, x, y, colour)
            for triangle in triangles:
                patch["objects"].append(triangle)
        x = initial_x
        y += y_addition

    return patch


# draw_final functions
def draw_line_row(win, y, initial_x, colour):
    width = 100
    height = 20

    line_row = Line(Point(initial_x, y + height), Point(initial_x + width, y + height))
    line_row.setOutline(colour)
    line_row.draw(win)

    return line_row


def draw_line_column(win, x, initial_y, colour):
    width = 20
    height = 100

    line_column = Line(
        Point(x + width, initial_y), Point(x + width, initial_y + height)
    )
    line_column.setOutline(colour)
    line_column.draw(win)

    return line_column


def draw_text_in_block(win, x, y, block_size, colour, text_string, text_size):
    block_middle = block_size / 2

    text_point = Point(x + block_middle, y + block_middle)
    text = Text(text_point, text_string)
    text.setFill(colour)
    text.setSize(text_size)
    text.draw(win)

    return text


def draw_final_patch(win, x, y, colour):
    patch = {
        "x": x,
        "y": y,
        "colour": colour,
        "objects": [],
    }

    block_size = 20

    repetitions = 5

    initial_x = x
    initial_y = y

    text = "hi"
    text_size = 8

    for y_increment in range(repetitions):
        if y_increment < repetitions - 1:
            line_row = draw_line_row(win, y, initial_x, colour)
            patch["objects"].append(line_row)
        for x_increment in range(repetitions):
            text_in_block = draw_text_in_block(
                win, x, y, block_size, colour, text, text_size
            )
            patch["objects"].append(text_in_block)
            if x_increment < repetitions - 1:
                line_column = draw_line_column(win, x, initial_y, colour)
                patch["objects"].append(line_column)

            x += block_size
        x = initial_x
        y += block_size

    return patch


# draw_patchwork functions
def draw_colour_patch(win, x, y, colour, size):
    patch = {
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

    patch["objects"].append(rectangle)

    return patch


def choose_patch(
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
        patch = draw_penultimate_patch(win, x, y, colour)
        return patch
    elif x_increment <= final_x_index and y_increment >= final_y_index:
        patch = draw_final_patch(win, x, y, colour)
        return patch
    else:
        patch = draw_colour_patch(win, x, y, colour, colour_block_size)
        return patch


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

    patch_list = []

    x = 0
    y = 0
    initial_x = x
    for y_increment in range(size):
        for x_increment in range(size):
            if x_increment == colour_split:
                colour = colours[1]
                patch = choose_patch(
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
                patch_list.append(patch)
            elif y_increment > 0 and x_increment >= colour_split:
                colour = colours[2]
                patch = choose_patch(
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
                patch_list.append(patch)
            else:
                colour = colours[0]
                patch = choose_patch(
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
                patch_list.append(patch)
            x += 100
        colour_split -= 1
        x = initial_x
        y += 100

    challenge(win, patch_list, valid_colours)


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
def get_patchwork(point, patchworks):
    size = 100

    for patchwork in patchworks:
        patchwork_x_start = patchwork["x"]
        patchwork_x_end = patchwork["x"] + size
        patchwork_y_start = patchwork["y"]
        patchwork_y_end = patchwork["y"] + size

        if (
            point.getX() > patchwork_x_start
            and point.getX() < patchwork_x_end
            and point.getY() > patchwork_y_start
            and point.getY() < patchwork_y_end
        ):
            return patchwork


def draw_border(win, x, y):
    size = 100
    line_width = 5

    border = {
        "x": x,
        "y": y,
        "objects": [],
    }

    lineTopLeftToTopRight = Line(Point(x, y), Point(x + size, y))
    border["objects"].append(lineTopLeftToTopRight)
    lineTopLeftToBottomLeft = Line(Point(x, y), Point(x, y + size))
    border["objects"].append(lineTopLeftToBottomLeft)
    lineTopRightToBottomRight = Line(Point(x + size, y), Point(x + size, y + size))
    border["objects"].append(lineTopRightToBottomRight)
    lineBottomLeftToBottomRight = Line(Point(x, y + size), Point(x + size, y + size))
    border["objects"].append(lineBottomLeftToBottomRight)

    for line in border["objects"]:
        line.draw(win)
        line.setWidth(line_width)

    return border


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
    block = draw_colour_patch(win, x, y, block_colour, block_size)
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

    ok_button_x = 0
    ok_button_y = 0
    ok_button_text = "OK"

    close_button_x = win.getWidth() - size
    close_button_y = 0
    close_button_text = "CLOSE"

    ok_button = draw_button(
        win,
        ok_button_x,
        ok_button_y,
        button_colour,
        size,
        text_colour,
        text_size,
        ok_button_text,
    )
    close_button = draw_button(
        win,
        close_button_x,
        close_button_y,
        button_colour,
        size,
        text_colour,
        text_size,
        close_button_text,
    )

    return [ok_button, close_button]


def undraw_objects_in_list_of_dictionary(list_of_dictionary):
    for dictionary in list_of_dictionary:
        for obj in dictionary["objects"]:
            obj.undraw()


def undraw_border(x, y, borders):
    for border in borders:
        if x == border["x"] and y == border["y"]:
            borders = remove_identical_x_and_y_patch_from_list(border, borders)
            undraw_objects_in_list_of_dictionary([border])
    return borders


def draw_border_and_add_patch_to_selected(win, patch, selected_list, borders):
    if patch in selected_list:
        selected_list = remove_identical_x_and_y_patch_from_list(patch, selected_list)
        borders = undraw_border(patch["x"], patch["y"], borders)
        return selected_list, borders

    selected_list.append(patch)
    border = draw_border(win, patch["x"], patch["y"])
    borders.append(border)

    return selected_list, borders


def draw_final_patch_on_selected(win, selected_list):
    finals = []

    undraw_objects_in_list_of_dictionary(selected_list)

    for selected_dictionary in selected_list:
        final = draw_final_patch(
            win,
            selected_dictionary["x"],
            selected_dictionary["y"],
            selected_dictionary["colour"],
        )
        finals.append(final)

    return finals


def draw_pen_patch_on_selected(win, selected_list):
    pens = []

    undraw_objects_in_list_of_dictionary(selected_list)

    for selected_dictionary in selected_list:
        pen = draw_penultimate_patch(
            win,
            selected_dictionary["x"],
            selected_dictionary["y"],
            selected_dictionary["colour"],
        )
        pens.append(pen)

    return pens


def draw_colour_patch_on_selected(win, selected_list):
    colour_blocks = []
    size = 100

    undraw_objects_in_list_of_dictionary(selected_list)

    for selected_dictionary in selected_list:
        block = draw_colour_patch(
            win,
            selected_dictionary["x"],
            selected_dictionary["y"],
            selected_dictionary["colour"],
            size,
        )
        colour_blocks.append(block)

    return colour_blocks


def get_random_colour(colours):
    colours_max_index = len(colours) - 1
    colour = colours[randint(0, colours_max_index)]
    return colour


def draw_four_colour_patch(win, x, y, size, prev_colour, valid_colours):
    colours = []

    for _ in range(4):
        colours.append(get_random_colour(valid_colours))

    four_colour = {
        "x": x,
        "y": y,
        "colour": prev_colour,
        "objects": [],
    }

    block_one = draw_colour_patch(
        win,
        x,
        y,
        colours[0],
        size,
    )
    block_two = draw_colour_patch(
        win,
        x + size,
        y,
        colours[1],
        size,
    )
    block_three = draw_colour_patch(
        win,
        x,
        y + size,
        colours[2],
        size,
    )
    block_four = draw_colour_patch(
        win,
        x + size,
        y + size,
        colours[3],
        size,
    )

    four_colour["objects"].append(block_one["objects"][0])
    four_colour["objects"].append(block_two["objects"][0])
    four_colour["objects"].append(block_three["objects"][0])
    four_colour["objects"].append(block_four["objects"][0])

    return four_colour


def draw_four_colour_patch_on_selected(win, selected_list, valid_colours):
    four_colours = []
    size = 50

    undraw_objects_in_list_of_dictionary(selected_list)
    for selected_dictionary in selected_list:
        x = selected_dictionary["x"]
        y = selected_dictionary["y"]
        prev_colour = selected_dictionary["colour"]

        four_colour = draw_four_colour_patch(
            win, x, y, size, prev_colour, valid_colours
        )
        four_colours.append(four_colour)

    return four_colours


def colour_selected(key, selected_objects, valid_colours):
    for colour in valid_colours:
        first_letter_of_colour = colour[0]
        if key == first_letter_of_colour:
            for selected_object in selected_objects:
                for obj in selected_object["objects"]:
                    obj.setFill(colour)
                    obj.setOutline(colour)


def remove_identical_x_and_y_patch_from_list(patch, patch_list):
    new_patch_list = []

    for patch_in_list in patch_list:
        if patch["x"] == patch_in_list["x"] and patch["y"] == patch_in_list["y"]:
            pass
        else:
            new_patch_list.append(patch_in_list)

    return new_patch_list


def update_patch_list_and_selected_list(new_patch_list, patch_list, selected_list):
    for new_patch in new_patch_list:
        patch_list = remove_identical_x_and_y_patch_from_list(new_patch, patch_list)
        patch_list.append(new_patch)
        selected_list = remove_identical_x_and_y_patch_from_list(
            new_patch, selected_list
        )
        selected_list.append(new_patch)
    return patch_list, selected_list


def check_if_point_inside_button(point, button_x, button_y, button_size):
    inside = False
    if (
        point.getX() > button_x
        and point.getX() <= button_x + button_size
        and point.getY() > button_y
        and point.getY() <= button_y + button_size
    ):
        inside = True
    return inside


def challenge(win, patch_list, valid_colours):
    selected_list = []
    borders = []

    selection_mode = True
    edit_mode = False
    closed = False

    buttons_size = 30
    buttons = draw_buttons(win, buttons_size)
    ok_button = buttons[0]
    close_button = buttons[1]

    while not closed:
        while selection_mode:
            undraw_objects_in_list_of_dictionary(buttons)
            buttons = draw_buttons(win, buttons_size)

            point = win.getMouse()

            click_is_inside_ok_button = check_if_point_inside_button(
                point, ok_button["x"], ok_button["y"], buttons_size
            )
            if click_is_inside_ok_button:
                selection_mode = False
                edit_mode = True
                break

            click_is_inside_close_button = check_if_point_inside_button(
                point, close_button["x"], close_button["y"], buttons_size
            )
            if click_is_inside_close_button:
                closed = True
                break

            patch = get_patchwork(point, patch_list)
            selected_list, borders = draw_border_and_add_patch_to_selected(
                win, patch, selected_list, borders
            )

        while edit_mode:
            undraw_objects_in_list_of_dictionary(buttons)
            key = win.getKey()

            if key == "s":
                edit_mode = False
                selection_mode = True
            elif key == "p":
                pens = draw_pen_patch_on_selected(win, selected_list)
                patch_list, selected_list = update_patch_list_and_selected_list(
                    pens, patch_list, selected_list
                )
            elif key == "f":
                finals = draw_final_patch_on_selected(win, selected_list)
                patch_list, selected_list = update_patch_list_and_selected_list(
                    finals, patch_list, selected_list
                )
            elif key == "q":
                colours = draw_colour_patch_on_selected(win, selected_list)
                patch_list, selected_list = update_patch_list_and_selected_list(
                    colours, patch_list, selected_list
                )
            elif key == "x":
                four_colours = draw_four_colour_patch_on_selected(
                    win, selected_list, valid_colours
                )
                patch_list, selected_list = update_patch_list_and_selected_list(
                    four_colours, patch_list, selected_list
                )
            elif key == "d":
                undraw_objects_in_list_of_dictionary(borders)

                selected_list = []
                borders = []
            else:
                colour_selected(key, selected_list, valid_colours)


# main
def main():
    size, sizes, colours, valid_colours = get_inputs()
    draw_patchwork(size, sizes, colours, valid_colours)


main()
