#coding:utf-8

import re

from utils import detect_url

httpstr = r"http:.*"
frame_regex =r"frame"
http_pattern = re.compile(httpstr)
frame_p = re.compile(frame_regex)
# print re.search(http_pattern,"Line 110: 2017-07-03 22:06:36,109 next_url_list_getter.py[line:21] ERROR fail get next_url_list http://www.scqs.gov.cn/xxgk/jbxxgk/tjxx.htm").group(0)
def test_frame(fail_dir):
	"""测失败的翻页中有frame的个数"""
	count = 0
	f = open(fail_dir, 'r')
	line_list = f.readlines()
	for line in line_list:
		url = re.search(http_pattern, line).group(0).strip()
		print url
		html = detect_url(url,"normal")
		result = re.search(frame_p,html)
		if result:
			count+=1
			print count
	print "sum count:%s"%count

def translate_non_special_char(to_tran, tran_to=None):
	"""针对unicode字符串"""
	special_char = u"/\<>|:\"*?\t"
	tran_table = dict((ord(char), tran_to) for char in special_char)
	return to_tran.translate(tran_table)