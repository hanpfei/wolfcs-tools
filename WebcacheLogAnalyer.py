#!/usr/bin/python3.5

import os
import re
import sys
import urllib.request


def usage():
    basename = os.path.basename(sys.argv[0])
    print(str(basename) + " [log_file_path]")
    exit(1)


def get_file_type(url):
    res_type_extract_pattern = re.compile(r".+//.+/.+(\..+)\?.+$")
    res_type_extract_pattern2 = re.compile(r".+//.+/.+(\..+)$")
    res_type_extract_pattern3 = re.compile(r".+//.+/(.+)\?.+$")
    res_type_extract_pattern4 = re.compile(r".+//.+/(.+)$")
    webp_type_extract_pattern = re.compile(r".+//.+/.+type=webp$")
    file_type = ""
    matcher = res_type_extract_pattern.match(url)
    if not matcher:
        matcher = res_type_extract_pattern2.match(url)
    if not matcher:
        matcher = res_type_extract_pattern3.match(url)
    if not matcher:
        matcher = res_type_extract_pattern4.match(url)

    if matcher:
        file_type = matcher.group(1)
    if not file_type.__contains__("."):
        matcher = webp_type_extract_pattern.match(url)
        if matcher:
            # print(url)
            file_type = ".webp"

    return file_type


def get_res_size(res_url):
    res = urllib.request.urlopen(res_url)
    data = res.read()
    data_length = len(data)
    return data_length


def get_url_from_log_line(line):
    pattern = re.compile(r".+Get resource (.+$)")
    matcher = pattern.match(line)
    url = None
    if matcher:
        url = matcher.group(1)
    return url

# Support the output of tshark, format: tshark -i enp4s0f2 -n -f 'tcp dst port 80'  -T fields -e http.host -e http.request.uri
def get_url_from_tshark_line(line):
    url = None
    line = line.strip()
    if line:
        parts = line.split("\t")
        host = parts[0].strip()
        res_path = parts[1].strip()

        url = "http://" + host + res_path
        # print("url = " + str(url))

    return url


if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
    log_file_path = sys.argv[1]

    if not os.path.exists(log_file_path):
        usage()
    fp = open(log_file_path, 'r+')
    all_log_lines = fp.readlines()

    request_num = 0
    jpg_request_num = 0
    css_res_num = 0
    gif_res_num = 0
    html_res_num = 0
    ico_res_num = 0
    js_res_num = 0
    mp4_res_num = 0
    png_request_num = 0
    shtml_request_num = 0
    webp_request_num = 0
    others_request_num = 0

    request_with_param_num = 0

    css_static_res_num = 0
    js_static_res_num = 0


    request_with_param_pattern = re.compile(r".+/.+\?.+$")

    css_static_url_pattern = re.compile(r".+(.+\.css$)")
    js_static_url_pattern = re.compile(r".+(.+\.js)$")

    jpg_request_pattern = re.compile(r".+\.jpg.+$")
    png_request_pattern = re.compile(r".+\.png.+$")

    types = set("")
    static_resource = []
    for line in all_log_lines:
        line = line.strip()
        url = get_url_from_tshark_line(line)
        if url:
            request_num += 1
            matcher = request_with_param_pattern.match(url)
            if matcher:
                request_with_param_num += 1

            matcher = css_static_url_pattern.match(url)
            if matcher:
                static_resource.append(url)
                css_static_res_num += 1
            matcher = js_static_url_pattern.match(url)
            if matcher:
                static_resource.append(url)
                js_static_res_num += 1

            # Extract file type
            file_type = get_file_type(url)
            if not file_type:
                print(url)
            elif file_type == ".JPG":
                jpg_request_num += 1
            elif file_type == ".jpeg":
                jpg_request_num += 1
            elif file_type == ".jpg":
                jpg_request_num += 1
            elif file_type == ".css":
                css_res_num += 1
            elif file_type == ".gif":
                gif_res_num += 1
            elif file_type == ".html":
                html_res_num += 1
            elif file_type == ".ico":
                ico_res_num += 1
            elif file_type == ".js":
                js_res_num += 1
            elif file_type == ".mp4":
                mp4_res_num += 1
            elif file_type == ".png":
                png_request_num += 1
            elif file_type == ".shtml":
                shtml_request_num += 1
            elif file_type == ".webp":
                webp_request_num += 1
            else:
                others_request_num += 1
                # print(url)

            types.add(file_type)

    static_res_request_distribute = {}
    print("Static resources: " + str(len(static_resource)))
    static_resource = sorted(static_resource)
    for sorted_url in static_resource:
        if not static_res_request_distribute.__contains__(sorted_url):
            static_res_info = {}
            static_res_info["filenum"] = 1
            static_res_info["filesize"] = get_res_size(sorted_url)
            static_res_request_distribute[sorted_url] = static_res_info
        else:
            static_res_request_distribute[sorted_url]["filenum"] = int(static_res_request_distribute[sorted_url]["filenum"]) + 1

    for unique_url in sorted(static_res_request_distribute.keys()):
        print("%-100s %-10d%-10d" % (unique_url, static_res_request_distribute[unique_url]["filenum"],
                                                  static_res_request_distribute[unique_url]["filesize"]))

    print("")
    print("--------------------------------------------------------------------------")
    print("%-25s%-25s%-25s%-25s" % ("request_num", "css_static_res_num", "js_static_res_num", "request_with_param_num"))
    print("%-25d%-25d%-25d%-25d" % (request_num, css_static_res_num, js_static_res_num, request_with_param_num))

    sum = jpg_request_num + css_res_num + gif_res_num + html_res_num + ico_res_num + js_res_num + mp4_res_num \
          + png_request_num + shtml_request_num + webp_request_num + others_request_num

    print("")
    print("--------------------------------------------------------------------------")
    print("%-25s%-25d%-.4f%%" % ("Jpeg file num: ", jpg_request_num, jpg_request_num / sum * 100))
    print("%-25s%-25d%-.4f%%" % ("css_res_num: ", css_res_num, css_res_num / sum * 100))
    print("%-25s%-25d%-.4f%%" % ("js_res_num: ", js_res_num, js_res_num / sum * 100))
    print("%-25s%-25d%-.4f%%" % ("gif_res_num: ", gif_res_num, gif_res_num / sum * 100))
    print("%-25s%-25d%-.4f%%" % ("html_res_num: ", html_res_num, html_res_num / sum * 100))
    print("%-25s%-25d%-.4f%%" % ("ico_res_num: ", ico_res_num, ico_res_num / sum * 100))
    print("%-25s%-25d%-.4f%%" % ("mp4_res_num: ", mp4_res_num, mp4_res_num / sum * 100))
    print("%-25s%-25d%-.4f%%" % ("png_request_num: ", png_request_num, png_request_num / sum * 100))
    print("%-25s%-25d%-.4f%%" % ("shtml_request_num: ", shtml_request_num, shtml_request_num / sum * 100))
    print("%-25s%-25d%-.4f%%" % ("webp_request_num: ", webp_request_num, webp_request_num / sum * 100))
    print("%-25s%-25d%-.4f%%" % ("others_request_num: ", others_request_num, others_request_num / sum * 100))
    print("--------------------------------------------------------------------------")
    print("")

    print("")
    print("--------------------------------------------------------------------------")
    print("sum = " + str(sum))
    print("--------------------------------------------------------------------------")
    print("")

    print("")
    print("--------------------------------------------------------------------------")
    print("file types: ")
    for file_type in sorted(types):
        pass
        print(file_type)
    print("--------------------------------------------------------------------------")