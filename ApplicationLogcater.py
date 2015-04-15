#!/usr/bin/python

import commands
import getopt
import os
import re
import subprocess
import sys
import thread
import time

adb_path = "/media/data/dev_tools/adt-bundle-linux-x86_64-20140624/sdk/platform-tools/adb"

g_app_pid = ""

def usage():
    print "Usage: " + sys.argv[0] + " -s device_name -a app_name"


def get_app_pid(device_name, app_name):
    # print "device name = " + device_name + ", app_name = " + app_name
    command = adb_path + " -s " + str(device_name) + " shell ps | grep " + app_name
    # print "cmd = " + command
    # (status, output) = commands.getstatusoutput(command)
    # print "status = " + str(status) + " output = " + str(output)
    cmd_result = os.popen(command)
    app_info = cmd_result.readline()
    # print "app_info = " + app_info

    pattern = re.compile('\w+\s+(\d+)\s+\d+\s+\d+\s+\d+\s+\w+\s+\d+\s+\w+\s+.+$')
    match = pattern.match(app_info.strip())
    app_pid = ""
    if match:
        app_pid = match.group(1)
    return app_pid

def logcat_app(device_name, app_name):
    logcat_format = " -v threadtime "
    command = adb_path + " -s " + str(device_name) + " logcat " + logcat_format
    print "cmd = " + command + " app_id = " + g_app_pid + " " + app_name
    popen = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    log_pattern = re.compile('(\S+\s+\S+)\s+(\d+)(.+)$')
    while True:
        log = popen.stdout.readline().strip()
        match = log_pattern.match(log)
        if match:
            pid = match.group(2)
            if (pid == g_app_pid):
                print str(match.group(1)) + " " + app_name + " " + str(match.group(2)) + str(match.group(3))

def get_app_pid_run(device_name, app_name):
    global g_app_pid
    while True:
        app_pid = get_app_pid(device_name, app_name)
        if (g_app_pid != app_pid):
            g_app_pid = app_pid
            print "new g_app_id = " + g_app_pid

        time.sleep(5)


if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "s:a:h")
    device_name = ""
    app_name = ""
    for op, value in opts:
        if op == "-s":
            device_name = value
        elif op == "-a":
            app_name = value
        elif op == "-h":
            usage()
            sys.exit()

    if app_name == "":
        usage()
        sys.exit()

    thread.start_new_thread(get_app_pid_run, (device_name, app_name))
    logcat_app(device_name, app_name)

