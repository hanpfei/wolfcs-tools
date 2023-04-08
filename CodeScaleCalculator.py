from genericpath import isfile
import os
import sys

ignore_dir_list = [
    "build",
    "doc",
    ".gradle",
    ".git",
    "gradle",
    ".idea",
    "captures",
    "git-batch",
    "gitlab-monitor",
    "nei-monitor",
    "fuzzer",
    "examples",
    "benchmarks",
    "fuzz"
]


valid_file_exts_list = [
    ".java",
    ".cpp",
    ".h",
    ".c",
    ".cc",
    ".scala",
    ".go",
    ".aidl",
    ".hal"
]


ignore_file_list = [
    "R.java",
    "BuildConfig.java",
    "nostra13",
    "json",
    "DShowBaseClasses",
    "poco",
    "Poco",
    "ortp",
    "testProgs",
    "WindowsAudioInputDevice",
    "test",
    "tests",
    "tools",
    "ftp",
    "websockets",
    "tcp_subr.c",
]


def print_usage_and_exit():
    print(sys.argv[0] + " [dir_path]")
    exit(1)


def isValidFileType(file):
    valid = False
    for ext in valid_file_exts_list:
        if str(file).endswith(ext):
            valid = True
            break
    return valid


def isValidFile(file):
    valid = True
    for invalid in ignore_file_list:
        if (file.find(invalid) != -1):
            # print("Skip " + invalid + ": " + file)
            valid = False
            break
    return valid


def calculateFileCodeScale(file):
    linenum = 0
    if (isValidFileType(file)):
        if (isValidFile(file)):
            fp = open(file, "r+")
            try:
                linenum = len(fp.readlines())
            except Exception:
                pass
    return linenum


def calculateCodeScale(root_path, index = 0, print_file_lines=False):
    total_line_num = 0
    filelist = []
    filelist.append(root_path);
    while len(filelist) > 0:
        file = filelist[0]
        filelist.remove(file)
        if os.path.isdir(str(file)):
            files = os.listdir(str(file))
            files = list(map(lambda curfile: file + os.path.sep + curfile, files))
            filelist = filelist + files

            # for subFile in files:
            #     sub_file_path = file + os.path.sep + subFile
            #     filelist.append(sub_file_path)
        elif os.path.isfile(str(file)):
                linenum = calculateFileCodeScale(file)
                total_line_num += linenum
                if print_file_lines:
                    print("file = " + str(file) + " : " + str(linenum))
    if total_line_num > 0:
        print("|  %d   |  %s   |  %s  |" %(index, os.path.basename(root_path), str(total_line_num)))
    return total_line_num > 0, total_line_num


def countCodeScaleInSubDirs(root_dir_path):
    index = 1
    print("| 序号        | 模块名称        | 代码规模    |")
    print("|----------------|----------------|-----------:|")
    dir_num = 0
    all_code = 0;
    if os.path.isdir(str(root_dir_path)):
        dir_or_files = os.listdir(str(root_dir_path))
        dir_or_files.sort()
        root_files_line_num = 0
        for sub_dir_or_file in dir_or_files:
            if ignore_dir_list.count(sub_dir_or_file) > 0:
                continue
            sub_file_or_dir_path = root_dir_path + os.path.sep + sub_dir_or_file

            if os.path.isdir(str(sub_file_or_dir_path)):
                valid_module, codescale = calculateCodeScale(sub_file_or_dir_path, index)
                if valid_module:
                    dir_num = dir_num + 1
                    all_code = all_code + codescale
                    index = index + 1
            elif os.path.isfile(str(sub_file_or_dir_path)):
                root_files_line_num += calculateFileCodeScale(sub_file_or_dir_path)
    if root_files_line_num > 0:
        print("|  %d   |  %s   |  %s  |" % (index, os.path.basename(root_dir_path), str(root_files_line_num)))
        all_code = all_code + root_files_line_num
    print("|  10000   |  Total   |  %s  |" % (str(all_code)))
    # print("Directory numbers: %s, total code: %s" % (str(dir_num), str(all_code)))

    return


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage_and_exit()

    dirpath = sys.argv[1]
    print("dirpath = " + dirpath)

    countCodeScaleInSubDirs(dirpath)