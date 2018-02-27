import os;
import sys;
import string;

def print_usage_and_exit():
    print(sys.argv[0] + " [dir_path]")
    exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage_and_exit()

    dirpath = sys.argv[1];
    total_line_num = 0;
    filelist = []
    print("dirpath = " + dirpath)
    filelist.append(dirpath);
    print("filelist = " + str(filelist))
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
                if (file.find("nostra13") != -1):
                    continue
                if (file.find("json") != -1):
                    continue
                if (file.find("DShowBaseClasses") != -1):
                    continue
                # if (file.find("ortp") != -1):
                #     continue
                if (file.find("poco") != -1 or file.find("Poco") != -1) :
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
                print ("file = " + str(file) + " : " + str(linenum))
    print("total line num = " + str(total_line_num))