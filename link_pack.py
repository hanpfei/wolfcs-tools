#!/usr/bin/python
# -*- coding: UTF-8 -*-

import getopt
import os
import shutil
import sys
import zipfile


def printUsageAndExit(code):
    print("NAME")
    print("    link_pack.py - pack kada link\n")
    print("SYNOPSIS")
    print("    module_build.py [OPTION]...\n")
    print("DESCRIPTION")
    print("    -r, --root_path ROOT_PATH")
    print("        specify the root path of kada-link project, e.g. "
          "ROOT_PATH_OF_KADA_LINK")
    print("    -o, --output_dir OUTPUT_DIR_PATH")
    print("        specify output dir path of target files.")
    print("    -h, --help")
    print("        print this message")
    sys.exit(code)


def copy_obj_files(link_root_path, output_dirpath):
    if (os.path.exists(output_dirpath)):
        shutil.rmtree(output_dirpath)
    os.mkdir(output_dirpath)

    resource_dir_path = link_root_path + os.path.sep + "kada-link" + os.path.sep + "resources"

    shutil.copytree(resource_dir_path, output_dirpath + os.path.sep + "resources")

    object_dir = link_root_path + os.path.sep + "out" + os.path.sep + "Default"
    objfiles = os.listdir(object_dir)

    for objfile in objfiles:
        if objfile.endswith(".TOC"):
            continue
        if objfile.endswith(".tmp"):
            continue
        if "ninja" in objfile:
            continue

        objfilepath = object_dir + os.path.sep + objfile
        if os.path.isdir(objfilepath):
            continue

        objfilepath = object_dir + os.path.sep + objfile
        shutil.copy(objfilepath, output_dirpath + os.path.sep + objfile)


def compress(output_dir):
    output_dir_name = "KadaLink"
    output_dirpath = output_dir + os.path.sep + output_dir_name
    zipfilename = output_dir + os.path.sep + output_dir_name + ".zip"

    if (os.path.exists(zipfilename)):
        os.remove(zipfilename)

    z = zipfile.ZipFile(zipfilename, 'w', zipfile.ZIP_DEFLATED)  # 参数一：文件夹名
    for dirpath, dirnames, filenames in os.walk(output_dirpath):
        fpath = dirpath.replace(output_dirpath, '')  # 这一句很重要，不replace的话，就从根目录开始复制
        fpath = fpath and fpath + os.sep or ''  # 这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
        for filename in filenames:
            z.write(os.path.join(dirpath, filename), fpath + filename)
    z.close()

    return zipfilename



def main():
    try:
        options, args = getopt.getopt(sys.argv[1:], "hr:o:",
                                      ["help", "root_path=", "output_dir="])
    except getopt.GetoptError:
        sys.exit()

    link_root_path = None
    output_dir = None
    for name, value in options:
        if not name:
            printUsageAndExit(1)
        if name in ("-h", "--help"):
            printUsageAndExit(0)
        if name in ("-r", "--root_path"):
            link_root_path = value
        if name in ("-o", "--output_dir"):
            output_dir = value

    if not link_root_path:
        print("No link root path argument exist")
        printUsageAndExit(1)
    if not output_dir:
        print("No output directory path argument exist")
        printUsageAndExit(1)

    if not os.path.exists(link_root_path):
        print("Link root path does not exist: " + str(link_root_path))
        printUsageAndExit(1)
    if not os.path.exists(output_dir):
        print("Output directory does not exist: " + str(output_dir))
        printUsageAndExit(1)

    output_dir_name = "KadaLink"
    output_dirpath = output_dir + os.path.sep + output_dir_name

    copy_obj_files(link_root_path, output_dirpath)

    zipfilepath = compress(output_dir)
    print("Zipfilepath: " + str(zipfilepath))


if __name__ == '__main__':
    main()


