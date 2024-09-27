import scrapy

class CarbonSpider(scrapy.Spider):
    name = "carbon"
    start_urls = ['https://www.carbon38.com/shop-all-activewear/tops']

    def parse(self, response):
        product_links = response.xpath("//div[contains(@class, 'ProductListWrapper')]//a/@href").getall()
        product_dict = {}

        # Iterate through the list and store valid links in the dictionary
        for index, link in enumerate(product_links):
            if link and link != '#':  # Ensure the link is not empty or a placeholder
                product_dict[f'link_{index}'] = link

        # Print or return the resulting dictionary
        self.log(product_dict)  # You can log it or yield it as needed
        yield product_dict  # This will yield the dictionary as a result

        # product_links = response.xpath("//div[contains(@class, 'ProductList ProductList--grid ProductList--removeMargin Grid ')]//a/@href").get() 
        
        for link in product_links: 
            yield response.follow(link, self.parse_product) 
            
            next_page = response.xpath("//a[contains(@class, 'Pagination__NavItem Link Link--primary')]/@href").get() 
            if next_page: 
                yield response.follow(next_page, self.parse)  


    def parse_product(self, response):
            yield
            {
                'brand' : response.xpath("//h3[@class='ProductItem__Designer']/text()").get(),
                'product_name' : response.xpath("//h2[@class='ProductItem__Title Heading']/a/text()").get(),
                'product_id' :response.xpath("//status-save-button/@product-id").get(),
                'primary_image_url' : response.xpath("//img[@class='ProductItem__Image']/@src").get(),
                'price' : response.xpath("//span[@class='ProductItem__Price Price']/text()").get(),
                'image_urls' : response.xpath("//img[contains(@class, 'ProductItem__Image ProductItem__Image--alternate')]/@src").getall(),
            }




