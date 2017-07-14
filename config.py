#coding:utf-8
import logdealer
import time
ZGTJXX_BASE_URL = 'http://www.tjcn.org/tjgb/'
TJGB_BASE_DIR = 'D:\\china_tjgb_common\\'         # 需要在其他机器同时跑时只需要把E改成.
crawler_log_name = './log/'+'tjgb_crawer_'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()).replace(':','')+'.log'
logger = logdealer.Logger(crawler_log_name).getLogger()
entrance_file_dir = '.\\all_success_site-2017-06-27-200433.log'
phantomjs_dir = 'D:\\phantomjs.exe'
fire_fox_dir = 'D:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe'
header_info = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1581.2 Safari/537.36',
    'Connection':'keep-alive',
    'Content-Type':'application/x-www-form-urlencoded',
    }
