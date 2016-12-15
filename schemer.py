#!/usr/bin/env python

import sys
import sdl2
import sdl2.ext
import json

GRID_WIDTH, GRID_HEIGHT = 21, 27
GRID = 30
PX_WIDTH, PX_HEIGHT = GRID_WIDTH*GRID, GRID_HEIGHT*GRID

def run():
    sdl2.ext.init()
    window = sdl2.ext.Window("Schemer", size=(PX_WIDTH, PX_HEIGHT))
    window.show()
    running = True
    schematic = {"lines": [], "toothed_edges": []}
    current_line = []
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            process_inputs(event, schematic, current_line)
        draw_frame(window, schematic, current_line)
        window.refresh()
    if len(sys.argv) > 1:
        save_schematic(sys.argv[1], schematic)
    else:
        save_schematic("schematic.json", schematic)
    return 0

def save_schematic(path, schematic):
    fout = open(path, "w")
    fout.write(json.dumps(schematic))
    fout.close()
    return

def process_inputs(event, schematic, current_line):
    if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
        x = int(event.button.x/float(GRID) + .5)
        y = int(event.button.y/float(GRID) + .5)
        if len(current_line) == 0:
            current_line.append([x, y])
        elif len(current_line) == 1:
            current_line.append([x, y])
            line = [current_line.pop(), current_line.pop()]
            if line in schematic["lines"]:
                schematic["lines"].pop(schematic["lines"].index(line))
            else:
                schematic["lines"].append(line)

def dot_product(v0, v1):
    products = [v0[i]*v1[i] for i in range(len(v0))]
    return sum(products)

def point_to_vector(image, pt, focal_length):
    mm_per_px = 3.39/image.h
    x = (pt[0] - image.w/2.0)*mm_per_px
    y = (pt[1] - image.h/2.0)*mm_per_px
    z = focal_length
    return [x, y, z]

def draw_frame(window, schematic, current_line):
    "Given the preloaded surface 'image', paint as background."
    ctx = sdl2.ext.Renderer(window)
    ctx.clear()
    render_grid(ctx)
    render_lines(ctx, schematic["lines"])
    ctx.present()
    return

def render_grid(ctx):
    color = sdl2.ext.Color(0, 127, 127)
    for i in range(0, GRID_HEIGHT):
        ctx.draw_line([0, i*GRID, PX_WIDTH, i*GRID], color)
    for i in range(0, GRID_WIDTH):
        ctx.draw_line([i*GRID, 0, i*GRID, PX_HEIGHT], color)

def render_lines(ctx, lines):
    color = sdl2.ext.Color(255, 255, 255)
    for line in lines:
        ctx.draw_line([line[0][0]*GRID, line[0][1]*GRID, line[1][0]*GRID, line[1][1]*GRID], color)

if __name__ == "__main__":
    sys.exit(run())
