import jwt
import json
import requests
import time
import os

class Alan():
    def __init__(self):
        self.url = ""
        self.secret = ""

        with open("url", "r") as f:
            self.url = f.read()
        
        with open("secret", "r") as f:
            self.secret = f.read()

    def create_jwt(self):
        claims = {
            "iss" : "test",
            "exp" : int(time.time()) + 3600
        }

        token = jwt.encode(claims, self.secret, "HS256")

        stuff = {
            "system" : "test",
            "token" : token.decode("utf-8")
        }

        return stuff

    def get_all_videos(self):
        r = requests.get(self.url + "go/getAllVideos", self.create_jwt())

        if r.status_code == 200:
            json_data = json.loads(r.text)

            return_list = []
            for p in json_data:
                return_list.append(p["path"])

            return return_list
        else:
            print("Error:" + r.status_code)
            return None

    def download_video(self, url, force=False):
        if os.path.isfile("Test Data/Alan/" + url.split("/")[-1]) is False or force is True:
            print("Downloading: " + url)
            r = requests.get(url, self.create_jwt())

            if r.status_code == 200:
                filename = url.split("/")[-1]
                with open("Test Data/Alan/" + filename, "wb") as f:
                    f.write(r.content)
                
                return "Test Data/Alan/" + filename
            else:
                print("Error:" + r.status_code)
                return None
        else:
            return "Test Data/Alan/" + url.split("/")[-1]
