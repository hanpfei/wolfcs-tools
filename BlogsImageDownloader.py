#!/usr/bin/env python

import os
import re
import requests
import sys
from PIL import Image

def print_usage_and_exit():
    print(sys.argv[0] + " [dir_path]")
    exit(1)


format_to_suffix = {
    "JPEG": ["jpg"],
    "PNG": ["png"],
    "WEBP": ["webp"],
}


def download_image_file(image_url, target_image_file_path):
    if not image_url.startswith("http") and not image_url.startswith("https"):
        print("Unsupported url " + image_url)
        return False

    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"
    headers = {'User-Agent': user_agent}

    r = requests.get(image_url, headers=headers)
    with open(target_image_file_path, "wb") as image_file_handle:
        image_file_handle.write(r.content)

    try:
        im = Image.open(target_image_file_path, 'r')
        str(im.format)
        im.close()
    except Image.UnidentifiedImageError as e:
        os.remove(target_image_file_path)
        print("Download image file %s failed!!!" % target_image_file_path)

    if os.path.exists(target_image_file_path):
        return True
    else:
        return False


def convert_image_format_from_webp_to_png(target_image_file_path):
    bak_image_file_path = target_image_file_path + "_bak"
    os.rename(target_image_file_path, bak_image_file_path)
    input_image = Image.open(bak_image_file_path)
    if input_image.mode != "RGB":
        input_image = input_image.convert("RGB")
    input_image.save(target_image_file_path, "PNG")

    os.remove(bak_image_file_path)


def check_image_file_ext_and_format(image_file_path):
    match = False
    ext_name = ""
    image_format = ""
    try:
        global format_to_suffix
        im = Image.open(image_file_path, 'r')
        image_format = str(im.format)
        im.close()
        ext_name = image_file_path[image_file_path.rfind(".") + 1:]
        ext_name = ext_name.upper()

        if image_format in format_to_suffix.keys():
            suffixes = format_to_suffix[image_format]
            for suffix in suffixes:
                if ext_name.upper() == suffix.upper():
                    match = True
                    break
        else:
            print("Unsupported image file %s, format %s" % (image_file_path, image_format))
    except Image.UnidentifiedImageError as e:
        os.remove(image_file_path)
        print("Invalid image file format: %s!!!" % image_file_path)

    return match, ext_name, image_format


def handle_match(matcher, root_path, file_path):
    image_url = matcher.group(2)
    image_file_name = os.path.basename(image_url)

    file_dir = os.path.abspath(os.path.join(file_path, ".."))
    image_dir_path = os.path.join(file_dir, "images")

    if not os.path.exists(image_dir_path) and not file_dir.endswith("_posts"):
        os.mkdir(image_dir_path)
    if not os.path.exists(image_dir_path):
        image_dir_path = os.path.join(root_path, "source", "images")

    target_image_file_path = os.path.join(image_dir_path, image_file_name)

    relpath = os.path.relpath(target_image_file_path, file_dir)
    new_image_url = relpath
    image_comment = matcher.group(1)

    # print(image_url)
    # print(image_file_name)
    # print(image_dir_path)
    # print(target_image_file_path)

    new_line = ""
    if image_url.find("www.wolfcstech.com") >= 0:
        new_line = "![" + image_comment + "](" + new_image_url + ")\n"
    elif not os.path.exists(target_image_file_path) or not os.path.isfile(target_image_file_path):
        if not download_image_file(image_url, target_image_file_path):
            return ""
        new_line = "![" + image_comment + "](" + new_image_url + ")\n"

    if not os.path.exists(target_image_file_path):
        print("Downlaod file %s failed" % target_image_file_path)

    (match, ext_name, image_format) = check_image_file_ext_and_format(target_image_file_path)
    if not match:
        if ext_name == "PNG" and image_format == "WEBP":
            convert_image_format_from_webp_to_png(target_image_file_path)

    return new_line


def revise_line(line, root_path, file_path):
    new_line = line
    pattern = re.compile(r".*\!\[(.*)\]\((.+)\?.+\)")
    matcher = pattern.match(line)

    if matcher:
        # print(line)
        tmp_new_line = handle_match(matcher, root_path, file_path)
        if tmp_new_line != "":
            new_line = tmp_new_line
    else:
        pattern = re.compile(r".*\!\[(.*)\]\((.+)\)")
        matcher = pattern.match(line)
        if matcher:
            # print(line)
            tmp_new_line = handle_match(matcher, root_path, file_path)
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
        new_line = revise_line(line, root_path, file_path)
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

    print("Done!!!")
