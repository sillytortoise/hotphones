import xlwt
import json
import pymysql

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

conn = pymysql.connect(host='localhost', port=3306, db='hotphones', user='root', password='')
cursor = conn.cursor(pymysql.cursors.DictCursor)
cursor.execute('select * from phones')
results = cursor.fetchall()

for index,item in enumerate(results):
    sheet.write(index+1, 0, item['id'])
    sheet.write(index+1, 1, item['pname'])
    sheet.write(index+1, 2, item['os'])
    sheet.write(index+1, 3, item['ptype'])
    sheet.write(index+1, 4, item['brand'])
    sheet.write(index+1, 5, str(item['size'])+'英寸')
    sheet.write(index+1, 6, item['resolution'])
    sheet.write(index+1, 7, item['pcpu'])
    sheet.write(index+1, 10, item['link'])

cursor.close()
conn.close()
workbook.save('./热门机型.xls')

