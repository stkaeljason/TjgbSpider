#coding:utf-8
#created:2017/06/21
#__author__:jiaqiying
#discript:get page content

import time
import multiprocessing
from Queue import Empty

from page_content_crawl.page_crawler import get_item_collection, get_item_collection_for_multi
from page_content_crawl.parser import get_all_entrances
from saver.html_saver import write_info, save_html_with_queue
from config import entrance_file_dir
from page_next_parser.next_parser import get_next_url_list


def get_all_items_gov(url):
	"""获取一个省的所有统计信息"""

	all_items = []
	# page_crawler = PageContentCrawer(url)
	gov_url_list = get_next_url_list(url)
	for url in gov_url_list:
		all_items.extend(get_item_collection(url))
	return all_items


def get_all_items_with_multiprocessing(url):
    queue = multiprocessing.JoinableQueue()
    num_consumers = multiprocessing.cpu_count()
    print 'num_consumers:%s' % num_consumers
    results_queue = multiprocessing.Queue()

    gov_url_list = get_next_url_list(url)
    for child_url in gov_url_list:
        queue.put(child_url)

    for i in range(num_consumers):
        p = multiprocessing.Process(target=get_item_collection_for_multi, args=(queue, results_queue))
        p.start()
    queue.join()

    items_list = []

    while True:
        try:
            item_list = results_queue.get(timeout=1)
        except Empty:
            break
        items_list.extend(item_list)

    return items_list





if __name__ == "__main__":
    stime = time.clock()
    all_entrance = get_all_entrances(entrance_file_dir)
    for gov in all_entrance[1:2]:
        print 'the %s get_urls is starting' % gov['gov_name']
        p_items = get_all_items_with_multiprocessing(gov['url'])
        print 'the %s items length is %s ' % (gov['gov_name'],len(p_items))
        print 'the %s write_info is starting' % gov['gov_name']
        write_info(p_items, gov)             # 如果已经有了就关闭不执行
        print 'the %s save_html is starting' % gov['gov_name']
        save_html_with_queue(p_items,gov)
        # save_html_with_gevent(p_items,gov)
        # time.sleep(2)
    endtime = time.clock()
    con = endtime - stime
    print "consum:%s"%str(con)
