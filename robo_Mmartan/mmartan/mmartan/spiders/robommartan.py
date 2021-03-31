# -*- coding: utf-8 -*-
import scrapy
import json


class RobommartanSpider(scrapy.Spider):
    name = 'robommartan'
    start_urls = ['http://mmartan.com.br/lojas/']

    def parse(self, response):
        data = json.loads(response.css('#__NEXT_DATA__::text').get())
        stores = (data['props']['initialMobxState']['distributorStore']
                  ['distributors'])        
        for store in stores:
            CNPJ = response.css('div.x21smb-0.eaLBM > p > span::text')
            store_name = store.get('name')
            store_address = store.get('address')
            postal_code = store_address.get('postalCode')
            address = store_address.get('address')
            neigh = store_address.get('district')
            city = store_address.get('city')
            state = store_address.get('state')

            store_phone = store.get('phone')
            email = store.get('email')

            position = store.get('position')

            lat = position.get('lat')
            lng = position.get('lng')

            

            yield {
                'Rede': 'Mmartan',
                'Nome Fantasia': store_name,
                'Logradouro': address,
                'Bairro': neigh,
                'Cep': postal_code,
                'Ddd': '',
                'Telefone': store_phone,
                'Uf': state,
                'Municipio': city,
                'DtAbertutra': '',
                'codUnidade': '',
                'Cnpj': CNPJ,
                'Categoria': 'Artigos Diversos',
                'Classsificação': '',
                'Fontes': '',
                'Cnes': '',
                'Latitude': lat,
                'Longitude': lng,
                'Email': email
            }

