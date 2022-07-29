import scrapy


class FundaSpider(scrapy.Spider):
    """Get data of available houses on the market"""
    name = "funda"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__property_map = {'huis': 'house', 'appartement': 'apartment'}
        self.start_urls = [
            'https://www.funda.nl/en/koop/heel-nederland/beschikbaar/appartement/',
            'https://www.funda.nl/en/koop/heel-nederland/beschikbaar/huis/',
        ]

    def parse(self, response, **kwargs):
        for content in response.css('div.search-result-content'):
            property_url = content.css('a::attr(href)')[0].getall()[0]
            yield response.follow(property_url, callback=self.parse_house)

        next_page = response.css('a[rel="next"]::attr(href)').get()
        if next_page is not None:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_house(self, response):
        yield {'url': response.url,
               'property_type': self.extract_property_type(response.url),
               'town': self.extract_town(response),
               'address': self.extract_address(response),
               'postcode': self.extract_postcode(response),
               'price': self.extract_price(response),
               'building_type': self.extract_building_type(response),
               'living_area': self.extract_living_area(response),
               'year_of_construction': self.extract_year_of_construction(response),
               }

    def extract_property_type(self, url):
        property_type = url.split('/')[-2].split('-')[0]

        if property_type in self.__property_map:
            return self.__property_map[property_type]

        return None

    @staticmethod
    def extract_town(response):
        return ' '.join(response.css('span[class="object-header__subtitle fd-color-dark-3"]::text')
                        .get().strip().split(' ')[2:])

    @staticmethod
    def extract_address(response):
        return response.css('span[class="object-header__title"]::text').get()

    @staticmethod
    def extract_postcode(response):
        return ' '.join(response.css('span[class="object-header__subtitle fd-color-dark-3"]::text')
                        .get().strip().split(' ')[0:2])

    @staticmethod
    def extract_price(response):
        return response.xpath("//dt[contains(.,'Asking price')]/following-sibling::dd[1]/span[1]/text()") \
            .get().split(' ')[1]

    @staticmethod
    def extract_building_type(response):
        return response.xpath("//dt[contains(.,'Building type')]/following-sibling::dd[1]/span[1]/text()") \
            .get()

    @staticmethod
    def extract_living_area(response):
        return response.xpath("//dt[contains(.,'Living area')]/following-sibling::dd[1]/span[1]/text()") \
            .get().split(' ')[0]

    @staticmethod
    def extract_year_of_construction(response):
        return response.xpath("//dt[contains(.,'Year of construction')]/following-sibling::dd[1]/span[1]/text()") \
            .get()
