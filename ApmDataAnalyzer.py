# -*- coding: utf-8 -*-

import re
import json
import sys
# from urlparse import urlparse
from urllib.parse import urlparse

class Header:
    header_name = ""
    occur_num = 0
    values = {}

    def __init__(self, header_name):
        self.header_name = header_name
        self.occur_num = 0
        self.values = {}

    def __str__(self):
        return self.header_name + ": " + str(self.occur_num) + "; values: " + str(self.values)

class HostItem:
    def __init__(self, product, host, count):
        self.product = product
        self.host = host
        self.count = count

    def __str__(self):
        return "%-40s %-60s %20d" % (self.product, self.host, self.count)


class HeaderAndValue:
    header_name = ""
    value = ""
    occur_num = 0
    def __init__(self, header_name, value, occur_num):
        self.header_name = header_name
        self.value = value
        self.occur_num = occur_num

    def __str__(self):
        return self.header_name + " : " + str(self.value) + " : " + str(self.occur_num)

def handleHeaders(statistics, headers):
    if headers and bool(headers):
        for header_name, header_value in headers.items():
            header = Header(header_name)
            if header_name in statistics:
                header = statistics[header_name]
            header.occur_num = header.occur_num + 1
            if header_value in header.values:
                header.values[header_value] = header.values[header_value] + 1
            else:
                header.values[header_value] = 1
            statistics[header_name] = header

def handleStatistics(statistics, file, write_file=False):
    req_header_and_values = []
    for header_name in statistics.keys():
        header_item = statistics.get(header_name)
        for value, count in header_item.values.items():
            header_and_value = HeaderAndValue(header_name=header_name, value=value, occur_num=count)
            req_header_and_values.append(header_and_value)

    req_header_and_values = sorted(req_header_and_values, key=lambda header_and_value: header_and_value.occur_num)
    req_header_and_values.reverse()

    if write_file:
        for header_and_value in req_header_and_values:
            file.write(str(header_and_value) + "\n")

    print(str("\n".join(sorted(statistics.keys()))))

def handle_url(hosts_statistics, productKey, url):
    if productKey not in hosts_statistics:
        hosts_statistics[productKey] = {}

    parse_result = urlparse(url)
    scheme = parse_result.scheme
    if (scheme == "http" or scheme == "https") and not url.startswith("http://127.0.0.1"):
        host = scheme + "://" + parse_result.netloc
        if host not in hosts_statistics[productKey]:
            hosts_statistics[productKey][host] = 0

        hosts_statistics[productKey][host] += 1

if __name__ == "__main__":
    pattern = re.compile(".+message:({.+})$");
    file = open("/home/hanpfei0306/apm-test-server-consumer.log")

    request_statistics = {}
    response_statistics = {}

    hosts_statistics = {}

    for line in file.readlines():
        mat = pattern.match(line)
        if mat:
            message = mat.group(1)
            jobj = json.loads(message)
            if "requestHeaders" in jobj:
                requestHeaders = jobj.get("requestHeaders")
                handleHeaders(request_statistics, requestHeaders)

            if "responseHeaders" in jobj:
                responseHeaders = jobj.get("responseHeaders")
                handleHeaders(response_statistics, responseHeaders)

            if "url" in jobj:
                url = jobj.get("url")
                productKey = jobj.get("productKey")
                handle_url(hosts_statistics, productKey, url)
                if url.startswith("file") or url.startswith("http://127.0.0.1"):
                    print(line.strip())

    # file.close()
    #
    # file = open("/home/hanpfei0306/app.log.result1", "w+")
    #
    # handleStatistics(request_statistics, file, True)
    # handleStatistics(response_statistics, file, True)

    # file.write(str(hosts_statistics))
    # print(str(hosts_statistics))
    # file.close()


    hostItems = {}
    for product in hosts_statistics:
        if product not in hostItems:
            hostItems[product] = []
        product_host = hosts_statistics[product]
        for hostname in product_host:
            hostItem = HostItem(product=product, host=hostname, count=hosts_statistics[product][hostname])
            hostItems[product].append(hostItem)

    for product in hostItems:
        productHostItems = hostItems[product]
        productHostItems = sorted(productHostItems, key=lambda host_item: host_item.count)
        productHostItems.reverse()
        for productHostItem in productHostItems:
            print(str(productHostItem).strip())



