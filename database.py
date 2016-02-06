import os
import csv
import sqlite3

class Datafile:
    # base class
    def __init__(self, path):
        self.path = path

    def exist(self):
        return os.path.isfile(self.path)

    @staticmethod
    def int(name):
        return {'field_type':'int', 'field_name': name}

    @staticmethod
    def float(name):
        return {'field_type':'float', 'field_name': name}

    @staticmethod
    def string(name):
        return {'field_type':'string', 'field_name': name}

# class Sqlite_db(Datafile):
#     # sqlite databe interface
#     def __init__(self, path):
#         super().__init__(path)

#     def fields(self, field):
#         pass

#     def insert(self, value):
#         pass

#     def close(self):
#         pass

# class Json_db(Datafile):
#     # json databe interface
#     def __init__(self, path):
#         super().__init__(path)

#     def fields(self, field):
#         pass

#     def insert(self, value):
#         pass

#     def close(self):
#         pass

class Csv_db(Datafile):
    # csv database interface
    def __init__(self, path):
        super().__init__(path)
        
        # opens for writing and reading if, it does 
        # not exist then create it and open it
        self.file = open(path, 'w+')

    def fields(self, *field):
        header = [f['field_name'] for f in field]
        writer = csv.writer(self.file)
        writer.writerow(header)
        self.writer = csv.DictWriter(self.file, header)
        
    def insert(self, **value):
        self.writer.writerow(value)

    def close(self):
        self.file.close()

# datafile interface factory
def database(config):
    # get app config setting
    path = config.datafile_path

    f_extension = os.path.splitext(path)[1]
    print('file type:' + f_extension)

    # return datafile interface object
    if f_extension == '.json':
        return Json_db(path)
    elif f_extension == '.csv':
        return Csv_db(path)
    elif f_extension == '.db':
        return Sqlite_db(path)
    else:
        return False
