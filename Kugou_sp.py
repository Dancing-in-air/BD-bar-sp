import requests
from lxml import etree
import re
import time


class KuGog:
    def __init__(self):
        # self.start_url_com="https://www.kugou.com/yy/html/rank.html"
        self.start_url = "https://www.kugou.com/yy/html/rank.html"
        self.header_comp = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                          "Chrome/73.0.3683.75 Safari/537.36"}
        self.header_ip = {"authority": "m3ws.kugou.com",
                          "method": "GET",
                          "path": "/kgsong/105vwk10.html",
                          "scheme": "https",
                          "user-agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, "
                                        "like Gecko) Chrome/73.0.3683.75 Mobile Safari/537.36",
                          "cookie": "uidData=%7B%22list%22%3A%5B%7B%22u%22%3A%22%22%7D%2C%7B%22u%22%3A%22%22%7D%2C%7B%22u%22%3A%22%22"
                                    "%7D%2C%7B%22u%22%3A%22%22%7D%2C%7B%22u%22%3A%22%22%7D%2C%7B%22u%22%3A%22%22%7D%2C%7B%22u%22%3A%22%22%7D%2C%7B%22u%22%3A%22%22%7D%2C%7B%22u%22%3A%22%22%7D%2C%7B%22u%22%3A%22%22%7D%2C%7B%22u%22%3A%22%22%7D%2C%7B%22u%22%3A%22%22%7D%2C%7B%22u%22%3A%22%22%7D%2C%7B%22u%22%3A%22%22%7D%2C%7B%22u%22%3A%22%22%7D%2C%7B%22u%22%3A%22%22%7D%5D%7D; kg_mid=a4aea1dccb0ca4f9d730da5581c11e6e; kg_dfid=3ve36F1twpJ10Xx8Jx0hgQG8; kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e; PHPSESSID=46e77s3cj6cd74en3hdtrp3e13; musicwo17=kugou; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1572670424,1572676143,1572678500; verify_st=undefined; Hm_lvt_85cd0cae296886f72cae1a333a549fe7=1572680772,1572682736,1572683596,1572683951; kg_mid_temp=a4aea1dccb0ca4f9d730da5581c11e6e; ACK_SERVER_10015=%7B%22list%22%3A%5B%5B%22bjlogin-user.kugou.com%22%5D%5D%7D; ACK_SERVER_10016=%7B%22list%22%3A%5B%5B%22bjreg-user.kugou.com%22%5D%5D%7D; ACK_SERVER_10017=%7B%22list%22%3A%5B%5B%22bjverifycode.service.kugou.com%22%5D%5D%7D; Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d=1572684870; Hm_lpvt_85cd0cae296886f72cae1a333a549fe7=1572684916",

                          }

    def parse_url(self, url, header):
        """
        发送请求,获取响应
        :param url: 网页地址
        :param header: 请求头
        :return:
        """
        response = requests.get(url, headers=header)
        print(response)
        return response.content.decode()

    def get_song_info(self, html):
        """
        获取歌曲的名字,电脑版IP,以及电脑版中歌曲id
        :param html:
        :return:
        """
        ele_html = etree.HTML(html)
        li_list = ele_html.xpath("//ul/li[@class=' ']")
        print(li_list)
        song_list = list()
        for li in li_list:
            song_solo_info = dict()
            song_solo_info["name"] = li.xpath("./@title")[0]  # 获取歌曲名称
            song_solo_info["addr"] = li.xpath("./a/@href")[0]
            pat = re.compile(r"https://www.kugou.com/song/(.*?)\.html")  # 获取歌曲电脑版地址
            song_solo_info["id"] = pat.findall(song_solo_info["addr"])[0]  # 获取歌曲id,用于手机
            song_list.append(song_solo_info)
        return song_list

    def get_down_url(self, id):
        """
        提取手机版歌曲下载地址-----目前失败
        :param id: 电脑版歌曲id
        :return:  歌曲下载地址
        """
        song_url = "https://m3ws.kugou.com/kgsong/{}.html".format(id)
        print(song_url)
        down_response = self.parse_url(song_url, self.header_ip)  # 下载手机版页面请求,获取响应
        print(down_response)  # 此处有问题,服务端可能存在反爬机制,导致返回的内容一直变动,提取不到地址
        pat = re.compile(r"'url':'(.*?)',")  # 无法提取
        down_url = pat.findall(down_response)
        print(down_url)
        return down_url

    def save_content(self, name, content):
        """
        保存歌曲
        :param name: 歌曲名称
        :param content: 歌曲内容
        :return:
        """
        with open("{}.mp3".format(name), "wb") as f:
            f.write(content)

    def run(self):
        html = self.parse_url(self.start_url, self.header_comp)
        song_list = self.get_song_info(html)
        print(song_list)
        for item in song_list:
            song_id = item["id"]
            song_name = item["name"]
            down_url = self.get_down_url(song_id)  # 调用函数,获取下载地址
            song_content = self.parse_url(down_url, self.header_ip).content.decode()
            self.save_content(song_name, song_content)  # 调用函数保存歌曲
            time.sleep(3)


if __name__ == '__main__':
    spider = KuGog()
    spider.run()
