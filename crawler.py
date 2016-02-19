import requests
from bs4 import BeautifulSoup

class roadSpeed_crawler:
    def __init__(self, db):
        self.db = db

    def run(self):
        db = self.db
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