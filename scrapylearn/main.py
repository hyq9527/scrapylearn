from scrapy.cmdline import execute

import sys
import os
import re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "JobboleSpider"])
# match_re = re.match(".*(\d+).*"," 4 收藏")
# print(match_re)