import pymongo
import time

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log


class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        for data in item:
            if not data:
                raise DropItem("Missing data!")
        if spider.name in ['fotoCasa']:
            file_log = open("log_fotoCasa.txt", "a")
            file_log.write("\n\n****************************" + time.strftime("%c") + "*******************************\n\n")
            if not self.collection.find({'detailReference': item['detailReference']}).count() > 0:
                file_log.write("Referencia [" + item['detailReference'] + "] NO encontrada\n")
                file_log.write("URL:  [" + item['url'] + "]\n")
                file_log.write("TITULO:  [" + item['title'] + "]\n")
                
                file = open("fotoCasa.txt", "a")
                file.write("<br><a class='texto'>"+ item['company'] +" </a>"+ "\n")
                if  item['price']:
                    file.write("<br><a class='texto'>"+ item['price'] + " Euros</a>" + "\n")
                if  item['surface']:  
                    file.write("<a class='texto'> -- "+ item['surface'] + "m</a>" + "\n")
                if  item['rooms']:
                    file.write("<a class='texto'> -- "+ item['rooms'] + " habitaciones </a>" + "\n")
                if  item['title']:
                    file.write("<br><a class='texto' href=" + item['url'] + ">"+ item['title'] +"</a>"+ "\n")
                else:
                    file.write("<br><a class='texto' href=" + item['url'] + ">---> al anuncio <---</a><br>"+ "\n")
                file.close()
                log.msg("Piso anyadido a la base de datos MongoDB", level=log.DEBUG, spider=spider)
            else:
                file_log.write("Referencia [" + item['detailReference'] + "] encontrada\n")
                file_log.write("URL:  [" + item['url'] + "]\n")
                file_log.write("TITULO:  [" + item['title'] + "]\n")
                
                log.msg("La referencia [" + item['detailReference'] + "] ya existe en base de datos.", level=log.DEBUG, spider=spider)
                
                
            file_log.write("\n\n***********************************************************\n\n")
            file_log.close()
        else:
            if not self.collection.find({'url': item['url']}).count() > 0:
                file = open("newfile.txt", "a")
                file.write("<br><a class='texto'>"+ item['company'] +" </a>"+ "\n")
                if  item['price']:
                    file.write("<br><a class='texto'>"+ item['price'] + " Euros</a>" + "\n")
                if  item['surface']:  
                    file.write("<a class='texto'> -- "+ item['surface'] + "m</a>" + "\n")
                if  item['rooms']:
                    file.write("<a class='texto'> -- "+ item['rooms'] + " habitaciones </a>" + "\n")
                if  item['title']:
                    file.write("<br><a class='texto' href=" + item['url'] + ">"+ item['title'] +"</a>"+ "\n")
                else:
                    file.write("<br><a class='texto' href=" + item['url'] + ">---> al anuncio <---</a><br>"+ "\n")
                #file.write(item['url'] + "\n")
                file.close()
                log.msg("Piso anyadido a la base de datos MongoDB", level=log.DEBUG, spider=spider)
        self.collection.update({'url': item['url']}, dict(item), upsert=True)
        #log.msg("Flat added to MongoDB database!", level=log.DEBUG, spider=spider)
        
        return item
