#coding:utf-8

import requests, time, chardet
from config import header_info, phantomjs_dir
from config import logger
from selenium import webdriver

def detect_url(url, detect_flag):
	"""探测url能否访问, 并返回页面html源码"""

	page_html = None
	if detect_flag == 'normal':
		res = None
		try:
			res = requests.get(url, timeout=60, headers=header_info)
			if res.status_code == 200:
				logger.debug('url:%s -------detect success' % url)
				page_html =  res.content
		except requests.ConnectionError, e:
			logger.error('ConnectionError: detect fail url------%s' % (url))
		except requests.HTTPError as f:
			logger.error('HTTPError: request fail url------%s' % (url))
		except requests.exceptions.Timeout, e:
			logger.error('requests.exceptions.Timeout: detect fail url------%s' % (url))

		except Exception,e:
			# print ('unknow error')
			logger.error('unknow error %s: request fail url:%s'% (str(e), url))
	elif detect_flag == "web_detect":
		driver = webdriver.PhantomJS(executable_path=phantomjs_dir)
		driver.get(url)
		time.sleep(5)
		html_src = driver.page_source
		# print html_src
		# print 'type:%s' % type(html_src)
		driver.close()
		html = html_src.encode('utf-8')          # 动态加载完是unicode编码，转化为utf-8
		page_html = html
	if page_html:
		html_srccode = chardet.detect(page_html)['encoding']
		# page_html = html_encode(page_html)
		page_html = page_html.decode(encoding=html_srccode, errors='replace')
		page_html = page_html.replace('\n', '').replace(' ','')  # 去换行和空格
		# print page_html
	return page_html
def structtime_to_timestamp(time_sourse):
	try:
		time_stamp_soure = time.mktime(time.strptime(time_sourse, '%Y-%m-%d %H:%M:%S'))
	except ValueError:
		time_stamp_soure = time.mktime(time.strptime(time_sourse, '%Y-%m-%d'))
	return str(int(time_stamp_soure))


def html_encode(html_1):
	encoding_dict = chardet.detect(html_1)
	web_encoding = encoding_dict['encoding']
	# print web_encoding
	if web_encoding == 'utf-8' or web_encoding == 'UTF-8':
		html = html_1
	elif web_encoding == 'GB2312':
		html = html_1.decode('GB2312', 'ignore').encode('utf-8')
	elif web_encoding == 'UTF-8-SIG':
		html = html_1.decode('UTF-8-SIG', 'ignore').encode('utf-8')
	elif web_encoding == 'ISO-8859-2':
		html = html_1.decode('ISO-8859-2', 'ignore').encode('utf-8')
	elif web_encoding == 'ascii':
		html = html_1.decode('ascii', 'ignore').encode('utf-8')
	else:
		html = html_1.decode('gbk', 'ignore').encode('utf-8')
	return html


def read_info(info_dir):
	"""从info中读取每个省的数据形成item列表"""

	items_list = []
	info_f = open(info_dir, 'r')
	lines = info_f.readlines()
	for line in lines:
		item = dict()
		line_list = line.split('\t')
		item['url'] = line_list[1].strip()
		item['title'] = line_list[0].strip()
		item['publish_time'] = line_list[2].strip()
		items_list.append(item)

	return items_list


