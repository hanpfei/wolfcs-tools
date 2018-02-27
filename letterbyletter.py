#!/usr/bin/python

'''
ZetCode PyCairo tutorial

This program shows text letter by
letter.

author: Jan Bodnar
website: zetcode.com
last edited: August 2012
'''

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import cairo


class cv(object):
    SPEED = 800
    TEXT_SIZE = 35
    COUNT_MAX = 8


class Example(Gtk.Window):
    def __init__(self):
        super(Example, self).__init__()

        self.init_ui()
        self.init_vars()

    def init_ui(self):

        self.darea = Gtk.DrawingArea()
        self.darea.connect("draw", self.on_draw)
        self.add(self.darea)

        GLib.timeout_add(cv.SPEED, self.on_timer)

        self.set_title("Letter by letter")
        self.resize(350, 200)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def init_vars(self):

        self.timer = True
        self.count = 0
        self.text = ["Z", "e", "t", "C", "o", "d", "e"]

    def on_timer(self):

        if not self.timer: return False

        self.darea.queue_draw()
        return True

    def on_draw0(self, wid, cr):

        cr.select_font_face("Courier", cairo.FONT_SLANT_NORMAL,
                            cairo.FONT_WEIGHT_BOLD)

        cr.set_font_size(cv.TEXT_SIZE)

        dis = 0

        for i in range(self.count):
            (x, y, width, height, dx, dy) = cr.text_extents(self.text[i])

            dis += width + 2
            cr.move_to(dis + 30, 50)
            cr.show_text(self.text[i])

        self.count += 1

        if self.count == cv.COUNT_MAX:
            self.timer = False
            self.count = 0

    def on_draw(self, wid, cr):

        cr.select_font_face("Serif", cairo.FONT_SLANT_NORMAL,
                            cairo.FONT_WEIGHT_NORMAL)

        cr.set_font_size(13)

        glyphs = []
        index = 0

        for y in range(20):
            for x in range(35):
                glyphs.append((index, x * 15 + 20, y * 18 + 20))
                index += 1

        cr.show_glyphs(glyphs)


def main():
    app = Example()
    Gtk.main()


if __name__ == "__main__":
    main()