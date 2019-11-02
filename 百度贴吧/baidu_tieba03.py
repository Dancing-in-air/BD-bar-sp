import requests
from lxml import etree
import json


class BdbarSpider:
    def __init__(self, name):
        self.start_url = "https://tieba.baidu.com/f?kw=" + name + "&pn=0"
        self.part_url = "https://tieba.baidu.com"  # 图片地址前部分
        self.header = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Mobile Safari/537.36"}
        self.bar_name = name

    def parse_url(self, url):  # 发送请求,获取响应
        response = requests.get(url, headers=self.header)
        # print(response.content.decode())
        return response.content.decode()

    def get_content_list(self, html_str):  # 提取数据
        html = etree.HTML(html_str)
        li_list = html.xpath("//li[contains(@class,'tl_shadow')]")
        content_list = []
        for li in li_list:
            item = dict()  # 创建一个空字典 用于接收提取数据 不能创建在for语句外面
            # 提取贴吧帖子发帖人
            item["name"] = li.xpath(".//div/span[@class='ti_author']/text()")[0] if len(
                li.xpath(".//div/span[@class='ti_author']/text()")) > 0 else None
            # 提取贴吧帖子的名字
            item["title"] = li.xpath(".//div[@class='ti_title']/span/text()")[0] if len(li.xpath(".//div["
                                                                                                 "@class='ti_title']/span/text()")) > 0 else None
            # 提取贴吧帖子的地址
            url = li.xpath("./a/@href")[0] if len(li.xpath("./a/@href")) > 0 else None
            item["href"] = self.part_url + url
            content_list.append(item)

        return content_list

    def get_img_list(self, detail_url):  # 获取帖子中的图片
        pass

    def save_content_list(self, content_list):
        file_path = self.bar_name + ".txt"
        with open(file_path, "a") as f:
            for content in content_list:
                f.write(json.dumps(content, ensure_ascii=False, indent=3))
                f.write("\n")

    def run(self):
        url = self.start_url
        html_str = self.parse_url(url)
        content_list = self.get_content_list(html_str)
        # 保存数据
        self.save_content_list(content_list)


if __name__ == '__main__':
    spider = BdbarSpider("做头发")
    spider.run()
