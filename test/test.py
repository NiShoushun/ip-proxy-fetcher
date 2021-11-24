import requests
from pprint import pprint

if __name__ == "__main__":
    for i in requests.get("http://127.0.0.1:8080/all/").json():
        pprint(i)