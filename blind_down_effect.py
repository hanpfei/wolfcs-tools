#!/usr/bin/python

'''
ZetCode PyCairo tutorial

This program creates a blind down
effect using masking operation.

author: Jan Bodnar
website: zetcode.com
last edited: August 2012
'''

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import cairo
import math


class Example(Gtk.Window):
    def __init__(self):
        super(Example, self).__init__()

        self.init_ui()
        self.load_image()
        self.init_vars()

    def init_ui(self):

        self.darea = Gtk.DrawingArea()
        self.darea.connect("draw", self.on_draw)
        self.add(self.darea)

        GLib.timeout_add(35, self.on_timer)

        self.set_title("Blind down")
        self.resize(325, 250)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def load_image(self):

        self.image = cairo.ImageSurface.create_from_png("beckov.png")

    def init_vars(self):

        self.timer = True
        self.h = 0
        self.iw = self.image.get_width()
        self.ih = self.image.get_height()

        self.ims = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                      self.iw, self.ih)

    def on_timer(self):

        if (not self.timer):
            return False

        self.darea.queue_draw()
        return True

    def on_draw_01(self, wid, cr):

        ic = cairo.Context(self.ims)

        ic.rectangle(0, 0, self.iw, self.h)
        ic.fill()

        self.h += 1

        if (self.h == self.ih):
            self.timer = False

        cr.set_source_surface(self.image, 10, 10)
        cr.mask_surface(self.ims, 10, 10)

    def on_draw(self, wid, cr):
        for i in range(1, 11):
            cr.set_source_rgba(0, 0, 1, i * 0.1)
            cr.rectangle(50 * i, 20, 40, 40)
            cr.fill()

def main():
    app = Example()
    Gtk.main()


if __name__ == "__main__":
    main()