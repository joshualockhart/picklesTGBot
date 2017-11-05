import requests
import config
import json

BACKEND_URL = config.PICKLES_BACKEND_URL

class PicklesHandler():
    def __init__(self):
        self.url = BACKEND_URL

    def get_userid_from_username(self, username):
        try:
            r = requests.post(self.url+'/getuserbyusername', json={"username": str(username)})
            if r.status_code == 200:
                return json.loads(r.text)['id']
            elif r.status_code == 404:
                raise ValueError("No user with username '{}'".format(username))
        except BaseException as ex:
            raise(ex)

    def new_user(self, username):
        try:
            r = requests.post(self.url+'/adduser', json={"username": str(username)})
            if r.status_code == 200:
                return json.loads(r.text)['id']
        except BaseException as ex:
            raise(ex)

    def new_sheet(self, name, owner):
        try:
            r = requests.post(self.url+'/addsheet', json={"name": str(name), "owner_id": str(owner)})
            if r.status_code == 200:
                return json.loads(r.text)['id']
        except BaseException as ex:
            raise(ex)

    def new_element(self, data, sheet_id):
        try:
            r = requests.post(self.url+'/addelement', json={"data": str(data), "sheet_id": str(sheet_id)})
            if r.status_code == 200:
                return json.loads(r.text)['id']
        except BaseException as ex:
            raise(ex)

    def get_sheets(self, user_id):
        try:
            r = requests.post(self.url+'/getsheetsofuser', json={"id": str(user_id)})
            if r.status_code == 200:
                results = json.loads(r.text)
                return results
        except BaseException as ex:
            raise(ex)

    def get_data_in_sheet(self, sheet_id):
        try:
            r = requests.post(self.url+'/getelementsofsheet', json={"id": str(sheet_id)})
            if r.status_code == 200:
                results = json.loads(r.text)
                return results
        except BaseException as ex:
            raise(ex)

   
