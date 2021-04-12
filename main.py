from scrapy.cmdline import execute
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(['scrapy','crawl','MM'])


# 这个过程是先爬取完成然后隔了五秒之后重新运行，如此循环
# import time
# import os
# while True:
#     os.system("scrapy crawl f")
#     time.sleep(86400)


