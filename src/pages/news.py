import os
import json

class News():

    def __init__(self, caller):
        self.caller = caller

    def get_news(self, from_date, start, num):
        articles = self.caller.api.get('services/news/search',from_date = from_date, start = start, num = num, fields = 'items[article[author|publication_date|title|headline_html|content_html]]|next_page|total')
        json_string = json.dumps(articles)
        return json_string
        