




import requests
from lxml import etree

headers = {
         'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24'
    }
url = 'http://bbs.guilinlife.com/forum.php?mod=viewthread&tid=9837843&extra=page%3D1'
res = requests.get(url, headers = headers)
response = etree.HTML(res.text)
# list3 = response.xpath(
#     "/html/body/div[6]/div[5]/div[2]/div[2]/div[2]/div/div[2]/div/div/table/tbody/tr[1]/td[2]/div[2]/div/div[1]/table/tbody/tr/td/div//text()")
# 2.获取主页面中的信息

list3 = response.xpath("//div[@id='first']//div[@class='t_fsz']//td[@class='t_f']//text()[normalize-space(.)]")
# list3 = response.xpath("/html/body/div[6]/div[5]/div[2]/div[2]/div[2]/div/div[2]/div/div/table/tbody/tr[1]/td[2]/div[2]/div/div[1]/table/tbody/tr/td/div//text()[normalize-space(.)]")
content = ' '.join(list3)


print(content)
#
# date = response.xpath("/html/body/div[6]/div[5]/div[2]/div[2]/div/div/div[2]/div/div/table/tbody/tr[1]/td[2]/div[1]/div[2]/div[2]/em/text()")
# date = ' '.join(date)
# print(date)