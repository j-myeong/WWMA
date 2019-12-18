import requests
import json

class PersonData():
    def getGameData(self):
        self.getURL()
        return self.dic

    def getURL(self):
        URL = 'https://whatiswrongwithmyage.run.goorm.io' + '/result'
        response = requests.get(URL)
        if response.status_code == 200:
            self.data = response.text
            self.dic = json.loads(self.data)
        else:
            self.dic = {"Server_Error":""}

class PersonDataDetail():
    def getGameDataDetail(self):
        self.getURL()
        return self.dic

    def getURL(self):
        URL = 'https://whatiswrongwithmyage.run.goorm.io' + '/result_detail'
        response = requests.get(URL)
        if response.status_code == 200:
            self.data = response.text
            self.dic = json.loads(self.data)
        else:
            self.dic = {"Server_Error":['E', 'R', 'R', 'O', 'R']}
