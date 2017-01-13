#!/usr/bin/python

import json
import os
import re
import sys

def usage():
    basename = os.path.basename(sys.argv[0])
    print (str(basename) + " [test_data_file_path]")
    exit(1)


def parse_statistics_item(statistics_json_str_item, total_statistics):
    statistics_json_item = json.loads(statistics_json_str_item)
    libname = statistics_json_item["netlib"]
    url = statistics_json_item["url"]
    receivedBytes = statistics_json_item["receivedBytes"]
    requestTime = statistics_json_item["time"]

    if not url in total_statistics:
        total_statistics[url] = {}
    if not libname in total_statistics[url]:
        total_statistics[url][libname] = {}

    if receivedBytes > 0 and requestTime < 10000:
        if not "totalTime" in total_statistics[url][libname]:
            total_statistics[url][libname]["totalTime"] = requestTime
        else:
            total_statistics[url][libname]["totalTime"] += requestTime

        if not "totalItemNum" in total_statistics[url][libname]:
            total_statistics[url][libname]["totalItemNum"] = 1
        else:
            total_statistics[url][libname]["totalItemNum"] += 1

        if not "libname" in total_statistics[url][libname]:
            total_statistics[url][libname]["libname"] = libname

        if not "url" in total_statistics[url][libname]:
            total_statistics[url][libname]["url"] = url

        total_statistics[url][libname]["length"] = receivedBytes


def compute_average_time(total_statistics):
    urls = total_statistics.keys()
    for url in urls:
        libnames = total_statistics[url].keys()
        for lib in libnames:
            if total_statistics[url][lib]:
                total_statistics[url][lib]["averageTime"] = total_statistics[url][lib]["totalTime"] / total_statistics[url][lib]["totalItemNum"]

def print_plain_statistics(total_statistics):
    urls = total_statistics.keys()
    urls = sorted(urls)

    line70 = ""
    for i in range(70):
        line70 = line70 + "-"

    line20 = ""
    for i in range(20):
        line20 = line20 + "-"

    print("|%-70s|%-20s|%-20s|%-20s|" % ("Url", "Library", "Length", "averageTime"))
    print("|%-70s|%-20s|%-20s|%-20s|" % (line70, line20, line20, line20))
    for url in urls:
        total_statistics[url]
        libnames = total_statistics[url].keys()
        libnames = sorted(libnames)
        for libname in libnames:
            if total_statistics[url][libname]:
                # print(str(total_statistics[url][libname]))
                print("|%-70s|%-20s|%-20d|%-20d|" % (url, libname, total_statistics[url][libname]["length"],
                                                          total_statistics[url][libname]["averageTime"]))
                # print(str(total_statistics[url]))


def print_statistics(total_statistics):
    urls = total_statistics.keys()
    urls = sorted(urls)
    libnames = total_statistics[urls[0]].keys()
    libnames = sorted(libnames)

    print(str(libnames))
    if len(libnames) == 2:
        print("%-50s%-20s%-20s%-20s" % ("Url", "data size(bytes)", libnames[0] + "(ms)",
                                                  libnames[1] + "(ms)"))
    elif len(libnames) == 3:
        print("%-50s%-20s%-20s%-20s%-20s" % ("Url", "data size(bytes)", libnames[0] + "(ms)",
                                                  libnames[1] + "(ms)", libnames[2] + "(ms)"))
    elif len(libnames) == 4:
        print ("%-50s%-20s%-20s%-20s%-20s%-20s" % ("Url", "data size(bytes)", libnames[0] + "(ms)",
                                                       libnames[1] + "(ms)", libnames[2] + "(ms)",
                                                       libnames[3] + "(ms)"))

        for url in urls:
            libnames = total_statistics[url].keys()
            libnames = sorted(libnames)
            print ("%-50s%-20d%-20d%-20d%-20d%-20d" % (url, total_statistics[url][libnames[0]]["length"],
                                                   total_statistics[url][libnames[0]]["averageTime"],
                                                   total_statistics[url][libnames[1]]["averageTime"],
                                                   total_statistics[url][libnames[2]]["averageTime"],
                                                   total_statistics[url][libnames[3]]["averageTime"]))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
    perf_test_data_path = sys.argv[1]

    if not os.path.exists(perf_test_data_path):
        usage()

    fp = open(perf_test_data_path, 'r+');
    all_test_lines = fp.readlines()

    total_statistics = {}
    pattern = re.compile(r".+statistics=(\{.+\}$)")
    for line in all_test_lines:
        line = line.strip()
        matcher = pattern.match(line)
        if matcher:
            statisticsJsonStrItem = matcher.group(1)

            parse_statistics_item(statisticsJsonStrItem, total_statistics)

    compute_average_time(total_statistics)
    print_plain_statistics(total_statistics)