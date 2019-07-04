import os

default_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Conf/config.ini")

with open(default_path, 'r', encoding="utf-8") as f:
    tmp = f.readlines()
    for i in tmp:
        print(i)
        print(f.tell())

