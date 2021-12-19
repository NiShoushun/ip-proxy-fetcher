import requests
from pprint import pprint

if __name__ == "__main__":
    proxy = requests.get("http://127.0.0.1:8080/get?type=http").json()
    resp = requests.get("https://bilibili.com", proxies={proxy["type"]: proxy["proxy"]})
    print(resp.text)

