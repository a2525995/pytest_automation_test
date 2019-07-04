# -*- coding: utf-8 -*-


'''
读取接口配置数据
'''
import os
import csv

class DataReader:

    def __init__(self):
        self.queries = []
        self.path_dir = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

    def readQueryList(self,file_name):
        file_path = '/Params/Data/'+file_name
        self.queries = csv.reader(open(self.path_dir + file_path, 'rt', encoding='utf-8'))
        data = []
        for query in self.queries:
            data.append(' '.join(query))

        return data

if __name__ == '__main__':
    reader = DataReader()
    qys = reader.readQueryList('query.csv')
    for qy in qys:
        print(qy)