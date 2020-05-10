from category.items import CategoryItem
from scrapy import Spider, Request

class CategorySpider(Spider):
    name = 'category_spider'
    allowed_urls = ["https://www.simplyrecipes.com/"]
    start_urls = ["https://www.simplyrecipes.com/"]

    def parse(self, response):
        main_ing = ['chicken', 'beef', 'seafood', 'lamb', 'pork', 'pasta']
        diet_ing = ['vegetarian']
        main_path = list(map(lambda x:  'main-ingredient/' + x, main_ing))
        diet_path = list(map(lambda x: 'diet/' + x, diet_ing))
        path_category = main_path + diet_path

        for item in path_category:
            category_url = f'https://www.simplyrecipes.com/recipes/{item}/dinner/'
            meta = {'category': item}
            yield Request(url=category_url, callback=self.parse_page_num, meta = meta)

    def parse_page_num(self, response):
        num_pages = int(response.xpath('//a[@class="rpg-page-numbers"]/text()').extract()[-1])
        #page_lst = response.request.url + f'page/{i+1}/' for i in range(num_pages)
        page_lst = list(map(lambda i: response.request.url + f'page/{i+1}/', range(num_pages)))

        for page in page_lst:
            yield Request(url = page, callback = self.parse_links, meta = response.meta)

    def parse_links(self, response):
        links = response.xpath('//a[@itemprop = "url"]/@href').extract()

        for link in links:
            yield Request(url = link, callback = self.parse_dish, meta = response.meta)

    def parse_dish(self, response):
        author = response.xpath('//span[@class="author"]//span/text()').extract_first()
        dish = response.xpath('//h1[@class="entry-title"]/text()').extract_first()

        item = CategoryItem()
        item['author'] = author
        item['dish'] = dish
        item['category'] = response.meta['category']

        yield item


        
