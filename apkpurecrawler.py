#!/usr/bin/env python3

#
# Required Modules
# - beautifulsoup4
# - html5lib
# - requests
#

import http.client
import logging
import multiprocessing
import os
import re
import requests
import sys

from bs4 import BeautifulSoup
import unicodedata


class ApkPureCrawler(object):
    def __init__(self):
        pass


    def parseRedirectPage(self, url):

        session = requests.Session()
        resp    = session.get(url)
        html    = unicodedata.normalize("NFKD", resp.text).encode("ascii", "ignore")

        if resp.status_code == http.client.OK:
            try:
                dom = BeautifulSoup(html, 'html5lib')
                download_src = dom.find("a", {"id": "download_link", "class": "ga"})["href"]
                apkName = dom.find("span", class_ = "file").text
                # Open the url
                session = requests.Session()
                r = session.get(download_src)
                outputFile = os.path.join(os.getcwd() + "/test/", apkName)
                with open(outputFile, 'wb') as local_file:
                    local_file.write(r.content)
            except:
                logging.exception('!!! Error parsing html from: "{0}"'.format(url))
    # END: def parseRedirectPage

    def checkApp(self):
        url = "https://apkpure.com/dating"
        session = requests.Session()
        resp    = session.get(url)
        html    = unicodedata.normalize('NFKD', resp.text).encode('ascii', 'ignore')

        num_apps = 1

        if resp.status_code == http.client.OK:
            try:
                dom = BeautifulSoup(html, 'html5lib')
                class_page = dom.find("ul", class_ = "category-template")
                src = class_page.find_all("a", {"rel" : "nofollow"}, href = True)
                for a_tag in src:
                    if num_apps > 0:
                        self.parseRedirectPage("https://apkpure.com" + a_tag["href"])
                        num_apps = num_apps - 1
            except:
                logging.exception('!!! Error parsing html from: "{0}"'.format(url))


    # END: def checkApp:

# END: class ApkPureCrawler


if __name__ == "__main__":

    crawler = ApkPureCrawler()
    crawler.checkApp()






"""
def get_request_package_name():
    with open(inputFile) as requestList:
        line = requestList.readline()
        while line:
            yield line
            line = requestList.readline()
"""
