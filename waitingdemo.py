#!/usr/bin/python

'''
ZetCode PyCairo tutorial

This program creates a 'waiting' effect.

author: Jan Bodnar
website: zetcode.com
last edited: August 2012
'''

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import cairo
import math


class cv(object):
    trs = (
        (0.0, 0.15, 0.30, 0.5, 0.65, 0.80, 0.9, 1.0),
        (1.0, 0.0, 0.15, 0.30, 0.5, 0.65, 0.8, 0.9),
        (0.9, 1.0, 0.0, 0.15, 0.3, 0.5, 0.65, 0.8),
        (0.8, 0.9, 1.0, 0.0, 0.15, 0.3, 0.5, 0.65),
        (0.65, 0.8, 0.9, 1.0, 0.0, 0.15, 0.3, 0.5),
        (0.5, 0.65, 0.8, 0.9, 1.0, 0.0, 0.15, 0.3),
        (0.3, 0.5, 0.65, 0.8, 0.9, 1.0, 0.0, 0.15),
        (0.15, 0.3, 0.5, 0.65, 0.8, 0.9, 1.0, 0.0,)
    )

    SPEED = 100
    CLIMIT = 1000
    NLINES = 8


class Example(Gtk.Window):
    def __init__(self):
        super(Example, self).__init__()

        self.init_ui()

    def init_ui(self):

        self.darea = Gtk.DrawingArea()
        self.darea.connect("draw", self.on_draw)
        self.add(self.darea)

        self.count = 0

        GLib.timeout_add(cv.SPEED, self.on_timer)

        self.set_title("Waiting")
        self.resize(250, 150)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def on_timer(self):

        self.count = self.count + 1

        if self.count >= cv.CLIMIT:
            self.count = 0

        self.darea.queue_draw()

        return True

    def on_draw(self, wid, cr):

        cr.set_line_width(3)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)

        w, h = self.get_size()

        cr.translate(w / 2, h / 2)

        for i in range(cv.NLINES):
            cr.set_source_rgba(0, 0, 0, cv.trs[self.count % 8][i])
            cr.move_to(0.0, -10.0)
            cr.line_to(0.0, -40.0)
            cr.rotate(math.pi / 4)
            cr.stroke()


def main():
    app = Example()
    Gtk.main()


if __name__ == "__main__":
    main()