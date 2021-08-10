from bs4 import BeautifulSoup
import requests
import html5lib
import json
import re
import xlrd
import xlwt


###爬取96款热门机型的链接###
phones_link = []

###机型信息###
'''
    {
        "name": ,
        "os": ,
        "type": ,
        "brand": ,
        "size": ,
        "resolution": ,
        "cpu": ,
        "screen": 
    }
'''

###页面1###
url1 = 'https://detail.zol.com.cn/cell_phone_index/subcate57_0_list_1_0_1_2_0_1.html'
html1 = requests.get(url1)
soup1 = BeautifulSoup(html1.text, 'html5lib')
phones1 = soup1.select('#J_PicMode > li')
for item1 in phones1:
    if 'data-follow-id' in item1.attrs and item1.select('.price-row')[0].span.attrs['class'][0] == 'price-tip':
        phones_link.append('https://detail.zol.com.cn' + item1.select('.pic')[0]['href'])

###页面2###
url2 = 'https://detail.zol.com.cn/cell_phone_index/subcate57_0_list_1_0_1_2_0_2.html'
html2 = requests.get(url2)
soup2 = BeautifulSoup(html2.text, 'html5lib')
phones2 = soup2.select('#J_PicMode > li')
for item2 in phones2:
    if 'data-follow-id' in item2.attrs and item2.select('.price-row')[0].span.attrs['class'][0] == 'price-tip':        #非概念产品
        phones_link.append('https://detail.zol.com.cn' + item2.select('.pic')[0]['href'])


workbook = xlwt.Workbook()
sheet = workbook.add_sheet('sheet 1')
sheet.write(0, 0, 'ID')
sheet.write(0, 1, '设备名称')
sheet.write(0, 2, '操作系统版本')
sheet.write(0, 3, '手机型号')
sheet.write(0, 4, '手机品牌')
sheet.write(0, 5, '屏幕尺寸')
sheet.write(0, 6, '屏幕分辨率')
sheet.write(0, 7, 'CPU')
sheet.write(0, 8, '屏幕类型')
sheet.write(0, 9, '备注')
sheet.write(0, 10, '链接')

with open('./brands.json', 'r', encoding='utf-8') as f:
    brands = json.load(f)
    for (index, link) in enumerate(phones_link):
        html = requests.get(link)
        soup = BeautifulSoup(html.text, 'html5lib')
        paras_link = 'https://detail.zol.com.cn' + soup.select('.section-more')[0]['href']
        paras_html = requests.get(paras_link)
        paras_soup = BeautifulSoup(paras_html.text, 'html5lib')
        phone = {}
        title = paras_soup.select('.product-model__name')[0].get_text()
        name = title[0:title.find('（')]

        os = paras_soup.find(text='出厂系统内核')
        os = os.parent.parent.next_sibling.next_sibling.span.get_text()
        os = os.replace('>','')

        cpu = paras_soup.find(text='CPU型号')
        cpu = cpu.parent.parent.next_sibling.next_sibling.span.get_text("|")
        cpu = cpu[:cpu.find('|')]
        cpu = cpu.replace(" ","")

        size = paras_soup.find(text='主屏尺寸')
        size = size.parent.parent.next_sibling.next_sibling.span.get_text("|")
        size = size[:size.find('|')]

        resolution = paras_soup.find(text='分辨率：')
        resolution = resolution.parent.next_sibling.get_text()
        resolution = resolution.replace('像素','')

        brand = ''
        phone_type = ''

        for b in brands:
            if re.match(b, name) is not None:
                brand = re.search(b, name).group(0)
                phone_type = name[re.search(b, name).end():]
                break
        
        # try:
        #     cursor.execute("insert into phones(pname,os,ptype,brand,size,resolution,pcpu) values('%s','%s','%s','%s',%s,'%s','%s')" %(name,os,phone_type,brand,size.replace('英寸',''),resolution,cpu))
        # except:
        #     conn.rollback()
        sheet.write(index + 1, 0, index + 1)
        sheet.write(index + 1, 1, name)
        sheet.write(index + 1, 2, os)
        sheet.write(index + 1, 3, phone_type)
        sheet.write(index + 1, 4, brand)
        sheet.write(index + 1, 5, size)
        sheet.write(index + 1, 6, resolution)
        sheet.write(index + 1, 7, cpu)
        sheet.write(index + 1, 10, paras_link)

workbook.save('热门机型.xls')
