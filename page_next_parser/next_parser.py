#coding:utf-8
import re
import urlparse
import chardet

from config import logger, fire_fox_dir
from regex_collection import NEXTPAGE_TAG_REGEX, A_TAG_NUM_REGEX, A_TAG_NUM_REGEX_DYNAMIC
from utils import detect_url, html_encode
from selenium import webdriver
from config import phantomjs_dir
import time
PATTERN_A_NUM = re.compile(A_TAG_NUM_REGEX)
PATTERN_NEXT_PAGE = re.compile(NEXTPAGE_TAG_REGEX.decode('utf-8'))


def parse_page_next_tag(regex_result, url):
	"""有分页标识时解析页面根据当前页获得下一页片段url"""

	if regex_result:
		logger.debug('success get next_url regex_result:%s' % url)
		next_url_part = regex_result.group('next_url')
		# next_url = urlparse.urljoin(url, next_url_part)
		next_url = next_url_part
	else:
		logger.error('get next_url regex_result none: %s' % url)
	return next_url



def get_next_url_next_tag(url, detect_flag):
	"""获取下页url的逻辑控制函数，调度各个获取方法来,暂时只用parse_fanye_first"""

	page_src = detect_url(url, detect_flag)
	next_url = None

	if page_src:
		# html_src = html_encode(page_src)
		regex_result = re.search(PATTERN_NEXT_PAGE, page_src)
		if regex_result:
			next_url = parse_page_next_tag(regex_result, url)
	return next_url


def get_next_url_num(current_url_dict, detect_flag):
	"""没有下页标识根据text是数字的a标签获取下页"""

	page_src = detect_url(current_url_dict['url'], detect_flag)
	# 此处预留动态加载处理
	next_url = {'url':None,'id':None}

	if page_src:
		# html_src = html_encode(page_src)                          # 切记先判断html获得后再编码
		new_id = current_url_dict['id'] + 1                       # 将id加1
		regex_repression = A_TAG_NUM_REGEX_DYNAMIC%str(new_id)
		pattern = re.compile(regex_repression)          # 匹配tex是id加一的a标签
		regex_result = re.search(pattern, page_src)
		if regex_result:
			next_url['url'] = regex_result.group('page_url')
			next_url['id'] = int(regex_result.group('page_id'))
	return next_url

def get_nexturl_list_has_nexttag(url, detect_flag):
	"""根据一个url获取所有的分页list包括首页"""
	print "main page: %s"%url
	logger.debug('main page start:%s' % url)
	next_url_list = []
	crawled_url_list = []
	current_url = url

	while True:
		next_url_list.append(current_url)
		part_next_url = get_next_url_next_tag(current_url, detect_flag)   # 根据当前页获得下页的片段url
		# print "part_next_url:%s"%part_next_url
		crawled_url_list.append(current_url)
		try:
			current_url = urlparse.urljoin(current_url, part_next_url)
			logger.debug('child page:%s' % current_url)
			print "child page: %s" % current_url
		except UnicodeDecodeError, e:
			logger.error(str(e))
		# print 'current_url:%s' % current_url
		if current_url in crawled_url_list:
			break

	if len(next_url_list) >= 2:
		logger.debug('success get next_url_list : %s'%url)
	else:
		logger.error('fail next_url_list tag_next : flag:%s, %s'% (detect_flag, url))
	return next_url_list


def get_nexturl_list_has_numpage(url, detect_flag):
	"""解决只有数字翻页问题"""

	print "main page: %s" % url
	logger.debug('main page start:%s' % url)
	next_url_list = []
	crawled_url_list = []

	current_url = {'url':url, 'id':1}
	while True:
		next_url_list.append(current_url['url'])
		part_next_url = get_next_url_num(current_url, detect_flag)         # 根据当前页获得下页的片段url
		crawled_url_list.append(current_url['url'])
		try:
			current_url['url'] = urlparse.urljoin(current_url['url'], part_next_url['url'])
			current_url['id'] = part_next_url['id']
			logger.debug('child page:%s' % current_url['url'])
			print "child page: %s" % current_url['url']
		except UnicodeDecodeError, e:
			logger.error(str(e))
		# print 'current_url:%s' % current_url
		if current_url['url'] in crawled_url_list:
			break

	if len(next_url_list) >= 2:
		logger.debug('success get next_url_list : %s'% url)
	else:
		logger.error('fail next_url_list tag_num : flag:%s, %s'% (detect_flag, url))
	return next_url_list


def webdriver_get_next_url_list(url, detect_flag):
	"""动态加载后再获取分页list"""

	page_url_list = []
	driver = webdriver.PhantomJS(executable_path=phantomjs_dir)
	driver.get(url)
	time.sleep(5)
	html_src = driver.page_source
	# print html_src
	# print 'type:%s' % type(html_src)
	driver.close()
	if html_src:
		html = html_src.encode('utf-8')
		result_regex = re.search(PATTERN_NEXT_PAGE, html)
		if result_regex:
			page_url_list = get_nexturl_list_has_nexttag(url, detect_flag)  # 有下页标识
			# print url
			# print page_url_list
		else:
			page_url_list = get_nexturl_list_has_numpage(url, detect_flag)  # 无下页标识
			# print url
			# print page_url_list
	return page_url_list

def get_next_url_list(url):
	"""获取分页urllist调度主逻辑函数"""
	page_url_list = []
	html = detect_url(url, 'normal')
	print(type(html))
	if html:
		# html = html_encode(html)
		result_regex = re.search(PATTERN_NEXT_PAGE, html)
		if result_regex:
			print "success xia yi ye"
			page_url_list = get_nexturl_list_has_nexttag(url, 'normal')   # 有下页标识
		else:
			print "success num pipei"
			page_url_list = get_nexturl_list_has_numpage(url, 'normal')   # 无下页标识
	if len(page_url_list) == 1:
		page_url_list = webdriver_get_next_url_list(url, detect_flag='web_detect')
	print url
	print page_url_list
	return page_url_list


def web_load_frame(url, frame_name):
    driver = webdriver.PhantomJS(executable_path=phantomjs_dir)
    driver.get(url)
    driver.switch_to.frame(frame_name)
    time.sleep(5)
    # print(driver.page_source)
    print driver.page_source
    driver.close()
    return driver.page_source


def web_load_normal(url):
    driver = webdriver.PhantomJS(executable_path=phantomjs_dir)
    driver.get(url)
    time.sleep(5)
    # driver.execute_script()
    page_source = driver.page_source.encode('utf-8')
    print page_source
    driver.close()