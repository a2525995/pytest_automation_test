# encoding: utf-8
import requests
import sys, os

BASE_DIR = os.path.dirname(os.path.dirname(os.getcwd()))

sys.path.append(BASE_DIR)

class Token:

    def __init__(self):
        self.header = {
            "Content-Type": "application/json",
            "SOPHON-Auth-Token": "auth_token"

        }

    def getToken(self,login_url,username,password):

        data = {
            "username": username,
            "password": password
        }
        login_headers = {'Content-Type': 'application/json'}
        login_res = requests.post(url=login_url, json=data, headers=login_headers)

        login_token = login_res.headers["SOPHON-Auth-Token"]
        login_uid = login_res.json()['id']
        return login_token, login_uid

    def getHeader(self,login_token):
        self.header["SOPHON-Auth-Token"] = login_token
        return self.header



if __name__ == '__main__':
    print(Token().getToken('http://172.17.6.30:18888/user/login', '100114', '1111qqqq'))
