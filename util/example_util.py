import re
import requests


def get_page_content(url):
    return requests.get(url).text


def get_page_href_list(content):
    return re.findall('href="(http[^"]*)"', content)
