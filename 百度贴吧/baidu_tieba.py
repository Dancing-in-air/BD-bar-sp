import requests

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": "BIDUPSID=C2D88AA0D52C8427FFEE1DC2987C937B; BAIDUID=D39D4F63A714C52877517598B5F1E053:FG=1; PSTM=1569804073; TIEBAUID=1cf4b247090738ec9d7552a2; TIEBA_USERTYPE=7e3647017f73155bdbf8e141; bdshare_firstime=1570591155576; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=1422_21102_29911_29568_29700_29220_26350; delPer=0; PSINO=7; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1571122671,1571122769,1571138420,1572325137; ZD_ENTRY=baidu; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1572331288",
    "Host": "tieba.baidu.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"
}
dest = input("请输入要爬去的贴吧名字:")
page = int(input("请输入要爬去的页数:"))
number = 0
n = 0
while number <= (page - 1) * 50:
    url = "https://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}".format(dest, number)
    response = requests.get(url, headers=headers, params=dest)
    ret = response.content.decode()
    print(ret)
    print(response.url)
    number += 50
    n += 1
    with open("第{}页.html".format(n), "w", encoding="utf-8") as f:
        f.write(ret)