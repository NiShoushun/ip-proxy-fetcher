

# IP PROXY FETCHER

[toc]

### 使用方式

#### 启动程序

修改项目根目录下的 `setting.json` 配置文件。

> 注意：
>
> setting.json 中的数据库了连接url。
>
> redis-server auth设置：
>
> ```bash
> config set requirepass 123456
> ```

运行 `runspider.sh` 

运行 `runserver.sh` 

#### 请求代理ip

通过向web api 发送请求，返回对应的json数据。

| api       | 说明                                       | 参数                                 |
| --------- | ------------------------------------------ | ------------------------------------ |
| `/get`    | 获取一个随机的代理                         | `type`: 代理类型（`http` | `https`)  |
| `/all`    | 获取包含所有的代理的列表                   | `type`: 代理类型（`http` | `https`)  |
| `/count`  | 获取抓取的代理数量                         |                                      |
| `/pop`    | 获取一个随机的代理，并从数据库中删除该代理 | `type`: 代理类型（`http` | `https`） |
| `/delete` | 删除代理                                   | `proxy`: `ip:port`                   |

#### 测试

`runspider.sh`：

对每个网站开启一个爬虫线程：

![image-20211125101654929](https://ni187note-pics.oss-cn-hangzhou.aliyuncs.com/notes-img/image-20211125101723222.png)

开始抓取代理数据：![image-20211125101759088](https://ni187note-pics.oss-cn-hangzhou.aliyuncs.com/notes-img/image-20211125101759088.png)

验证代理有效性：![image-20211125102223788](https://ni187note-pics.oss-cn-hangzhou.aliyuncs.com/notes-img/image-20211125102223788.png)

请求web api ： `http://localhost:8080/all` 获取抓取到的代理数据：

![image-20211125102328837](https://ni187note-pics.oss-cn-hangzhou.aliyuncs.com/notes-img/image-20211125102328837.png)

结合 `requests` 库使用代理：

```python
import requests
from pprint import pprint

if __name__ == "__main__":
    proxy = requests.get("http://127.0.0.1:8080/get?type=http").json()
    resp = requests.get("https://bilibili.com", proxies={proxyDict["type"]: proxyDict["proxy"]})
    print(resp.text)
```

![image-20211219220615825](https://ni187note-pics.oss-cn-hangzhou.aliyuncs.com/notes-img/image-20211219220615825.png)

