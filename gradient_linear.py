#!/usr/bin/python

'''
ZetCode PyCairo tutorial

This program works with linear
gradients in PyCairo.

author: Jan Bodnar
website: zetcode.com
last edited: August 2012
'''

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import cairo


class Example(Gtk.Window):
    def __init__(self):
        super(Example, self).__init__()

        self.init_ui()

    def init_ui(self):

        darea = Gtk.DrawingArea()
        darea.connect("draw", self.on_draw)
        self.add(darea)

        self.set_title("Linear gradients")
        self.resize(340, 390)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def on_draw(self, wid, cr):

        self.draw_gradient1(cr)
        self.draw_gradient2(cr)
        self.draw_gradient3(cr)

    def draw_gradient1(self, cr):

        lg1 = cairo.LinearGradient(0.0, 0.0, 350.0, 350.0)

        count = 1

        i = 0.1
        while i < 1.0:
            if count % 2:
                lg1.add_color_stop_rgba(i, 0, 0, 0, 1)
            else:
                lg1.add_color_stop_rgba(i, 1, 0, 0, 1)
            i = i + 0.1
            count = count + 1

        cr.rectangle(20, 20, 300, 100)
        cr.set_source(lg1)
        cr.fill()

    def draw_gradient2(self, cr):

        lg2 = cairo.LinearGradient(0.0, 0.0, 350.0, 0)

        count = 1

        i = 0.05
        while i < 0.95:
            if count % 2:
                lg2.add_color_stop_rgba(i, 0, 0, 0, 1)
            else:
                lg2.add_color_stop_rgba(i, 0, 0, 1, 1)
            i = i + 0.025
            count = count + 1

        cr.rectangle(20, 140, 300, 100)
        cr.set_source(lg2)
        cr.fill()

    def draw_gradient3(self, cr):

        lg3 = cairo.LinearGradient(20.0, 260.0, 20.0, 360.0)
        lg3.add_color_stop_rgba(0.1, 0, 0, 0, 1)
        lg3.add_color_stop_rgba(0.5, 1, 1, 0, 1)
        lg3.add_color_stop_rgba(0.9, 0, 0, 0, 1)

        cr.rectangle(20, 260, 300, 100)
        cr.set_source(lg3)
        cr.fill()


def main():
    app = Example()
    Gtk.main()


if __name__ == "__main__":
    main()