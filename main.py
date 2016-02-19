import os
import database
from crawler import RoadSpeed_crawler

def main():
    import config
    path = config.datafile_path
    
    if path.endswith('json'):
        db = database.Json_db(path)
    elif path.endswith('csv'):
        db = database.Csv_db(path)
    elif path.endswith('sq3'):
        db = database.Sqlite_db(path)
    else:
        raise ValueError('cannot handle {} file'.format(path))

    crawler = RoadSpeed_crawler(db)
    crawler.run()

if __name__ == '__main__':
    main()