#coding:utf-8
#created:2017/06/21
#__author__:jiaqiying
#discript:get page content

import requests
import chardet
from Queue import Empty

from bs4 import BeautifulSoup
from parser import get_page_data_list
from utils import detect_url
from utils import html_encode






class PageContentCrawer:
	"""根据进入的url抓取所需内容"""

	def __init__(self, url):
		self.base_url = url
		self.__page_content = dict()
		self.__page_item_list = []
		self.crawled_url_list = []


	def common_item_collection(self, url):
		page_src = detect_url(url, 'normal')
		if page_src:
			# html_src = html_encode(page_src)
			# html_src = html_src.decode('utf-8')
			# html_src = html_src.replace('\n', '')
			self.__page_item_list = get_page_data_list(page_src, url)
		return self.__page_item_list


def get_item_collection(url):
	page_item_list = []
	page_src = detect_url(url,'normal')
	if page_src:
		# print page_src
		page_item_list = get_page_data_list(page_src, url)
	return page_item_list


def get_item_collection_for_multi(task_queue, result_queue):
    while True:
        try:
            url = task_queue.get(timeout=1)
        except Empty:
            break
        page_src = detect_url(url,'normal')
        if page_src:
            page_item_list = get_page_data_list(page_src, url)
            result_queue.put(page_item_list)
        task_queue.task_done()
