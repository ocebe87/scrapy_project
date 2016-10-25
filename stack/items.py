from scrapy.item import Item, Field


class StackItem(Item):
    title = Field()
    url = Field()
    price = Field()
    update_date = Field()
    features = Field()
    description = Field()
    rooms = Field()
    surface = Field()
    images = Field()
    location = Field()
    postal_code = Field()
