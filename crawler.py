from database import database

class Weather_crawler:
    def __init__(self, config):
        self.config = config
        self.db = database(config)

    def run(self):
        # for test
        db = self.db

        # set datafile fields
        db.fields(db.string('Loc'), db.int('Pop'), db.int('Temp'))

        # # insert value
        db.insert(Loc = 'Taipei', Pop = 10, Temp = 8)
        db.insert(Loc = 'Tainan', Pop = 0, Temp = 9)
        
        db.close()

if __name__ == '__main__':
    import config
    c = Weather_crawler(config)
    c.run()