import scrapy 

# Título= //h1/a/text()
# Citas = //span[@class="text" and @itemprop="text"]/text()
# Top ten tags= response.xpath('//div[contains(@class,"tags-box")]//span[@class="tag-item"]/a/text()').getall()
# next_page_button = response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()

class QuotesSpider(scrapy.Spider):
    name='quotes'
    start_urls=[
        'https://quotes.toscrape.com/'
    ]
    custom_settings = {
        'FEEDS': {
            'quotes.json': {
                'format': 'json',
                'encoding': 'utf8',
                'store_empty': False,
                'fields': None,
                'indent': 4,
                'item_export_kwargs': {
                    'export_empty_fields': True,
                },
            },
        },
    } #Acá podriamos agregar para que guarde en un CSV, agregarle un CONCURRENT_REQUESTS, un MEMUSAGE_LIMIT_MB, UN MEMUSAGE_NOTIFY_MAIL (insertar mail), DECIRLE SI VA A OBEDECR AL ROBOTS.TXT o NO. SE PUEDE AGREGAR TAMBIEN EL USER AGENT, tambien se puede agregar el FEED_EXPORT_ENCODING a utf-8

    def parse_only_quotes(self,response,**kwargs):
        if kwargs:
            quotes=kwargs['quotes']
        quotes.extend(response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall())

        next_page_button_link=response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        if next_page_button_link:
            yield response.follow(next_page_button_link,callback=self.parse_only_quotes,cb_kwargs={'quotes':quotes})
        else:
            yield{
                'quotes':quotes
            }

    def parse(self,response): #Analiza la respuesta HTTP de la url y extrae informacion valiosa
        title=response.xpath('//h1/a/text()').get()
        quotes=response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()
        top_tags=response.xpath('//div[contains(@class,"tags-box")]//span[@class="tag-item"]/a/text()').getall()

        top = getattr(self,'top',None)

        if top:
            top=int(top)
            top_tags = top_tags[:top]
        
        #yield hace un return parcial de datos

        yield { 
            'title':title,
            'top_tags':top_tags,
        } 

        next_page_button_link=response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        if next_page_button_link:
            yield response.follow(next_page_button_link,callback=self.parse_only_quotes,cb_kwargs={'quotes':quotes})#Un callback es una funcion que se va a ejecutar luego de hacer la request al link

    