#coding: utf-8
import re

from config import entrance_file_dir
from page_content_crawl.page_crawler import get_item_collection
from page_next_parser.next_parser import get_next_url_list

from page_content_crawl.parser import get_all_entrances

from config import logger
from utils import detect_url


def test_frame():
	all_entrance = get_all_entrances(entrance_file_dir)
	count = 0
	for enter in all_entrance:
		print enter['url']
		page_src = detect_url(enter['url'],'normal')
		regex = r"frame"
		pattern = re.compile(regex)

		if page_src:
			result = re.search(pattern, page_src)
			if result:
				count+=1
				print count
	print "count:%s"%count
def test_get_items():
	all_entrance = get_all_entrances(entrance_file_dir)  # 从奥博文件中获取所有url项
	print 'all url count:%s' % str(len(all_entrance))
	success_count = 0
	for enter in all_entrance:
		print enter['url']
		item_list = get_item_collection(enter['url'])
		if len(item_list) <3:
			success_count+=1
			print success_count
	print "sum:%s"%success_count


if __name__ == "__main__":
	all_entrance = get_all_entrances(entrance_file_dir)      # 从奥博文件中获取所有url项
	print 'all url count:%s'%str(len(all_entrance))
	success_count = 0
	for enter in all_entrance:
		next_url_list = get_next_url_list(enter['url'])      # 获取单个url对应的url_list
		if len(next_url_list) >= 2:                           # 如果分页list长度大于2，即认为提取成功（默认首页在list中）
			success_count+=1
			print success_count
		else:
			logger.error('fail get next_url_list %s'%enter['url'])
	print 'success_count:%s'%str(success_count)


