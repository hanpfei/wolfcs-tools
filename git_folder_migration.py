#!/usr/bin/env python

import git
import os
import sys
import git_patch

__NO_ERROR    = "\u001b[32m" # green
__WARNING = "\u001b[33m" # yellow
__FATAL  = "\u001b[31m" # read
__INFO = "\u001b[36m" # cyan
__NONE    = "\u001b[0m"           # reset

def print_usage_and_exit(msg):
    basename = os.path.basename(sys.argv[0])
    print(__FATAL, "Failed for: " + msg, __NONE)
    print(__FATAL, "Usage: python " + basename + " [src_repo_path] [dst_repo_path] [sub_dir_path] [from_tag] [to_tag]", __NONE)
    print(__INFO, "For example: python " + basename + " ~/data/linux_official ~/data/linux_local sound/soc/sof v5.10 v6.6", __NONE)
    exit(1)


# Destination commits should contain all source commits, and the location 
# in src commits and in dst commits should be same.
def verify_commits(src_commits, dst_commits):
    for i in range(1, len(src_commits) + 1):
        src_commit_id = str(src_commits[-i])
        dst_commit_id = str(dst_commits[-i])
        if src_commit_id != dst_commit_id:
            print("Position " + str(i) + ":", "Incorrect commit " + src_commit_id, dst_commit_id)
    return True


def main():
    if (len(sys.argv) < 6):
        print_usage_and_exit("Missing arguments")
    src_repo_path = sys.argv[1]
    dst_repo_path = sys.argv[2]
    sub_dir_path = sys.argv[3]
    src_tag = sys.argv[4]
    to_tag = sys.argv[5]

    if not os.path.exists(src_repo_path) or not os.path.isdir(src_repo_path):
        print_usage_and_exit("Source repo directory does not exists or invalid: %s" % src_repo_path)
    if not os.path.exists(dst_repo_path) or not os.path.isdir(dst_repo_path):
        print_usage_and_exit("Destination repo directory does not existsor invalid: %s" % dst_repo_path)

    sub_path = os.path.join(src_repo_path, sub_dir_path)
    if not os.path.exists(sub_path) or not os.path.isdir(sub_path):
        print_usage_and_exit("Sub directory does not exists or invalid: %s" % sub_path)

    if src_repo_path == dst_repo_path:
        print_usage_and_exit("Source and destination repo path is same: %s" % src_repo_path)

    src_repo = git.Repo(src_repo_path)
    src_sub_dir_commits = list(src_repo.iter_commits(rev=src_tag, paths=[sub_dir_path]))
    dst_sub_dir_commits = list(src_repo.iter_commits(rev=to_tag, paths=[sub_dir_path]))

    src_sub_dir_commits_count = len(src_sub_dir_commits)
    dst_sub_dir_commits_count = len(dst_sub_dir_commits)

    if dst_sub_dir_commits_count <= src_sub_dir_commits_count:
        print_usage_and_exit("Something wrong, dst commits count %d "\
                             "is smaller than src commits count %d" 
                             % (dst_sub_dir_commits_count, src_sub_dir_commits_count))

    if not verify_commits(src_sub_dir_commits, dst_sub_dir_commits):
        print_usage_and_exit("Verify commits failed")

    diff_commits_count = dst_sub_dir_commits_count - src_sub_dir_commits_count
    
    diff_commits = dst_sub_dir_commits[:diff_commits_count]
    print(__NO_ERROR, "First commit " 
          + str(diff_commits[0]) + ", last commit " + str(diff_commits[-1]), __NONE)
    diff_commits.reverse();
    print(__NO_ERROR, "First commit " 
          + str(diff_commits[0]) + ", last commit " + str(diff_commits[-1]), __NONE)
    
    print(__NO_ERROR, "Diff_commits count " + str(len(diff_commits)), __NONE)
    print(__WARNING, "src_sub_dir_commits count " + str(len(src_sub_dir_commits)), 
          "dst_sub_dir_commits count " + str(len(dst_sub_dir_commits)), __NONE)


if __name__ == "__main__":
    main()