import sys
from scrapy.utils.project import get_project_settings
from universalspider.spiders.templateEin import TemplateeinSpider
from universalspider.utils import get_config
from scrapy.crawler import CrawlerProcess

def run(_name):
    
    custom_settings = get_config(_name)

    spider = custom_settings.get('spider','templateEin')
    project_settings = get_project_settings()
    settings = dict(project_settings.copy())

    settings.update(custom_settings.get('settings'))#覆盖and添加，UA，限速，middlewares
    process = CrawlerProcess(settings)

    process.crawl(spider, **{'_name':_name})
    process.start()

if __name__ == '__main__':
    name = sys.argv[1]
    run(name)