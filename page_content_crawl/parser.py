#coding:utf-8
#created:2017/06/21
#__author__:jiaqiying
#discript:every parsers
import urlparse
import json
from config import ZGTJXX_BASE_URL
import re
from bs4 import BeautifulSoup

# from page_content_crawl.page_crawler import PageContentCrawer
from regex_collection import PAGE_TITLE_REGEX0, ZGTJ_NEXT_PAGE_REGEX, ZGTJ_SINGLE_PAGE_REGEX,PAGE_TITLE_REGEX1
from utils import html_encode
from utils import detect_url
from config import logger


pattern_date_tail = re.compile(PAGE_TITLE_REGEX0, re.I)
pattern_date_head = re.compile(PAGE_TITLE_REGEX1, re.I)


# def parse_zgtjxx_bottom_url(page_content, url):
# 	'''针对中国信息网的底部翻页url获取'''
# 	soup = BeautifulSoup(page_content)
# 	page_info = soup.find_all('span', class_='pageinfo')
# 	# print 'page_info%s' %(page_info)
# 	page_sum = page_info[0].strong.get_text()
# 	page_content = html_encode(page_content)
# 	model_string = re.search(ZGTJ_NEXT_PAGE_REGEX, page_content).group(1)
# 	bottom_url_list = [(urlparse.urljoin(url, model_string.replace('_2.', '_'+str(i+1)+'.'))) for i in xrange(int(page_sum))]
# 	return bottom_url_list
#
#
# def parse_tjgb_page(main_page, base_url):
# 	"""在公报第一页获取其他分页url,针对中国统计信息网"""
#
# 	pattern = re.compile(r'\d{2,5}_{1}\d{1,3}.html')
# 	try:
# 		result = re.findall(pattern, main_page)
# 	except TypeError, e:
# 		logger.error('url->%, error:%s'%(base_url, str(e)))
# 	url_fenye_list = [(base_url+url) for url in list(set(result))]
# 	return url_fenye_list


def get_page_data_list(html_src, url):
	item_list = []
	regex_result = None
	judge_time = 0
	regex_result = re.findall(pattern_date_tail, html_src)
	if regex_result:
		for result in regex_result:
			item = dict()
			try:
				item['url'] = urlparse.urljoin(url, result[0]).strip()
			except UnicodeDecodeError,e:
				item['url'] = ''
				logger.error(str(e))
			# print 'url :%s' % item['url']
			item['title'] = result[1].strip()
			item['publish_time'] = result[3]
			try:
				print item['title']
			except Exception:
				pass
			item_list.append(item)
	else:
		regex_result = re.findall(pattern_date_head, html_src)
		if regex_result:
			for result in regex_result:
				item = dict()
				try:
					item['url'] = urlparse.urljoin(url, result[7]).strip()
				except UnicodeDecodeError,e:
					item['url'] = ''
					logger.error(str(e))
				print 'url :%s' % item['url']
				item['title'] = result[-1].strip()
				item['publish_time'] = result[0]
				try:
					print item['title']
				except Exception:
					pass
				item_list.append(item)
		else:
			logger.error('page parse fail url:%s'%url)
	return item_list




def get_all_entrances(dir):
	"""获得搜集的区县统计信息的网页url等信息列表"""

	entrance_list = []
	entrance_f = open(dir, 'r')
	lines = entrance_f.readlines()
	for line in lines:
		line = json.loads(line.decode(encoding='utf-8'))
		item = dict()
		item['url'] = line['des_url']
		item['gov_name'] = line['gov_name']
		item['gov_id'] = line['gov_id']
		entrance_list.append(item)
	return entrance_list


def get_province_entrances_zgtj(zgtj_base_url):
	p_items = []
	"""获得所有省的入口url"""
	page_content = detect_url(zgtj_base_url)
	soup = BeautifulSoup(page_content)
	provice_set = soup.find('div', class_='sonnav')
	provice_unit = provice_set.find_all('span')
	for p_unit in provice_unit:
		item = dict()
		item['url'] = urlparse.urljoin(zgtj_base_url, p_unit.a['href'])
		item['province_name'] = p_unit.a.get_text()
		p_items.append(item)
	return p_items