from selenium import webdriver
from lxml import etree
from pymongo import MongoClient

client = MongoClient()
collection = client["TencentJob"]["content"]


class TencentJob:
    def __init__(self):
        self.start_url = "https://careers.tencent.com/jobopportunity.html"
        self.part_url = "https://careers.tencent.com/"  # 工作类型网址前部分

    def parse_url(self, url):
        driver = webdriver.Chrome()
        driver.get(url)
        html = driver.page_source
        return html

    def get_job_content(self, html):
        """
        获取工作类型(包括其名称和其下面的岗位地址)
        :param html:
        :return:
        """
        ele_html = etree.HTML(html)
        div_list = ele_html.xpath("//div[@class='job-content']/div/div")  # 获取工作类型div列表
        job_list = list()
        for div in div_list:
            item = dict()
            item["job_type"] = div.xpath("./div/p/text()")[0]  # 工作类型名称
            item["recruit_url"] = self.part_url + div.xpath("./a/@href")[0]  # 完整的工作类型下面的岗位地址
            job_list.append(item)
        return job_list

    def get_recruit_content(self, html, job_type):
        """
        获取工作类型下的岗位内容
        :param html:
        :return:
        """
        ele_html = etree.HTML(html)
        div_list = ele_html.xpath("//div[@class='recruit-wrap recruit-margin']/div")  # 获取岗位列表
        recruit_list = list()
        for div in div_list:
            item = dict()
            item["type"] = job_type
            item["name"] = div.xpath("./a/h4/text()")[0]
            item["addr"] = div.xpath("./a/p/span[2]/text()")[0]
            item["job_content"] = div.xpath("./a/p[2]/text()")[0]
            recruit_list.append(item)
        return recruit_list

    def save_content(self, item):
        """
            将数据保存在mongodb
        """
        collection.insert_many(item)

    def run(self):
        html = self.parse_url(self.start_url)  # 获取主页源代码
        job_list = self.get_job_content(html)  # 获取工作类型列表
        print(job_list)
        for job in job_list:
            print(job["recruit_url"])
            html = self.parse_url(job["recruit_url"])
            recruit_list = self.get_recruit_content(html, job["job_type"])  # 提取岗位信息
            print(recruit_list)
            self.save_content(recruit_list)  # 保存数据到数据库


if __name__ == '__main__':
    spider = TencentJob()
    spider.run()
    ret = collection.find({"name": 1, "addr": 1})
    for i in ret:
        print(i)
