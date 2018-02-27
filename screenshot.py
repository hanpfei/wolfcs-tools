#!/usr/bin/python

'''
ZetCode PyCairo tutorial

This code example takes a screenshot.

author: Jan Bodnar
website: zetcode.com
last edited: August 2012
'''

import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
import cairo


def main():
    root_win = Gdk.get_default_root_window()

    width = root_win.get_width()
    height = root_win.get_height()

    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    pb = Gdk.pixbuf_get_from_window(root_win, 0, 0, width, height)

    cr = cairo.Context(ims)
    Gdk.cairo_set_source_pixbuf(cr, pb, 0, 0)
    cr.paint()

    ims.write_to_png("screenshot.png")


if __name__ == "__main__":
    main()