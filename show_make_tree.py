#!/usr/bin/python3

import sys
import os
from os.path import exists

__FILE    = "\u001b[32mFile   : " # green
__INHERIT = "\u001b[33mInherit: " # yellow
__DUPLICATE = "\u001b[33mDuplica: " # yellow
__SEARCH  = "\u001b[31mFound  : " # read
__INCLUDE = "\u001b[36mInclude: " # cyan
__NONE    = "\u001b[0m"           # reset


__NO_ERROR    = "\u001b[32m" # green
__WARNING = "\u001b[33m" # yellow
__FATAL  = "\u001b[31m" # read
__INFO = "\u001b[36m" # cyan


def print_usage():
    print(__FATAL, "Usage: %s $android_root $root_mk_file $target" % sys.argv[0])
    print(__NONE)


def indent(level, type, line, linenum = -1):
    print(type, end="")
    for _ in range(level):
        print("  ", end="")
    print(line, end="")
    if linenum != -1:
        print(" (%d)" % linenum, end="")
    print(__NONE)


def find(android_root, mk_file, level, type, search_target, mk_files):
    file = android_root + os.path.sep + mk_file
    if exists(file):
        if file in mk_files:
            indent(level, __DUPLICATE, mk_file)
            return
        else:
            mk_files.add(file)
        indent(level, type, mk_file)
        with open(file, "r") as f:
            for index, line in enumerate(f.readlines()):
                line = line.strip()
                if line.startswith("$(call inherit-product"):
                    line = line.replace("$(SRC_TARGET_DIR)", "build/target")
                    line = line.split(",")[1]
                    line = line[:-1]
                    line = line.strip()
                    
                    find(android_root, line, level+1, __INHERIT, search_target, mk_files)
                if line.startswith("include"):
                    line = line.split(" ")[1]
                    line = line.strip()
                    find(android_root, line, level+1, __INCLUDE, search_target, mk_files)
                if search_target in line:
                    indent(level+1, __SEARCH, line, index + 1)


if len(sys.argv) >= 4:
    android_root = sys.argv[1]
    root_mk_file = sys.argv[2]
    search_target = sys.argv[3]

    mk_files = set()

    print("Search for\n\u001b[31m" + search_target + "\u001b[0m\nin");
    find(android_root, root_mk_file, 0, __FILE, search_target, mk_files)
else:
    print_usage()