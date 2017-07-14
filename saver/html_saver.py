#coding:utf-8
#created:2017/06/22
#__author__:jiaqiying
#discript:build dir and write info
import Queue
import threading
from gevent.queue import Queue as Gqueue
from gevent.queue import Empty
from gevent import monkey
from gevent.pool import Pool
# monkey.patch_all()

import requests
from config import TJGB_BASE_DIR
import chardet
import time
from tools.tool import translate_non_special_char
from utils import structtime_to_timestamp
from utils import html_encode
from utils import detect_url
from config import logger
from config import logger
import logdealer
import os



# logger = logdealer.Logger('crawl_tjgb.log').getLogger()

def save_html():
	pass


def write_info(items, province):
	"""将公报title，url，time等信息写入info"""
	try:
		part_path = province['gov_name'].replace('|','\\')
		path = TJGB_BASE_DIR + part_path
		is_exists = os.path.exists(path)
		if not is_exists:
			os.makedirs(path)
		else:
			logger.debug('the %s dir is existing' % (province['gov_name']))
	except WindowsError:
		logger.error('the %s dir is existing' % (province['gov_name']))

	file_path = os.path.join(path, 'info.txt')
	print 'path:%s'%path
	info_f = open(file_path, 'w')
	print 'infodir: %s' % (info_f.name)
	for item in items:
		try:
			info_f.write((item['title'] +'\t'+item['url']+'\t'+item['publish_time']+'\n').encode('utf-8',errors='replace'))
		except Exception,e:
			logger.error(str(e))
	info_f.close()


lock = threading.Lock()
def save_html_old(items, gov):
    path = os.path.join(os.path.join(TJGB_BASE_DIR, gov['gov_name'].replace('|','\\')), 'tjgb_files')
    is_exist = os.path.exists(path)
    if not is_exist:
        os.makedirs(path)
    else:
        pass
	if items:
		logger.debug('success crawl data gov_name:%s, gov_url:%s' % (gov['gov_name'], gov['url']))  # 用来记录成功爬取的区县
	for item in items:
            page_content = detect_url(item['url'],'normal')
            if page_content:
                try:
                    item['publish_time'] = item['publish_time'].replace(':','').replace('.','')
                    try:
                        file_name = translate_non_special_char(item['title'] + '_' + item['publish_time'] + '.txt')
                        print "file_name:%s"%file_name
                        tjgb_file_path = os.path.join(path, file_name)
                    except IOError:
                        tjgb_file_path = os.path.join(path,'_'+item['publish_time']+'.txt')
                    html_f = open(tjgb_file_path, 'w')
                    html_f.write(page_content.encode('utf-8',errors='replace'))
                    html_f.close()
                    # logger.debug('success write file gov_name:%s, item_url:%s'%(gov['gov_name'], item['url'])
                except UnicodeEncodeError,e:
                    print 'UnicodeEncodeError:%s' % (item['url'])


def save_html(item, path):
    page_content = detect_url(item['url'],'normal')
    if page_content:
        try:
            # item['publish_time'] = item['publish_time'].replace(':','').replace('.','')
            try:
                file_name = translate_non_special_char(item['title'] + '_' + item['publish_time'] + '.txt')
                print "file_name:%s"%file_name
                tjgb_file_path = os.path.join(path, file_name)
            except IOError:
                tjgb_file_path = os.path.join(path,'_'+item['publish_time']+'.txt')
            html_f = open(tjgb_file_path, 'w')
            html_f.write(page_content.encode('utf-8',errors='replace'))
            html_f.close()
            # logger.debug('success write file gov_name:%s, item_url:%s'%(gov['gov_name'], item['url'])
        except UnicodeEncodeError,e:
            print 'UnicodeEncodeError:%s' % (item['url'])


def save_html_for_queue(queue, gov_name):
    
    path = os.path.join(os.path.join(TJGB_BASE_DIR, gov_name.replace('|','\\')), 'tjgb_files')
    is_exist = os.path.exists(path)
    if not is_exist:
        os.makedirs(path)
    else:
        pass
    while True:
        item = queue.get()
        save_html(item, path)
        queue.task_done()


def save_html_with_queue(items, gov):
    item_queue = Queue.Queue()
    for i in range(10):
        t = threading.Thread(target=save_html_for_queue, args=(item_queue,gov['gov_name']))
        t.setDaemon(True)
        t.start()
    
    for item in items:
        item_queue.put(item)

    item_queue.join()


def save_html_for_gevent(queue, gov_name):

    path = os.path.join(os.path.join(TJGB_BASE_DIR, gov_name.replace('|','\\')), 'tjgb_files')
    is_exist = os.path.exists(path)
    if not is_exist:
        os.makedirs(path)
    else:
        pass
    while True:
        try:
            item = queue.get(timeout=0)
        except Empty:
            break
        save_html(item, path)


def save_html_with_gevent(items, gov):
    pool = Pool(10)
    queue = Gqueue()

    for item in items:

        queue.put(item)

    while pool.free_count():
        pool.spawn(save_html_for_gevent, queue, gov['gov_name'])

    pool.join()