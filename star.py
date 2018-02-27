#!/usr/bin/python

'''
ZetCode PyCairo tutorial

This is a star example which
demonstrates scaling, translating and
rotating operations in PyCairo.

author: Jan Bodnar
website: zetcode.com
last edited: August 2012
'''

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import cairo


class cv(object):
    points = (
        (0, 85),
        (75, 75),
        (100, 10),
        (125, 75),
        (200, 85),
        (150, 125),
        (160, 190),
        (100, 150),
        (40, 190),
        (50, 125),
        (0, 85)
    )

    SPEED = 20
    TIMER_ID = 1


class Example(Gtk.Window):
    def __init__(self):
        super(Example, self).__init__()

        self.init_ui()
        self.init_vars()

    def init_ui(self):

        self.darea = Gtk.DrawingArea()
        self.darea.connect("draw", self.on_draw)
        self.add(self.darea)

        self.set_title("Star")
        self.resize(400, 300)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def init_vars(self):

        self.angle = 0
        self.scale = 1
        self.delta = 0.01

        GLib.timeout_add(cv.SPEED, self.on_timer)

    def on_timer(self):

        if self.scale < 0.01:
            self.delta = -self.delta

        elif self.scale > 0.99:
            self.delta = -self.delta

        self.scale += self.delta
        self.angle += 0.01

        self.darea.queue_draw()

        return True

    def on_draw0(self, wid, cr):

        w, h = self.get_size()

        cr.set_source_rgb(0, 0.44, 0.7)
        cr.set_line_width(1)

        cr.translate(w / 2, h / 2)
        cr.rotate(self.angle)
        cr.scale(self.scale, self.scale)

        for i in range(10):
            cr.line_to(cv.points[i][0], cv.points[i][1])

        cr.fill()

    def on_draw1(self, wid, cr):

        cr.set_source_rgb(0.1, 0.1, 0.1)

        cr.select_font_face("Purisa", cairo.FONT_SLANT_NORMAL,
                            cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(13)

        cr.move_to(20, 30)
        cr.show_text("Most relationships seem so transitory")
        cr.move_to(20, 60)
        cr.show_text("They're all good but not the permanent one")
        cr.move_to(20, 120)
        cr.show_text("Who doesn't long for someone to hold")
        cr.move_to(20, 150)
        cr.show_text("Who knows how to love without being told")
        cr.move_to(20, 180)
        cr.show_text("Somebody tell me why I'm on my own")
        cr.move_to(20, 210)
        cr.show_text("If there's a soulmate for everyone")

    def on_draw2(self, wid, cr):

        w, h = self.get_size()

        cr.select_font_face("Courier", cairo.FONT_SLANT_NORMAL,
                            cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(60)

        (x, y, width, height, dx, dy) = cr.text_extents("ZetCode")

        cr.move_to(w / 2 - width / 2, h / 2)
        cr.show_text("ZetCode")

    def on_draw3(self, wid, cr):

        cr.select_font_face("Serif", cairo.FONT_SLANT_NORMAL,
                            cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(50)

        cr.set_source_rgb(0, 0, 0)
        cr.move_to(40, 60)
        cr.show_text("ZetCode")

        cr.set_source_rgb(0.5, 0.5, 0.5)
        cr.move_to(43, 63)
        cr.show_text("ZetCode")

    def on_draw(self, wid, cr):

        cr.set_source_rgb(0.2, 0.2, 0.2)
        cr.paint()

        h = 90

        cr.select_font_face("Serif", cairo.FONT_SLANT_ITALIC,
                            cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(h)

        lg = cairo.LinearGradient(0, 15, 0, h * 0.8)
        lg.set_extend(cairo.EXTEND_REPEAT)
        lg.add_color_stop_rgb(0.0, 1, 0.6, 0)
        lg.add_color_stop_rgb(0.5, 1, 0.3, 0)

        cr.move_to(15, 80)
        cr.text_path("ZetCode")
        cr.set_source(lg)
        cr.fill()

def main():
    app = Example()
    Gtk.main()


if __name__ == "__main__":
    main()