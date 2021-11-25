![image-20211125101654929](https://ni187note-pics.oss-cn-hangzhou.aliyuncs.com/notes-img/image-20211125101723222.png)

![image-20211125101759088](https://ni187note-pics.oss-cn-hangzhou.aliyuncs.com/notes-img/image-20211125101759088.png)

![image-20211125102223788](https://ni187note-pics.oss-cn-hangzhou.aliyuncs.com/notes-img/image-20211125102223788.png)

![image-20211125102328837](https://ni187note-pics.oss-cn-hangzhou.aliyuncs.com/notes-img/image-20211125102328837.png)

![image-20211125102353041](https://ni187note-pics.oss-cn-hangzhou.aliyuncs.com/notes-img/image-20211125102353041.png)

通过web使用ip

```python
import requests
from pprint import pprint

if __name__ == "__main__":
    for i in requests.get("http://127.0.0.1:8080/all/").json():
        pprint(i)
```

![image-20211125102534899](https://ni187note-pics.oss-cn-hangzhou.aliyuncs.com/notes-img/image-20211125102534899.png)

