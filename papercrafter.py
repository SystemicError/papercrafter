#!/usr/bin/env python

import cairo
import math
import json
import sys

PX_WIDTH, PX_HEIGHT = 2550, 3300

MM_WIDTH, MM_HEIGHT = 215.9, 279.4

GRID = 118


def load_schematic(path = "schematic.json"):
	fin = open(path)
	text = fin.read()
	fin.close()
	return json.loads(text)

def render_grid(cr):
    cr.set_source_rgb(0,1.0,1.0)
    for i in range(0, PX_HEIGHT, GRID):
        cr.move_to(0, i)
        cr.line_to(PX_WIDTH, i)
        cr.stroke()
    for i in range(0, PX_WIDTH, GRID):
        cr.move_to(i, 0)
        cr.line_to(i, PX_HEIGHT)
        cr.stroke()

def render_lines(cr, lines):
    cr.set_source_rgb(0, 0, 0)
    for line in lines:
        cr.move_to(line[0][0]*GRID, line[0][1]*GRID)
        cr.line_to(line[1][0]*GRID, line[1][1]*GRID)
        cr.stroke()

def render_edges(cr, edges):
    cr.set_source_rgb(.5, .5, .5)
    for edge in edges:
        cr.move_to(edges[0][0]*GRID, edges[0][1]*GRID)
        cr.line_to(edges[1][0]*GRID, edges[1][1]*GRID)
        cr.stroke()

def draw_schematic(cr, schematic):
    cr.set_source_rgb(1.0, 1.0, 1.0)
    cr.rectangle(0, 0, PX_WIDTH, PX_HEIGHT)
    cr.paint()
    render_grid(cr)
    render_lines(cr, schematic["lines"])
    render_edges(cr, schematic["toothed_edges"])
    return

#schematic = {"lines": [], "toothed_edges": []}
if len(sys.argv) > 1:
    schematic = load_schematic(sys.argv[1])
else:
    schematic = load_schematic()

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, PX_WIDTH, PX_HEIGHT)
cr = cairo.Context(surface)

draw_schematic(cr, schematic)

path = "schematic.png"
surface.write_to_png(path)
