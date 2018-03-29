import os;
import sys;
import string;

def print_usage_and_exit():
    print(sys.argv[0] + " [dir_path]")
    exit(1)

def calculateCodeScale(root_path, print_file_lines=False):
    total_line_num = 0
    filelist = []
    filelist.append(root_path);
    while len(filelist) > 0:
        file = filelist[0]
        filelist.remove(file)
        if os.path.isdir(str(file)):
            files = os.listdir(str(file))
            for subFile in files:
                sub_file_path = file + os.path.sep + subFile
                filelist.append(sub_file_path)
        elif os.path.isfile(str(file)):
            if (str(file).endswith("java") or str(file).endswith("cpp")
                or str(file).endswith(".h") or str(file).endswith(".c")
                or str(file).endswith(".cc") or str(file).endswith(".scala")
                or str(file).endswith(".go")):
                if (file.find("R.java") != -1):
                    continue
                if (file.find("BuildConfig.java") != -1):
                    continue
                # if (file.find("nostra13") != -1):
                #     continue
                if (file.find("json") != -1):
                    continue
                if (file.find("DShowBaseClasses") != -1):
                    continue
                # if (file.find("ortp") != -1):
                #     continue
                if (file.find("poco") != -1 or file.find("Poco") != -1):
                    continue
                # if (file.find("testProgs") != -1):
                #     continue
                # if (file.find("WindowsAudioInputDevice") != -1):
                #     continue
                if (file.find("test") != -1):
                    continue
                if (file.find("tools") != -1):
                    continue
                if (file.find("ftp") != -1):
                    continue
                if (file.find("websockets") != -1):
                    continue
                if (file.find("tcp_subr.c") != -1):
                    continue
                fp = open(file, "r+")
                try:
                    linenum = len(fp.readlines())
                except Exception:
                    pass

                total_line_num += linenum
                if print_file_lines:
                    print("file = " + str(file) + " : " + str(linenum))
    if total_line_num > 0:
        print("|  %s   |  %s  |" %(os.path.basename(root_path), str(total_line_num)))
    return total_line_num > 0, total_line_num

def countCodeScaleInSubDirs(root_dir_path):
    print("| 模块名称        | 代码规模    |")
    print("|----------------|-----------:|")
    dir_num = 0
    all_code = 0;
    if os.path.isdir(str(root_dir_path)):
        dirs = os.listdir(str(root_dir_path))
        dirs.sort()
        for sub_dir in dirs:
            if sub_dir == "build" or sub_dir == "doc" or sub_dir == ".gradle" or sub_dir == ".git"\
                    or sub_dir == "gradle" or sub_dir == ".idea" or sub_dir == "captures" \
                    or sub_dir == "git-batch" or sub_dir == "gitlab-monitor" or sub_dir == "nei-monitor":
                continue
            sub_dir_path = root_dir_path + os.path.sep + sub_dir

            if os.path.isdir(str(sub_dir_path)):
                valid_module, codescale = calculateCodeScale(sub_dir_path)
                if valid_module:
                    dir_num = dir_num + 1
                    all_code = all_code + codescale

    print("Directory numbers: %s, total code: %s" % (str(dir_num), str(all_code)))

    return


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage_and_exit()

    dirpath = sys.argv[1]
    print("dirpath = " + dirpath)

    countCodeScaleInSubDirs(dirpath)