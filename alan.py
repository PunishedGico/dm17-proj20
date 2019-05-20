import jwt
import json
import requests
import time

with open("url", "r") as f:
    url = f.read()

with open("secret", "r") as f:
    secret = f.read()

flightId = 0

claims = {
    "iss" : "test",
    "exp" : int(time.time()) + 3600
}

token = jwt.encode(claims, secret, "HS256")

stuff = {
    "system" : "test",
    "token" : token.decode("utf-8")
}

r = requests.get(url + "go/getAllVideos", stuff)

print(r.url)
print(r.status_code)
print(r.content)

"https://test-hive-rt.lorenztechnology.com/go/downloadvideo/03137efe91ed4a6d967829bb07786505.mp4"

claims = {
    "iss" : "test",
    "exp" : int(time.time()) + 3600
}

token = jwt.encode(claims, secret, "HS256")

stuff = {
    "system" : "test",
    "token" : token.decode("utf-8")
}

r = requests.get("https://test-hive-rt.lorenztechnology.com/go/downloadvideo/03137efe91ed4a6d967829bb07786505.mp4", stuff)

print(r.url)
print(r.status_code)

with open("alan.mp4", "wb") as f:
    f.write(r.content)
