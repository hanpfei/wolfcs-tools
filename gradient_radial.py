#!/usr/bin/python

'''
ZetCode PyCairo tutorial

This program works with radial
gradients in PyCairo.

author: Jan Bodnar
website: zetcode.com
last edited: August 2012
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

        self.set_title("Radial gradients")
        self.resize(300, 200)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def on_draw(self, wid, cr):
        self.draw_gradient1(cr)
        self.draw_gradient2(cr)

    def draw_gradient1(self, cr):
        cr.set_source_rgba(0, 0, 0, 1)
        cr.set_line_width(12)

        cr.translate(60, 60)

        r1 = cairo.RadialGradient(30, 30, 10, 30, 30, 90)
        r1.add_color_stop_rgba(0, 1, 1, 1, 1)
        r1.add_color_stop_rgba(1, 0.6, 0.6, 0.6, 1)
        cr.set_source(r1)
        cr.arc(0, 0, 40, 0, math.pi * 2)
        cr.fill()

        cr.translate(120, 0)

    def draw_gradient2(self, cr):
        r2 = cairo.RadialGradient(0, 0, 10, 0, 0, 40)
        r2.add_color_stop_rgb(0, 1, 1, 0)
        r2.add_color_stop_rgb(0.8, 0, 0, 0)
        cr.set_source(r2)
        cr.arc(0, 0, 40, 0, math.pi * 2)
        cr.fill()


def main():
    app = Example()
    Gtk.main()


if __name__ == "__main__":
    main()