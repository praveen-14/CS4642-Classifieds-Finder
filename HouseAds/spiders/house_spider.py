import scrapy
import pprint
import re
import csv
# from unidecode import unidecode



class HouseAdSpider(scrapy.Spider):
    name = "house_ad_crawler"

    start_urls = [
        'http://www.hitad.lk/EN/houses?page=0'
    ]

    # def start_requests(self):
    #     urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.log('crawling to - ' + response.url)
        startDigit = response.url.index("=")
        page = response.url[startDigit+1:]
        filename = 'house-ad-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        ads = response.xpath('//div[@class="detail-sum fw_b"]')
        descriptions = []
        locations = []
        types = []
        categories = []
        sub_categories = []
        dates = []
        refNumbers = []
        prices = []

        for p in ads:
            description = p.css('div a h4::text').extract_first()
            if(description):
                # description = unidecode(description)
                descriptions.append(re.sub(r"\s+", " ", description).rstrip().lstrip())
            else:
                descriptions.append("")

            date = p.css('div div.ad-info-2::text').extract_first()
            if (date):
                dates.append(re.sub(r"\s+", " ", date).rstrip().lstrip())
            else:
                dates.append("")

            price = p.css('div')[-1].css('div span::text').extract_first()
            if (price):
                # price = price.replace(",","")
                prices.append(re.sub(r"\s+", " ", price).rstrip().lstrip())
            else:
                prices.append("")

            refNumber = p.css('div')[0].css('div span::text').extract_first()
            if (refNumber):
                refNumbers.append(re.sub(r"\s+", " ", refNumber).rstrip().lstrip())
            else:
                refNumbers.append("")

            location = p.css('div.col-lg-12 div.item-facets2::text').extract_first()
            if (location):
                location = location.lstrip().rstrip()
            else:
                location = ""
            location1 = p.css('div.col-lg-12 div.item-facets2 font::text').extract_first()
            if(location1):
                location1 = location1.lstrip()[1:].lstrip().rstrip()
                location = location + "-" + location1
            locations.append(location)

            category = p.css('div.col-lg-12').xpath('div[@class="item-facets hidden-xs"]/text()').extract()
            if category[0]:
                types.append(category[0])
            else:
                types.append("")
            if category[1]:
                categories.append(category[1])
            else:
                categories.append("")
            if category[2]:
                sub_categories.append(category[2])
            else:
                sub_categories.append("")

        print(len(ads))
        print(len(descriptions))
        print(len(locations))
        print(len(types))
        print(len(dates))
        print(len(categories))
        print(len(sub_categories))
        print(len(prices))
        print(len(refNumbers))

        print(descriptions)
        print(locations)
        print(types)
        print(categories)
        print(sub_categories)
        print(dates)
        print(prices)
        print(refNumbers)

        with open('data.csv', 'a', encoding="utf-8", newline='') as file:
            CSVWriter = csv.writer(file)
            for i in range(len(ads)):
                data =  [refNumbers[i],
                        descriptions[i],
                        dates[i],
                        types[i],
                        categories[i],
                        sub_categories[i],
                        locations[i],
                        prices[i]]
                print(data)
                CSVWriter.writerow(data)
        hrefs = response.css('a.number::attr(href)').extract()
        pageNumbers = [x[startDigit+1:] for x in hrefs ]
        #
        # descriptions = response.css("h4.fw_b::text").extract()
        #
        # for i in range(len(descriptions)):
        #     descriptions[i] = re.sub(r"\s+", " ", descriptions[i]).rstrip().lstrip()
        # # print(descriptions)
        # print(len(descriptions))
        #
        # date = response.css("div.ad-info-2::text").extract()
        # # print(date)
        # print(len(date))
        # referenceNumbers = response.xpath('//div[@class="col-md-3 col-sm-3 ad-info-2 hidden-xs"]/span/text()').extract()
        # print(referenceNumbers)
        # print (len(referenceNumbers))
        # map(str.rstrip, descriptions)
        # print(descriptions)

        for pageNumber in pageNumbers:
            if int(pageNumber) > int(page):
                nextPage = hrefs[pageNumbers.index(pageNumber)]
                yield response.follow(nextPage, callback=self.parse)


