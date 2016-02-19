import os
import database
from crawler import roadSpeed_crawler

def main():
    import config
    path = config.datafile_path
    f_extension = os.path.splitext(path)[1]
    
    if f_extension == '.json':
        db = database.Json_db(path)
    elif f_extension == '.csv':
        db = database.Csv_db(path)
    elif f_extension == '.db':
        db = database.Sqlite_db(path)
     
    # inject into crawler
    c = roadSpeed_crawler(db)
    c.run()

if __name__ == '__main__':
    main()