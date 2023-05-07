#!/usr/bin/python3

import os
import sys
import subprocess


__NO_ERROR    = "\u001b[32m" # green
__WARNING = "\u001b[33m" # yellow
__FATAL  = "\u001b[31m" # read
__INFO = "\u001b[36m" # cyan
__NONE    = "\u001b[0m"           # reset


def print_usage_and_exit():
    print(__FATAL, "Usage: %s $git_repo_path $target_remote" % sys.argv[0])
    print(__NONE)
    exit(-1)


def run_cmd(cmd, output_mode=0):
    if output_mode == 0:
        print(cmd)

    FNULL = open(os.devnull, 'w')
    if output_mode == 0:
        pipe = subprocess.Popen(cmd, stderr=sys.stderr, stdout=sys.stdout, shell=True)
    elif output_mode == 1:
        pipe = subprocess.Popen(cmd, stderr=FNULL, stdout=FNULL, shell=True)
    elif output_mode == 2:
        pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    ret = pipe.wait()
    FNULL.close()
    ret_str = ""
    if pipe.stdout:
        ret_str = pipe.stdout.read().decode().strip()
    return ret, ret_str


def clean_branch(branch_name):
    branch_name = branch_name.strip()
    if branch_name.startswith("* "):
        branch_name = branch_name[2:]
    return branch_name


def get_all_branchs():
    command = 'git branch -a '
    ret, outstring = run_cmd(command, 2)

    all_branchs = None
    if ret == 0:
        all_branchs = list(map(lambda x: x.strip(),  outstring.split('\n')))
    
    return all_branchs


def check_remote_branch_exist(new_remote_branch):
    all_branchs = get_all_branchs()
    # print("all_branchs: " + str(all_branchs))
    if all_branchs and new_remote_branch in all_branchs:
        return True
    return False


def delete_local_branch(local_branch):
    command = 'git checkout ' + "main"
    ret, outstring = run_cmd(command, 2)
    print(outstring)

    all_branchs = get_all_branchs()
    if local_branch in all_branchs:
        command = 'git branch -D ' + local_branch
        ret, outstring = run_cmd(command, 2)
        print(outstring)


def checkout_branch(local_branch, remote_branch):
    all_branchs = get_all_branchs()
    if all_branchs:
        if local_branch in all_branchs:
            command = 'git checkout ' + local_branch
        elif ("* %s" % local_branch) in all_branchs:
            command = None
        else:
            command = 'git checkout -t ' + remote_branch
    else:
        command = 'git checkout -t ' + remote_branch
    if command:
        print("Command: " + command)
        _, outstring = run_cmd(command, 2)
        print(outstring)


remote_branchs = [
    "origin/android-4.19-stable",
    "origin/android11-5.4",
    "origin/android11-5.4-lts",
    "origin/android12-5.10-2023-01",
    "origin/android12-5.10-2023-02",
    "origin/android12-5.10-2023-03",
    "origin/android12-5.10-2023-04",
    "origin/android12-5.10-2023-05",
    "origin/android12-5.10-lts",
    "origin/android12-5.4",
    "origin/android12-5.4-lts",
    "origin/android13-5.10-2023-01",
    "origin/android13-5.10-2023-02",
    "origin/android13-5.10-2023-03",
    "origin/android13-5.10-2023-04",
    "origin/android13-5.10-2023-05",
    "origin/android13-5.10-lts",
    "origin/android13-5.15",
    "origin/android13-5.15-2023-01",
    "origin/android13-5.15-2023-02",
    "origin/android13-5.15-2023-03",
    "origin/android13-5.15-2023-04",
    "origin/android13-5.15-2023-05",
    "origin/android13-5.15-lts",
    "origin/android14-5.15",
    "origin/android14-6.1",
    "origin/upstream-linux-5.10.y",
    "origin/upstream-linux-5.15.y",
    "origin/upstream-linux-5.4.y",
    "origin/upstream-linux-6.1.y"
]


def main():
    if (len(sys.argv) != 3):
        print_usage_and_exit()

    repo_path = sys.argv[1]
    git_meta_path = repo_path + os.path.sep + ".git"
    target_remote = sys.argv[2]

    if not os.path.exists(repo_path) or not os.path.isdir(repo_path)\
            or not os.path.exists(git_meta_path) or not os.path.isdir(git_meta_path):
        print(__WARNING, "Invalid git repository: " + repo_path)
        print(__NONE)
        print_usage_and_exit()

    os.chdir(repo_path)
    
    for remote_branch in remote_branchs:
        local_branch = "/".join(remote_branch.split('/')[1:])
        new_remote_branch = "remotes/%s/%s" % (target_remote, local_branch)

        if check_remote_branch_exist(new_remote_branch):
            print(__INFO, "New remote branch '%s' exists " % new_remote_branch)
            print(__NONE)
            delete_local_branch(local_branch)
            continue

        checkout_branch(local_branch, remote_branch)

        command = 'git push ' + target_remote
        ret, outstring = run_cmd(command, 2)
        if ret != 0:
            print(__WARNING, ("Command: '%s' failed: " % command) +  outstring.strip())
            print(__NONE)
        else:
            print(outstring)

        delete_local_branch(local_branch)

        if ret != 0:
            print(__FATAL, "Migrate branch %s failed!" % remote_branch)
        else:
            print(__NO_ERROR, "Migrate branch %s completed!" % remote_branch)
        print(__NONE)


if __name__ == "__main__":
    main()