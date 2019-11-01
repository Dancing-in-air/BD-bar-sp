import requests
import re


class BaiduTieba():
    def __init__(self, name, page):
        self.name = name
        self.page = page
        self.url = "https://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}".format(self.name, (self.page - 1) * 50)
        self.header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"}

    def run(self):
        response = requests.get(self.url, headers=self.header)
        ret = response.content.decode()
        # pat = re.compile("<!--|-->")
        # result = pat.sub("", ret)
        with open("{}贴吧--第{}页.html".format(self.name, self.page), "w") as f:
            f.write(ret)


cat = BaiduTieba("毛泽东", 1)
cat.run()
