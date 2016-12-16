#!/usr/bin/env python

import sys
import sdl2
import sdl2.ext
import json

GRID_WIDTH, GRID_HEIGHT = 42, 54
GRID = 15
PX_WIDTH, PX_HEIGHT = GRID_WIDTH*GRID, GRID_HEIGHT*GRID

def run():
    sdl2.ext.init()
    window = sdl2.ext.Window("Schemer", size=(PX_WIDTH, PX_HEIGHT))
    window.show()
    running = True
    if len(sys.argv) > 1:
        schematic = load_schematic(sys.argv[1])
    else:
        schematic = {"lines": [], "toothed_edges": []}
    current_line = []
    current_selection = []
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            process_inputs(event, schematic, current_line, current_selection)
        draw_frame(window, schematic, current_line, current_selection)
        window.refresh()
    if len(sys.argv) > 1:
        save_schematic(sys.argv[1], schematic)
    else:
        save_schematic("schematic.json", schematic)
    return 0

def load_schematic(path):
    try:
        fin = open(path, "r")
        schematic = json.loads(fin.read())
        fin.close()
        return schematic
    except IOError:
        return {"lines": [], "toothed_edges": []}


def save_schematic(path, schematic):
    fout = open(path, "w")
    fout.write(json.dumps(schematic))
    fout.close()
    return

def process_inputs(event, schematic, current_line, current_selection):
    if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
        x = int(event.button.x/float(GRID) + .5)
        y = int(event.button.y/float(GRID) + .5)
        if event.button.button == sdl2.SDL_BUTTON_LEFT and current_selection == []:
            if len(current_line) == 0:
                current_line.append([x, y])
            elif len(current_line) == 1:
                current_line.append([x, y])
                line = [current_line.pop(), current_line.pop()]
                if line in schematic["lines"]:
                    schematic["lines"].pop(schematic["lines"].index(line))
                else:
                    schematic["lines"].append(line)
        elif event.button.button == sdl2.SDL_BUTTON_RIGHT and current_line == []:
            if len(current_selection) == 0:
                current_selection.append([x, y])
            elif len(current_selection) == 1:
                current_selection.append([x, y])
                adjust_selection(current_selection)
            elif len(current_selection) == 2:
                current_selection.pop()
                current_selection.pop()
    elif event.type == sdl2.SDL_KEYDOWN:
        if len(current_selection) == 2:
            if event.key.keysym.sym == sdl2.SDLK_d:
                delete_selection(schematic, current_selection)

def line_is_selected(line, selection):
    "Returns true if either point of line is within selection."
    return point_is_selected(line[0], selection) or point_is_selected(line[1], selection)

def point_is_selected(point, selection):
    "Returns true point is within selection."
    if point[0] >= selection[0][0] and point[0] <= selection[1][0] and point[1] >= selection[0][1] and point[1] <= selection[1][1]:
        return True
    else:
        return False

def delete_selection(schematic, selection):
    schematic["lines"] = [x for x in schematic["lines"] if not line_is_selected(x, selection)]

def adjust_selection(selection):
    "Makes sure that the first point is the upper left, second is lower right."
    upper_left = [min([selection[0][0], selection[1][0]]), min([selection[0][1], selection[1][1]])]
    lower_right = [max([selection[0][0], selection[1][0]]), max([selection[0][1], selection[1][1]])]
    selection[0] = upper_left
    selection[1] = lower_right

def draw_frame(window, schematic, current_line, current_selection):
    "Given the preloaded surface 'image', paint as background."
    ctx = sdl2.ext.Renderer(window)
    ctx.clear()
    render_grid(ctx)
    render_lines(ctx, schematic["lines"])
    if len(current_selection) == 2:
        highlight_selection(ctx, current_selection)
    ctx.present()
    return

def render_grid(ctx):
    color = sdl2.ext.Color(0, 100, 100)
    for i in range(0, GRID_HEIGHT):
        ctx.draw_line([0, i*GRID, PX_WIDTH, i*GRID], color)
    for i in range(0, GRID_WIDTH):
        ctx.draw_line([i*GRID, 0, i*GRID, PX_HEIGHT], color)

def render_lines(ctx, lines):
    color = sdl2.ext.Color(255, 255, 255)
    for line in lines:
        ctx.draw_line([line[0][0]*GRID, line[0][1]*GRID, line[1][0]*GRID, line[1][1]*GRID], color)

def highlight_selection(ctx, current_selection):
    color = sdl2.ext.Color(255, 0, 0)
    upper_left = current_selection[0]
    lower_right = current_selection[1]
    min_x = int((upper_left[0] - .5)*GRID)
    min_y = int((upper_left[1] - .5)*GRID)
    max_x = int((lower_right[0] + .5)*GRID)
    max_y = int((lower_right[1] + .5)*GRID)
    ctx.draw_line([min_x, min_y, min_x, max_y, max_x, max_y, max_x, min_y, min_x, min_y], color)

if __name__ == "__main__":
    sys.exit(run())
