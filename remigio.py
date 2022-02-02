# -*- coding: utf-8 -*-

import scrapy

class remigioSpider(scrapy.Spider):
    name = 'diario_remigio'

    start_urls = ['https://www.remigio.pb.gov.br/portal/publicacoes/diario-oficial']

    def parse(self, response):
        diarios = response.xpath(
            '//*[@id="pubs"]/li/a[re:test(@href, "diario-oficial")]/@href').getall()
        pages_url = response.css(".page-link::attr(href)").getall()[-1]
        
        for diario in diarios:
            yield scrapy.Request(
                response.urljoin(diario),
                callback=self.parse_category,
            )
        
        yield scrapy.Request(
            response.urljoin(pages_url),
            callback=self.parse,
        )


    def parse_category(self, response):
        title = response.css(".col-md-8 .font-or::text").get()
        date = response.css(".text-danger::text").get()
        pdf_diario = response.css("#conteudo div > ul > li > a::attr(href)").get()

        yield {
            'titulo':title,
            'data':date,
            'diario_pdf':pdf_diario
        }


#############PARA RODAR O SPIDER/SCRAPY######################
#############EXECUTE O CODIGO ABAIXO NO TERMINAL#############
############# scrapy runspider remigio.py -s HTTPCACHE_ENABLED=1 -o diariosrmg.csv #####################