#!/usr/bin/env python

import os
import re
import requests
import shutil
import sys

def print_usage_and_exit():
    print(sys.argv[0] + " [dir_path]")
    exit(1)


def handle_match(matcher, root_path):
    image_url = matcher.group(2)
    image_file_name = os.path.basename(image_url)
    image_dir_path = os.path.join(root_path, "assets/images")
    target_image_file_path = os.path.join(image_dir_path, image_file_name)

    new_image_url = "https://www.wolfcstech.com/images/" + image_file_name
    image_comment = matcher.group(1)

    # print(image_url)
    # print(image_file_name)
    # print(image_dir_path)
    # print(target_image_file_path)

    new_line = ""
    if not os.path.exists(target_image_file_path) or not os.path.isfile(target_image_file_path):
        r = requests.get(image_url)
        with open(target_image_file_path, "wb") as image_file_handle:
            image_file_handle.write(r.content)
        new_line = "![" + image_comment + "](" + new_image_url + ")\n"

    return new_line

def revise_line(line, root_path):
    new_line = line
    pattern = re.compile(r".*\!\[(.*)\]\((.+)\?.+\)")
    matcher = pattern.match(line)

    if matcher:
        # print(line)
        tmp_new_line = handle_match(matcher, root_path)
        if tmp_new_line != "":
            new_line = tmp_new_line
    else:
        pattern = re.compile(r".*\!\[(.*)\]\((.+)\)")
        matcher = pattern.match(line)
        if matcher:
            # print(line)
            tmp_new_line = handle_match(matcher, root_path)
            if tmp_new_line != "":
                new_line = tmp_new_line

    return new_line

def handle_file(file_path, root_path):
    if not os.path.isfile(file_path):
        return
    if not file_path.endswith(".md"):
        return
    bak_file_path = file_path + ".tmp"
    os.rename(file_path, bak_file_path)
    bak_file_handle = open(bak_file_path)
    new_file_handle = open(file_path, "w+")

    lines = bak_file_handle.readlines()
    for line in lines:
        new_line = revise_line(line, root_path)
        new_file_handle.write(new_line)

    bak_file_handle.close()
    new_file_handle.close()

    os.remove(bak_file_path)
    # print(file_path)


def handle_dir_with_walk(dirpath, root_path):
    list_dirs = os.walk(dirpath)

    for root, dirs, files in list_dirs:
        for fil in files:
            handle_file(os.path.join(root, fil))

def handle_dir(dirpath, root_path):
    new_dir_path = []
    dirname = os.path.basename(dirpath)
    if dirname == "themes":
        return
    subfiles = os.listdir(dirpath)

    for subfile in subfiles:
        subfile_path = os.path.join(dirpath, subfile)
        if os.path.isdir(subfile_path) and subfile_path.__contains__("source"):
            new_dir_path.append(subfile_path)
        elif os.path.isfile(subfile_path) and subfile_path.endswith(".md"):
            # print("subfile_path = " + subfile_path)
            handle_file(subfile_path, root_path)
    return new_dir_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage_and_exit()
    dirpath = sys.argv[1]
    print(dirpath)
    dirpaths = []
    dirpaths.append(dirpath)

    while len(dirpaths) > 0:
        cur_dir = dirpaths[0]
        new_dirs = handle_dir(cur_dir, dirpath)
        dirpaths.remove(cur_dir)
        if new_dirs:
            dirpaths += new_dirs
