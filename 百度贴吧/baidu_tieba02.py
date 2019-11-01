import requests


class BdbarSpider:
    def __init__(self, bar_name, pages):
        """

        :param bar_name: 贴吧名称  str
        :param pages: 想要获取的页数 int
        """
        self.bar_name = bar_name
        self.pages = pages
        self.url_temp = "https://tieba.baidu.com/f?kw=" + bar_name + "&ie=utf-8&pn={}"
        self.header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"}

    def __get_url_list(self, pages):
        """
        获取请求的url列表
        :param bar_name: 贴吧名称  str
        :param pages: 查询页数  int
        :return:
        """
        # url_list = list()
        # for i in range(pages):
        #     url_list.append(self.url_temp.format(i * 50))
        # return url_list  # 返回url列表
        return [self.url_temp.format(i * 50) for i in range(pages)]

    def __parse_url(self, url):
        """
        发送请求,获取响应
        :param url: 请求地址
        :return: 响应
        """
        response = requests.get(url, headers=self.header)
        return response.content.decode()

    def __save_html(self, ret, page_num):
        """
        保存内容到本地
        :param ret: 响应内容
        :param page_num: 响应内容的页数
        :return: None
        """
        with open("{}贴吧-第{}页.html".format(self.bar_name, page_num), "w") as f:
            f.write(ret)

    def run(self):
        """

        :return:
        """
        url_list = self.__get_url_list(self.pages)  # 调用函数 获取网页列表
        for url in url_list:
            page_num = url_list.index(url) + 1
            ret = self.__parse_url(url)  # 调用函数 获取响应内容
            self.__save_html(ret, page_num)  # 调用函数 保存内容到本地
            print("{}贴吧-第{}页.html".format(self.bar_name, page_num))


if __name__ == '__main__':
    spider = BdbarSpider("美女", 5)
    spider.run()
