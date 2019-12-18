import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import ssl

class FaceAPI():
    def setFile(self, filename):
        self.filename = filename

    def imagecheck(self):
        headers = {
            # Request headers
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': 'e2d275fc90f34570ab0989c1c393626e',
        }

        body = list(open(self.filename, 'rb'))

        params = urllib.parse.urlencode({
            # Request parameters
            'returnFaceId': 'false',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age,gender',
            'recognitionModel': 'recognition_01',
            'returnRecognitionModel': 'false',
            'detectionModel': 'detection_01',
        })

        ssl._create_default_https_context = ssl._create_unverified_context
        try:
            conn = http.client.HTTPSConnection('kace-id.cognitiveservices.azure.com')
            conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
            response = conn.getresponse()
            data = response.read()

        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

        dic = json.loads(data.decode('utf-8'))[0]
        self.result = (dic['faceAttributes']['gender'], dic['faceAttributes']['age'])

        return self.result

    def sendServer(self):
        conn = http.client.HTTPSConnection('whatiswrongwithmyage.run.goorm.io')
        conn.request("GET", "/game?nickname=MS-FaceAPI&gender={gender}&age={age}".format(gender=self.result[0], age=str(int(self.result[1]))))
        response = conn.getresponse()
        return response.code