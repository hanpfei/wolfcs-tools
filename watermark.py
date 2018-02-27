#!/usr/bin/python

'''
ZetCode PyCairo tutorial

This program draws a watermark
on an image.

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
        self.load_image()
        self.draw_mark()

    def init_ui(self):
        darea = Gtk.DrawingArea()
        darea.connect("draw", self.on_draw)
        self.add(darea)

        self.set_title("Watermark")
        self.resize(350, 250)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def load_image(self):
        self.ims = cairo.ImageSurface.create_from_png("beckov.png")

    def draw_mark(self):
        cr = cairo.Context(self.ims)
        cr.set_font_size(11)
        cr.set_source_rgb(0.9, 0.9, 0.9)
        cr.move_to(20, 30)
        cr.show_text(" Beckov 2012 , (c) Jan Bodnar ")
        cr.stroke()

    def on_draw(self, wid, cr):
        cr.set_source_surface(self.ims, 10, 10)
        cr.paint()


def main():
    app = Example()
    Gtk.main()


if __name__ == "__main__":
    main()