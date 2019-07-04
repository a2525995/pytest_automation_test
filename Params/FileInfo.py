# -*- coding: utf-8 -*-

import os
import hashlib
import json

_FILE_SLIM = (100 * 1024 * 1024)  # 100MB


class FileInfo:
    def __init__(self):
        self.path_dir = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

    def get_fileInfo(self, filename):
        print(self.path_dir)
        file_path = os.path.join(self.path_dir ,'Params//Data//' , filename)
        # file_path = self.path_dir + '/Params/Data/' + filename
        hmd5 = hashlib.md5()
        fp = open(file_path, "rb")
        f_size = os.stat(file_path).st_size
        if f_size > _FILE_SLIM:
            while f_size > _FILE_SLIM:
                if (f_size > 0) and (f_size <= _FILE_SLIM):
                    hmd5.update(fp.read())
        else:
            hmd5.update(fp.read())
        md5 = hmd5.hexdigest()
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)

        file_infos = {"file_name": file_name, "md5": md5, "file_size": file_size, "file_path": file_path}
        return json.dumps(file_infos)


if __name__ == '__main__':
    print(FileInfo().get_fileInfo("New-phonegis.xlsx"))
