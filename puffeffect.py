#!/usr/bin/python

'''
ZetCode PyCairo tutorial

This program creates a 'puff'
effect.

author: Jan Bodnar
website: zetcode.com
last edited: August 2012
'''

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import cairo


class cv(object):
    SPEED = 14
    TEXT_SIZE_MAX = 20
    ALPHA_DECREASE = 0.01
    SIZE_INCREASE = 0.8


class Example(Gtk.Window):
    def __init__(self):
        super(Example, self).__init__()

        self.init_ui()

    def init_ui(self):

        self.darea = Gtk.DrawingArea()
        self.darea.connect("draw", self.on_draw)
        self.add(self.darea)

        self.timer = True
        self.alpha = 1.0
        self.size = 1.0

        GLib.timeout_add(cv.SPEED, self.on_timer)

        self.set_title("Puff")
        self.resize(350, 200)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def on_timer(self):

        if not self.timer: return False

        self.darea.queue_draw()
        return True

    def on_draw0(self, wid, cr):

        w, h = self.get_size()

        cr.set_source_rgb(0.5, 0, 0)
        cr.paint()

        cr.select_font_face("Courier", cairo.FONT_SLANT_NORMAL,
                            cairo.FONT_WEIGHT_BOLD)

        self.size = self.size + cv.SIZE_INCREASE

        if self.size > cv.TEXT_SIZE_MAX:
            self.alpha = self.alpha - cv.ALPHA_DECREASE

        cr.set_font_size(self.size)
        cr.set_source_rgb(1, 1, 1)

        (x, y, width, height, dx, dy) = cr.text_extents("ZetCode")

        cr.move_to(w / 2 - width / 2, h / 2)
        cr.text_path("ZetCode")
        cr.clip()
        cr.paint_with_alpha(self.alpha)

        if self.alpha <= 0:
            self.timer = False

    def on_draw1(self, wid, cr):

        cr.set_source_rgb(0.2, 0.3, 0.8)
        cr.rectangle(10, 10, 30, 30)
        cr.fill()

        cr.translate(20, 20)
        cr.set_source_rgb(0.8, 0.3, 0.2)
        cr.rectangle(0, 0, 30, 30)
        cr.fill()

        cr.translate(30, 30)
        cr.set_source_rgb(0.8, 0.8, 0.2)
        cr.rectangle(0, 0, 30, 30)
        cr.fill()

        cr.translate(40, 40)
        cr.set_source_rgb(0.3, 0.8, 0.8)
        cr.rectangle(0, 0, 30, 30)
        cr.fill()

    def on_draw2(self, wid, cr):

        cr.set_source_rgb(0.6, 0.6, 0.6)
        cr.rectangle(20, 30, 80, 50)
        cr.fill()

        mtx = cairo.Matrix(1.0, 0.5,
                           0.0, 1.0,
                           0.0, 0.0)

        cr.transform(mtx)
        cr.rectangle(130, 30, 80, 50)
        cr.fill()

    def on_draw3(self, wid, cr):

        cr.set_source_rgb(0.2, 0.3, 0.8)
        cr.rectangle(10, 10, 90, 90)
        cr.fill()

        cr.scale(0.6, 0.6)
        cr.set_source_rgb(0.8, 0.3, 0.2)
        cr.rectangle(30, 30, 90, 90)
        cr.fill()

        cr.scale(0.8, 0.8)
        cr.set_source_rgb(0.8, 0.8, 0.2)
        cr.rectangle(50, 50, 90, 90)
        cr.fill()

    def on_draw(self, wid, cr):

        cr.set_source_rgb(0.2, 0.3, 0.8)
        cr.rectangle(10, 10, 90, 90)
        cr.fill()

        cr.save()
        cr.scale(0.6, 0.6)
        cr.set_source_rgb(0.8, 0.3, 0.2)
        cr.rectangle(30, 30, 90, 90)
        cr.fill()
        cr.restore()

        cr.save()
        cr.scale(0.8, 0.8)
        cr.set_source_rgb(0.8, 0.8, 0.2)
        cr.rectangle(50, 50, 90, 90)
        cr.fill()
        cr.restore()

def main():
    app = Example()
    Gtk.main()


if __name__ == "__main__":
    main()