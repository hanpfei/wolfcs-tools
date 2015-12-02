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

g_app_pid = {}

def usage():
    print "Usage: " + sys.argv[0] + " [-s device_name] -a app_name"


def get_app_pid(device_name, app_name):
    # print "device name = " + device_name + ", app_name = " + app_name
    command = adb_path
    if len(device_name) > 0:
        command = command + " -s " + str(device_name)
    command = command + " shell ps | grep " + app_name
    # print "cmd = " + command
    # (status, output) = commands.getstatusoutput(command)
    # print "status = " + str(status) + " output = " + str(output)
    cmd_result = os.popen(command)
    app_infos = cmd_result.readlines()
    # print "app_infos = " + str(app_infos)

    app_pids = {}
    app_pid = ""
    pattern = re.compile('\w+\s+(\d+)\s+\d+\s+\d+\s+\d+\s+\w+\s+\w+\s+\w+\s+(.+)$')
    for app_info in app_infos:
        match = pattern.match(app_info.strip())
        if match:
            app_pid = match.group(1)
            pkgname = match.group(2)
            print "app_id = " + str(app_pid) + " pkgname = " + str(pkgname)
            app_pids[app_pid] = pkgname

    return app_pids

def logcat_app(device_name, app_name):
    global g_app_pid

    logcat_format = " -v threadtime "
    command = adb_path
    if len(device_name) > 0:
        command = command + " -s " + str(device_name)
    command = command + " logcat " + logcat_format

    print "cmd = " + command + ", app_id = " + str(g_app_pid) + " " + app_name
    popen = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    log_pattern = re.compile('(\S+\s+\S+)\s+(\d+)(.+)$')
    while True:
        log = popen.stdout.readline().strip()
        match = log_pattern.match(log)
        if match:
            pid = match.group(2)
            for apppid in g_app_pid.keys():
                if (pid == apppid):
                    print str(match.group(1)) + " " + g_app_pid[apppid] + " " + str(match.group(2)) + str(match.group(3))

def get_app_pid_run(device_name, app_name):
    global g_app_pid
    while True:
        app_pids = get_app_pid(device_name, app_name)
        g_app_pid = app_pids
        print "new g_app_id = " + str(g_app_pid)

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

