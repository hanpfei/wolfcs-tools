#!/usr/bin/python

from urllib.parse import urlparse
from urllib.parse import urljoin

import git
import html.parser
import os
import re
import requests

default_dir_name = "ROS"
ros_package_list_page_url = "http://www.ros.org/browse/list.php"

class RosPkgListPageParser(html.parser.HTMLParser):
    def __init__(self, pkg_list_page_url):
        html.parser.HTMLParser.__init__(self)
        self.pkg_list_page_url = pkg_list_page_url
        self.in_pkg_td = False
        self.current_pkg_href = None
        self.pkg_detail_pages = []

    def handle_starttag(self, tag, attrs):
        in_tag_td = False
        in_tag_a = False

        if tag == "td":
            in_tag_td = True
        elif tag == "a":
            in_tag_a = True

        for attr_name, attr_value in attrs:
            if in_tag_td and attr_name == "class" and attr_value == "pkgname":
                self.in_pkg_td = True
            elif self.in_pkg_td and in_tag_a and attr_name == "href":
                self.current_pkg_href = attr_value

    def handle_endtag(self, tag):
        if tag == "td":
            self.in_pkg_td = False

    def handle_data(self, data):
        if self.in_pkg_td and self.current_pkg_href:
            # print(self.current_pkg_href, " data  : ", data)
            pkg_detail_page_url = urljoin(self.pkg_list_page_url, self.current_pkg_href)
            self.pkg_detail_pages.append((data, pkg_detail_page_url))
            self.current_pkg_href = None

    def get_ros_pkg_detail_pages(self):
        return self.pkg_detail_pages


class RosPkgDetailPageParser(html.parser.HTMLParser):
    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        self.enter_tag_p = False
        self.enter_tag_b = False
        self.enter_tag_a = False
        self.in_source_p = False
        self.pkg_source_git_repo_url = None

    def handle_starttag(self, tag, attrs):
        if tag == "p":
            self.enter_tag_p = True
        elif tag == "b":
            self.enter_tag_b = True
        elif tag == "a":
            self.enter_tag_a = True

    def handle_endtag(self, tag):
        if tag == "p":
            self.enter_tag_p = False
            self.in_source_p = False
        elif tag == "b":
            self.enter_tag_b = False
        elif tag == "a":
            self.enter_tag_a = False

    def handle_data(self, data):
        if self.enter_tag_p and self.enter_tag_b and "Source" in data:
            self.in_source_p = True
        elif self.in_source_p and self.enter_tag_a:
            self.pkg_source_git_repo_url = data

    def get_pkg_source_git_repo_url(self):
        return self.pkg_source_git_repo_url


def clone_ros_package(pkg_name, pkg_source_git_repo_url):
    print(pkg_source_git_repo_url, pkg_name)
    url_comp = urlparse(pkg_source_git_repo_url)
    basename = os.path.basename(url_comp.path)
    dirname = os.path.splitext(basename)[0]

    if not os.path.exists(dirname):
        git.Repo.clone_from(pkg_source_git_repo_url, dirname, recursive=True)

def download_ros_package(pkg_name, pkg_detail_page_url):
    ros_package_detail_page_req = requests.get(pkg_detail_page_url)
    if ros_package_detail_page_req:
        ros_package_page_content = ros_package_detail_page_req.content.decode("utf-8")

        parser = RosPkgDetailPageParser()
        parser.feed(ros_package_page_content)
        pkg_source_git_repo_url = parser.get_pkg_source_git_repo_url();
        if not pkg_source_git_repo_url:
            print("Cannot get  source git repo url for: ", pkg_name, pkg_detail_page_url)
        else:
            clone_ros_package(pkg_name, pkg_source_git_repo_url)


def download_ros_packages(ros_pkg_detail_pages):
    print(os.getcwd())
    for (pkg_name, pkg_detail_page_url) in ros_pkg_detail_pages:
        download_ros_package(pkg_name, pkg_detail_page_url)


def request_ros_package_list_page(page_url):
    ros_package_list_page_req = requests.get(page_url)
    ros_pkg_detail_pages = []
    if ros_package_list_page_req:
        ros_list_page_content = ros_package_list_page_req.content.decode("utf-8")
        parser = RosPkgListPageParser(page_url)
        parser.feed(ros_list_page_content)
        ros_pkg_detail_pages = parser.get_ros_pkg_detail_pages()

    return ros_pkg_detail_pages

def main():
    print(os.getcwd())
    if not os.path.exists(default_dir_name):
        os.mkdir(default_dir_name)

    if not os.path.exists(default_dir_name):
        print("ROS not exist.")
        exit()
    else:
        print("ROS exist.")
    os.chdir(default_dir_name)

    ros_pkg_detail_pages = request_ros_package_list_page(ros_package_list_page_url)

    download_ros_packages(ros_pkg_detail_pages)

if __name__ == "__main__":
    main()