import os, sys
from scrapy.cmdline import execute

base_dir = os.path.abspath(os.path.dirname(__file__))
print(base_dir)
sys.path.insert(0, base_dir)

# execute("scrapy crawlmany shunqi qianchengwuyou".split())
# execute("scrapy crawlmany  qianchengwuyou shunqi --nolog".split())
execute("scrapy crawl music".split())