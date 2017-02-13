#!/usr/bin/env python
#coding: utf-8

import datetime
import smtplib
import sys
import time

from email.mime.text import MIMEText
from email.header import Header
from jinja2 import Environment, PackageLoader
from xml.etree import ElementTree

SubjectFormatter = 'Webcache数据统计（考拉）日报 - %s'

smtpserver = ''

sender = ""
username = ''
password = ''

receivers = []
ccs = []

def print_usage_and_exit():
    print(sys.argv[0] + " [dir_path]")
    exit(1)

def get_child_node(rootnode, child_field_name):
    nodes = rootnode.getiterator(child_field_name)
    node_value = nodes[0].text
    # print(child_field_name + " = " + node_value)
    return node_value

def get_child_node_list(rootnode, child_field_name):
    nodes = rootnode.getiterator(child_field_name)
    child_node_list = []
    for node in nodes:
        child_node_list.append(node.text)
    # print(str(child_node_list))
    return child_node_list

def parse_config(config_file_path = None):
    global smtpserver
    global sender
    global username
    global password
    global receivers
    global ccs

    if config_file_path == None:
        config_file_path = "config.xml"
        root = ElementTree.parse(config_file_path)

        smtpserver = get_child_node(root, "smtpserver")
        sender = get_child_node(root, "sender")
        username = get_child_node(root, "username")
        password = get_child_node(root, "password")

        receivers = get_child_node_list(root.getiterator("receivers")[0], "email")
        ccs = get_child_node_list(root.getiterator("ccs")[0], "email")

def construct_subject():
    date = datetime.datetime.now().strftime("%Y/%m/%d")
    subject = SubjectFormatter % date
    return subject

def send_mail(page_content):
    msg = MIMEText(page_content, 'html', 'utf-8')
    subject = construct_subject()
    msg['Subject'] = msg['Subject'] = Header(subject, 'utf-8')
    msg['To'] = ",".join(receivers)
    msg['CC'] = ",".join(ccs)

    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)

    smtp.send_message(msg, sender, receivers + ccs)

    smtp.quit()

def get_query_range():
    today = datetime.date.today()

    now = datetime.datetime.now()
    timestamp = time.mktime(now.timetuple())
    one_week_ago = today.fromtimestamp(timestamp - 7 * 24 * 60 * 60)
    today_str = today.strftime("%Y-%m-%d")
    one_week_ago_str = one_week_ago.strftime("%Y-%m-%d")

    return one_week_ago_str, today_str

def mock_data():
    android_meta_data = {}
    android_meta_data['statTime'] = datetime.datetime.now().strftime("%Y-%m-%d")

    ios_meta_data = {}
    ios_meta_data['statTime'] = datetime.datetime.now().strftime("%Y-%m-%d")

    android_datas = []
    android_data1 = {}
    android_data1['date'] = datetime.datetime.now().strftime("%Y-%m-%d")
    android_data1['totalRequestFileNumber'] = 641063
    android_data1['cacheHitFileNumber'] = 4359
    android_data1['cacheHitFilePercent'] = 0.00679964371676
    android_data1['cacheHitFileTotalSize'] = 1187792050
    android_data1['resrouceTotalSize'] = 7792050
    android_data1['networkType'] = "Mobile"
    android_datas.append(android_data1)

    android_data1 = {}
    android_data1['date'] = datetime.datetime.now().strftime("%Y-%m-%d")
    android_data1['totalRequestFileNumber'] = 687539
    android_data1['cacheHitFileNumber'] = 5539
    android_data1['cacheHitFilePercent'] = 0.00805627026249
    android_data1['cacheHitFileTotalSize'] = 1503460872
    android_data1['resrouceTotalSize'] = 3460872
    android_data1['networkType'] = "WiFi"
    android_datas.append(android_data1)

    return android_meta_data, android_datas, ios_meta_data, android_datas

def format_integer(int_value):
    value_str = ""
    while int_value > 1000:
        remainder = int_value % 1000
        int_value = int_value / 1000
        int_value = int(int_value)
        value_str = ("%03d" % remainder) + value_str
        value_str = "," + value_str

    value_str = str(int_value) + value_str

    return value_str

def format_double2percent(double_value):
    double_value = double_value * 100
    double_str = "%-.4f" % double_value
    double_str = double_str + "%"
    return double_str

def format_integer2space(int_value):
    value_str = ""
    if int_value < 1024:
        value_str = "%d Bytes" % int_value
    elif int_value < 1024 * 1024:
        int_value /= 1024.0
        value_str = "%-.4f KBytes" % int_value
    elif int_value < 1024 * 1024 * 1024:
        int_value /= (1024.0 * 1024.0)
        value_str = "%-.4f MBytes" % int_value
    else:
        int_value /= 1024.0 * 1024.0 * 1024.0
        value_str = "%-.4f GBytes" % int_value

    return value_str

def format_data(origin_datas):
    formatted_datas = []
    for data_item in origin_datas:
        formatted_data_item = {}
        formatted_data_item['date'] = data_item['date']
        formatted_data_item['totalRequestFileNumber'] = format_integer(data_item['totalRequestFileNumber'])
        formatted_data_item['cacheHitFileNumber'] = format_integer(data_item['cacheHitFileNumber'])
        formatted_data_item['cacheHitFilePercent'] = format_double2percent(data_item['cacheHitFilePercent'])
        formatted_data_item['cacheHitFileTotalSize'] = format_integer2space(data_item['cacheHitFileTotalSize'])
        formatted_data_item['resrouceTotalSize'] = format_integer2space(data_item['resrouceTotalSize'])
        formatted_data_item['networkType'] = data_item['networkType']

        formatted_datas.append(formatted_data_item)
    return formatted_datas;

def generate_page(env, android_meta_data, android_datas, ios_meta_data, ios_datas):
    template = env.get_template('mail_template.html')

    android_datas = format_data(android_datas)
    ios_datas = format_data(ios_datas)

    return template.render(android_meta_data = android_meta_data, android_datas = android_datas,
                           ios_meta_data = ios_meta_data, ios_datas = ios_datas)

def query_data(start_date, end_date):
    android_meta_data = None
    android_datas = None
    ios_meta_data = None
    ios_datas = None

    return android_meta_data, android_datas, ios_meta_data, ios_datas

def write_page_to_file(page_content):
    page_file_path = "/home/hanpfei0306/report.html"
    with open(page_file_path, "w") as page_file_handle:
        page_file_handle.write(page_content)

if __name__ == "__main__":
    parse_config()
    query_start_date, query_end_date = get_query_range()
    android_meta_data, android_datas, ios_meta_data, ios_datas = query_data(query_start_date, query_end_date)
    android_meta_data, android_datas, ios_meta_data, ios_datas = mock_data()

    env = Environment(loader=PackageLoader('MailSender', '.'))
    page_content = generate_page(env, android_meta_data, android_datas, ios_meta_data, ios_datas)

    write_page_to_file(page_content)

    send_mail(page_content)
