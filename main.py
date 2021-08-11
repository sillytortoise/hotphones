from bs4 import BeautifulSoup
import requests
import html5lib
import json
import re
import pymysql


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

###页面循环###
for i in range(1, 8):
    url1 = 'https://detail.zol.com.cn/cell_phone_index/subcate57_0_list_1_0_1_2_0_%d.html' % i
    html1 = requests.get(url1)
    soup1 = BeautifulSoup(html1.text, 'html5lib')
    phones1 = soup1.select('#J_PicMode > li')
    for item1 in phones1:
        if 'data-follow-id' in item1.attrs and item1.select('.price-row')[0].span.attrs['class'][0] == 'price-tip':
            phones_link.append('https://detail.zol.com.cn' +
                               item1.select('.pic')[0]['href'])



with open('./brands.json', 'r', encoding='utf-8') as f:
    conn = pymysql.connect(host='localhost', port=3306,
                           user='root', password='', database='hotphones')
    cursor = conn.cursor()
    brands = json.load(f)
    for (index, link) in enumerate(phones_link):
        print(index, '   ', link)
        html = requests.get(link)
        soup = BeautifulSoup(html.text, 'html5lib')
        img = soup.select('.big-pic')
        if img is not None:
            img = img[0].a.img
            img = img.attrs['src']
        else:
            img = ''

        print(' '+img)

        paras_link = 'https://detail.zol.com.cn' + \
            soup.select('.section-more')[0]['href']
        paras_html = requests.get(paras_link)
        paras_soup = BeautifulSoup(paras_html.text, 'html5lib')
        phone = {}
        title = paras_soup.select('.product-model__name')[0].get_text()


        name = title[0:title.find('（')]

        os = paras_soup.find(text='出厂系统内核')
        if os is not None:
            os = os.parent.parent.next_sibling.next_sibling.span.get_text()
            os = os.replace('>', '')
        else:
            os = ''

        cpu = paras_soup.find(text='CPU型号')
        if cpu is not None:
            cpu = cpu.parent.parent.next_sibling.next_sibling.span.get_text("|")
            cpu = cpu[:cpu.find('|')]
            cpu = cpu.replace(" ", "")
        else:
            cpu = ''

        size = paras_soup.find(text='主屏尺寸')
        if size is not None:
            size = size.parent.parent.next_sibling.next_sibling.span.get_text("|")
            size = size[:size.find('|')]
        else:
            size = ''

        resolution = paras_soup.find(text='分辨率：')
        if resolution is not None:
            resolution = resolution.parent.next_sibling.get_text()
            resolution = resolution.replace('像素', '')
        else:
            resolution = ''

        brand = ''
        phone_type = ''

        isfind = False
        for b in brands:
            if re.match(b, name) is not None:
                brand = re.search(b, name).group(0)
                phone_type = name[re.search(b, name).end():]
                isfind = True
                break

        if isfind == False:
            print(name)
            continue

        try:
            cursor.execute("insert into newphones(pname,os,ptype,brand,size,resolution,pcpu,link,img) values('%s','%s','%s','%s',%s,'%s','%s','%s','%s')" % (
                name, os, phone_type, brand, size.replace('英寸', ''), resolution, cpu, paras_link,img))
        except Exception as e:
            print(e)
            conn.rollback()

    conn.commit()