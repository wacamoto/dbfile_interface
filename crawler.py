import requests
from bs4 import BeautifulSoup
from database import database

class roadSpeed_crawler:
    def __init__(self, config):
        self.config = config

    def run(self):
        db = database(self.config)
        db.fields(db.string('southbound'),
            db.int('Northbound'),db.int('road'))

        req = requests.get('http://1968.freeway.gov.tw/traffic/index/fid/10010')
        soup = BeautifulSoup(req.text, 'html.parser')
        tb = soup.find(id='secs_body')
        
        for tr in tb.find_all('tr'):
            tds = tr.find_all('td')
            # insert value
            db.insert(road=tds[1].text, Northbound=tds[2].text,
                southbound=tds[0].text)
        
        db.close()

if __name__ == '__main__':
    import config
    c = roadSpeed_crawler(config)
    c.run()