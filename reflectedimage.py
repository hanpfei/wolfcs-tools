#!/usr/bin/python

'''
ZetCode PyCairo tutorial

This program creates an image reflection.

author: Jan Bodnar
website: zetcode.com
last edited: August 2012
'''

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import cairo
import sys


class Example(Gtk.Window):
    def __init__(self):
        super(Example, self).__init__()

        self.init_ui()
        self.load_image()
        self.init_vars()

    def init_ui(self):

        darea = Gtk.DrawingArea()
        darea.connect("draw", self.on_draw)
        self.add(darea)

        self.set_title("Reflection")
        self.resize(300, 350)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def load_image(self):

        try:
            self.s = cairo.ImageSurface.create_from_png("slanec.png")
        except Exception as e:
            print(e)
            sys.exit(1)

    def init_vars(self):

        self.imageWidth = self.s.get_width()
        self.imageHeight = self.s.get_height()
        self.gap = 40
        self.border = 20

    def on_draw(self, wid, cr):

        w, h = self.get_size()

        lg = cairo.LinearGradient(w / 2, 0, w / 2, h * 3)
        lg.add_color_stop_rgba(0, 0, 0, 0, 1)
        lg.add_color_stop_rgba(h, 0.2, 0.2, 0.2, 1)

        cr.set_source(lg)
        cr.paint()

        cr.set_source_surface(self.s, self.border, self.border)
        cr.paint()

        alpha = 0.7
        step = 1.0 / self.imageHeight

        cr.translate(0, 2 * self.imageHeight + self.gap)
        cr.scale(1, -1)

        i = 0

        while (i < self.imageHeight):
            cr.rectangle(self.border, self.imageHeight - i,
                         self.imageWidth, 1)

            i = i + 1

            cr.save()
            cr.clip()
            cr.set_source_surface(self.s, self.border,
                                  self.border)

            alpha = alpha - step

            cr.paint_with_alpha(alpha)
            cr.restore()


def main():
    app = Example()
    Gtk.main()


if __name__ == "__main__":
    main()