#coding=utf-8

import types
import urllib
import json
import codecs
import sys
import importlib
importlib.reload(sys)

from common.common import *

def log(info):
    print (info)


GROUP_URLS = [
    # edu-public-android
    "https://g.hz.netease.com/api/v3/groups/4217?private_token=yPz5i_kdNVtRrSh5p-Ga",
    # edu-android
    "https://g.hz.netease.com/api/v3/groups/3438?private_token=yPz5i_kdNVtRrSh5p-Ga"]

PROJECTS = getFilePath("FILE_PROJECTS")
PROJECTS_SSH_URLS = getFilePath("FILE_PROJECTS_SSH_URLS")

# Get project group info from edu-android and edu-public-android groups.
def getProjects(url):
    try:
        data = urllib.urlopen(url).read()
        return data
    except Exception as e:
        print(e)

#提取所有工程名，输出到 file_name 文件夹中
def exportProjectsNames(file_name):
    output_array = []
    file = codecs.open(file_name, 'w', 'utf-8')
    try:
        for url in GROUP_URLS:
            data = getProjects(url)
            tarObj = json.loads(data)
            for project in tarObj.get('projects'):
                project = project.get('path')
                output_array.append(project + "\n")
        file.writelines(sorted(output_array))
    finally:
        file.close()
    info = file_name + " 已被更新"
    log(info)


#提取所有工程名ssh路径，输出到 file_name 文件夹中
def exportProjectsSSHUrls(file_name):
    output_array = []
    file = codecs.open(file_name, 'w', 'utf-8')
    try:
        for url in GROUP_URLS:
            data = getProjects(url)
            tarObj = json.loads(data)
            for project in tarObj.get('projects'):
                output_array.append(project.get('ssh_url_to_repo') + "\n")
        file.writelines(sorted(output_array))
    finally:
        file.close()
    info = file_name + " 已被更新"
    log(info)



if __name__ == "__main__":
    info = "=======从 git 仓库中拉取所有的工程，将列表分别放到 projects.txt & projects_ssh_urls.txt 两个文件中======"
    log(info)

    exportProjectsNames(PROJECTS)
    exportProjectsSSHUrls(PROJECTS_SSH_URLS)


