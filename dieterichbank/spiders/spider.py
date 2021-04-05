import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import DdieterichbankItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class DdieterichbankSpider(scrapy.Spider):
	name = 'dieterichbank'
	start_urls = ['https://www.dieterichbank.com/dieterich-bank/media-center']

	def parse(self, response):
		post_links = response.xpath('//h5/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = 'Not stated in article'
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//div[@data-content-block="bodyCopy"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=DdieterichbankItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
