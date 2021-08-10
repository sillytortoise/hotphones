import xlrd
import json
import pymysql

conn = pymysql.connect(host='localhost', port=3306, db='hotphones', user='root', password='')
cursor = conn.cursor(pymysql.cursors.DictCursor)


book = xlrd.open_workbook('热门机型.xls')
sheet1 = book.sheets()[0]
for i in range(1, sheet1.nrows):
    name = sheet1.cell(i,1).value
    os = sheet1.cell(i,2).value
    phone_type = sheet1.cell(i,3).value
    brand = sheet1.cell(i,4).value
    size = sheet1.cell(i,5).value.replace('英寸','')
    resolution = sheet1.cell(i,6).value
    cpu = sheet1.cell(i,7).value
    link = sheet1.cell(i,10).value
    sql = "insert into phones(pname,os,ptype,brand,size,resolution,pcpu,link) values('%s','%s','%s','%s',%s,'%s','%s','%s')" %(name,os,phone_type,brand,size,resolution,cpu,link)
    cursor.execute(sql)

conn.commit()
cursor.close()
conn.close()

