#!/usr/bin/python

'''
ZetCode PyCairo tutorial

This code example draws a circle
using the PyCairo library.

Author: Jan Bodnar
Website: zetcode.com
Last edited: April 2018
'''

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import cairo
import math


class Example(Gtk.Window):
    def __init__(self):
        super(Example, self).__init__()

        self.init_ui()

    def init_ui(self):
        darea = Gtk.DrawingArea()
        darea.connect("draw", self.on_draw)
        self.add(darea)

        self.set_title("Spline")
        self.resize(230, 150)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def on_draw_lines(self, wid, cr):
        cr.set_line_width(9)
        cr.set_source_rgb(0.7, 0.2, 0.0)

        w, h = self.get_size()

        cr.translate(w / 2, h / 2)
        cr.arc(0, 0, 50, 0, 2 * math.pi)
        cr.stroke_preserve()

        cr.set_source_rgb(0.3, 0.4, 0.6)
        cr.fill()


    def on_draw_pen_dashes(self, wid, cr):

        cr.set_source_rgba(0, 0, 0, 1)
        cr.set_line_width(2)

        cr.set_dash([4.0, 21.0, 2.0])

        cr.move_to(40, 30)
        cr.line_to(250, 30)
        cr.stroke()

        cr.set_dash([14.0, 6.0])

        cr.move_to(40, 50)
        cr.line_to(250, 50)
        cr.stroke()

        cr.set_dash([1.0])

        cr.move_to(40, 70)
        cr.line_to(250, 70)
        cr.stroke()

    def on_draw_line_cap(self, wid, cr):

        cr.set_source_rgba(0, 0, 0, 1)
        cr.set_line_width(12)

        cr.set_line_cap(cairo.LINE_CAP_BUTT)
        cr.move_to(30, 50)
        cr.line_to(150, 50)
        cr.stroke()

        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(30, 90)
        cr.line_to(150, 90)
        cr.stroke()

        cr.set_line_cap(cairo.LINE_CAP_SQUARE)
        cr.move_to(30, 130)
        cr.line_to(150, 130)
        cr.stroke()

        cr.set_line_width(1.5)

        cr.move_to(30, 35)
        cr.line_to(30, 145)
        cr.stroke()

        cr.move_to(150, 35)
        cr.line_to(150, 145)
        cr.stroke()

        cr.move_to(155, 35)
        cr.line_to(155, 145)
        cr.stroke()


    def on_draw_line_joins(self, wid, cr):
        cr.set_line_width(14)

        cr.rectangle(30, 30, 100, 100)
        cr.set_line_join(cairo.LINE_JOIN_MITER)
        cr.stroke()

        cr.rectangle(160, 30, 100, 100)
        cr.set_line_join(cairo.LINE_JOIN_BEVEL)
        cr.stroke()

        cr.rectangle(100, 160, 100, 100)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.stroke()

    def on_draw_bezier_curve(self, wid, cr):

        cr.move_to(20, 40)
        cr.curve_to(320, 200, 330, 110, 450, 40)
        cr.stroke()


    def on_draw(self, wid, cr):
        cr.set_source_rgb(0.6, 0.6, 0.6)

        cr.rectangle(20, 20, 120, 80)
        cr.rectangle(180, 20, 80, 80)
        cr.fill()

        cr.arc(330, 60, 40, 0, 2 * math.pi)
        cr.fill()

        cr.arc(90, 160, 40, math.pi / 4, math.pi)
        cr.fill()

        cr.translate(220, 180)
        cr.scale(1, 0.7)
        cr.arc(0, 0, 50, 0, 2 * math.pi)
        cr.fill()

def main():
    app = Example()
    Gtk.main()


if __name__ == "__main__":
    main()