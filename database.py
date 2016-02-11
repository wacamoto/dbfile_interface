import os
import csv
import json
import sqlite3

class Datafile:
    # base class
    def __init__(self, path):
        self.path = path
        self.exist = os.path.isfile(self.path)

    @staticmethod
    def int(name):
        return {'field_type':'int', 'field_name': name}

    @staticmethod
    def float(name):
        return {'field_type':'real', 'field_name': name}

    @staticmethod
    def string(name):
        return {'field_type':'text', 'field_name': name}

class Sqlite_db(Datafile):
    # sqlite datafile interface
    def __init__(self, path):
        super().__init__(path)

        # if sqlite database does not exist 
        # it will be created 
        self.db = sqlite3.connect(path)

    def fields(self, *field):
        if self.exist: return True # for temp
        tableField = []
        for f in field:
            tableField.append((f['field_name'] + ' ' + f['field_type']))
        tableField = '(%s)' % ','.join(tableField)

        # create table
        self.db.execute('CREATE TABLE DATA ' + tableField)

    def insert(self, **value):
        val = []
        key = [str(i) for i in value.keys()]
        for i in value.values():
            if isinstance(i, str):
                val.append('"%s"' % str(i))
            else:
                val.append(str(i))
        
        key = '(%s)' % ','.join(key)
        val = '(%s)' % ','.join(val)

        self.db.execute('INSERT INTO DATA' + key + 'values' + val)
        self.db.commit()

    def close(self):
        self.db.close()

class Json_db(Datafile):
    # json datafile interface
    def __init__(self, path):
        super().__init__(path)

        # opens for writing and reading, if it does 
        # not exist then create it and open it
        self.file = open(path, 'w+')
        self.json= {"data": []}

    def fields(self, *field):
        pass

    def insert(self, **value):
        self.json['data'] += [value]

    def close(self):
        json.dump(self.json, self.file, indent=4)
        self.file.close()

class Csv_db(Datafile):
    # csv datafile interface
    def __init__(self, path):
        super().__init__(path)
        
        # opens for writing and reading, if it does 
        # not exist then create it and open it
        self.file = open(path, 'w+')

    def fields(self, *field):
        header = [f['field_name'] for f in field]
        self.writer = csv.DictWriter(self.file, header)
        writer = csv.writer(self.file)
        writer.writerow(header)
        
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

def container(spring):
    # inject spring into container retrun object interface
    # use this class fields type defined datafile fields
    pass