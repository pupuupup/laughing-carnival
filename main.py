# -- coding: utf-8 --

import unicodecsv as csv
import config
import re
import glob
import requests
import urllib
from bs4 import BeautifulSoup
import sys
import os.path
import json
import atexit
from fractions import Fraction
from collections import OrderedDict


proxies = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}

#TODO
#
# 1. make image
# 2. add description header and footer
# 3. remove link from description
#


reload(sys)
sys.setdefaultencoding('utf-8')
keys = config.getKeys()

dataShield = OrderedDict({
    "Z": {
        "value": 'ฝาเหล็ก ',
        "images": 'http://www.skf.com/binary/30-28366/SSDGBB_open-1-1_ratio__.jpg'
    },
    "RS": {
        "value": 'ฝายาง ',
        "images": 'https://msk.rost-holding.ru/upload/shop_4/2/0/9/item_20960/63004-2rs.jpg'
    },
    "": {
        "value": '',
        "images": 'https://msk.rost-holding.ru/upload/shop_4/2/0/9/item_20960/63004-2rs.jpg'
    }
})

dataCage = OrderedDict({
    "ECM": {
        "value": 'รังทองเหลือง ',
        "images": 'https://i.ebayimg.com/images/g/CvQAAOSw8Y1btrEy/s-l640.jpg'
    },
    "ECP": {
        "value": 'รังโพลี่ยาไมด์ ',
        "images": 'https://msk.rost-holding.ru/upload/shop_4/2/0/9/item_20960/63004-2rs.jpg'
    }
})

dataHousing = OrderedDict({
    "SYJ": {
        "value": 'เสื้อตุ๊กตาพลัมเม่อบล็อก ',
        "images": 'http://www.skf.com/binary/30-300948/p2b_mounted_unit_ball-fm_101_0_701_600.jpg'
    },
    "FYJ": {
        "value": 'เสื้อสี่เหลี่ยมหน้าแปลน ',
        "images": "http://www.skf.com/binary/30-300951/f4b_mounted_unit_ball-fm_155_0_755_600.jpg"
    }
})

dataBore = OrderedDict({
    "K": {
        "value": 'รูเตเปอร์ รู K ',
        "images": 'http://www.skf.com/binary/30-153089/22320-E.jpeg'
    },
    "": {
        "value": 'รูตรง ',
        "images": 'http://www.skf.com/binary/30-153089/22320-E.jpeg'
    }
})

dataClearance = {
    "C3": {
        "value": 'รองรับความเร็วรอบและความร้อนสูง ',
    },
    "C4": {
        "value": 'รองรับความเร็วรอบและความร้อนสูงมาก ',
    }
}

def importData():
    reader = csv.DictReader(open('data.csv', 'rb'))
    d = []
    for l in reader:
        d.append(l)
    return d

def isNotDone(data):
    if "done" in data:
        if data["done"] == 1 or data["done"] == "1":
            return False
        else:
            return True
    else:
        return True

def editTitle(datas):
    count = 1
    for data in datas:
        count = count + 1
        if not isNotDone(data):
            title = data['title']
            data['title'] = data['title'] + " SKF "
            data['dimension_text'] = ''
            data['image_url'] = title.replace('/', '-').replace(' ', '_')
            soup = BeautifulSoup(data['html'], 'html.parser')
            normalisedTitle = ''

            #for Deep Groove Ball Bearing
            if count > 0 and count <= 589:
                #shield
                d = soup.find("td", text="d").findNextSibling("td").findNextSibling("td").contents[0]
                D = soup.find("td", text="D").findNextSibling("td").findNextSibling("td").contents[0]
                B = soup.find("td", text="B").findNextSibling("td").findNextSibling("td").contents[0]
                for key in dataShield.keys():
                    if key in title:
                        data['category'] = 'Deep Groove Ball Bearing'
                        data['category_th'] = 'ตลับลูกปืนเม็ดกลมล่องลึก '
                        data['dimension'] = d + 'x' + D + 'x' + B
                        data['dimension_text'] = '(' + data['dimension']  + ')'
                        data['title'] = data['title'] + data['category_th']
                        data['title'] = data['title'] + dataShield[key]['value']
                        data['image0'] = dataShield[key]['images']
                        data['height'] = int(B) + 5
                        data['width'] = int(D) + 5
                        data['length'] = int(D) + 5
                        normalisedTitle = title.replace('-', ' ')
                        normalisedTitle = normalisedTitle.replace('/', ' ')
                        break


            #for Cylindrical Roller Bearing
            if count > 589 and count <= 675:
                #cage
                d = soup.find("td", text="d").findNextSibling("td").findNextSibling("td").contents[0]
                D = soup.find("td", text="D").findNextSibling("td").findNextSibling("td").contents[0]
                B = soup.find("td", text="B").findNextSibling("td").findNextSibling("td").contents[0]
                for key in dataCage.keys():
                    if key in title:
                        data['category'] = 'Cylindrical Roller Bearing'
                        data['category_th'] = 'ตลับลูกปืนเม็ดทรงกระบอก '
                        data['dimension'] = d + 'x' + D + 'x' + B
                        data['dimension_text'] = '(' + data['dimension']  + ')'
                        data['title'] = data['title'] + data['category_th']
                        data['title'] = data['title'] + dataCage[key]['value']
                        data['image0'] = dataCage[key]['images']
                        data['height'] = int(B) + 5
                        data['width'] = int(D) + 5
                        data['length'] = int(D) + 5
                        normalisedTitle = title.replace('-', ' ')
                        normalisedTitle = normalisedTitle.replace('/', ' ')
                        break

            #for Y-Bearing
            if count > 675 and count <= 698:
                #cage
                d = soup.find("td", text="d").findNextSibling("td").findNextSibling("td").contents[0]
                L = soup.find("td", text="L").findNextSibling("td").findNextSibling("td").contents[0]
                A = soup.find("td", text="A").findNextSibling("td").findNextSibling("td").contents[0]
                B = soup.find("td", text="B").findNextSibling("td").findNextSibling("td").contents[0]
                try:
                    H = soup.find("td", text="H").findNextSibling("td").findNextSibling("td").contents[0]
                except:
                    pass
                for key in dataHousing.keys():
                    if key in title:
                        unit = ''
                        try:
                            d = int(d)
                            unit = 'มม.'
                        except:
                            d = float(d)
                            unit = 'นิ้ว'
                            if d == 25.4:
                                d = '1\"'
                            elif d == 38.1:
                                d = '1\"1/2'
                            elif d == 31.75:
                                d = '1\"1/4'
                            elif d == 44.45:
                                d = '1\"3/4'
                            elif d == 50.8:
                                d = '2\"'
                        data['category'] = 'Bearing Units Y-Bearing'
                        data['category_th'] = 'ตลับลูกปืนชุด '
                        data['dimension'] = 'รูเพลา ' + str(d) + unit
                        data['dimension_text'] = '(' + data['dimension']  + ')'
                        data['title'] = data['title'] + data['category_th']
                        data['title'] = data['title'] + dataHousing[key]['value']
                        data['image0'] = dataHousing[key]['images']
                        data['height'] = float(L) + 5
                        data['length'] = float(L) + 5
                        if A > B:
                            data['width'] = float(A) + 5
                        else:
                            data['width'] = float(B) + 5
                        normalisedTitle = title.replace('-', ' ')
                        break

            #for Spherical Roller Bearing
            if count > 699 and count <= 751:
                #Bore
                d = soup.find("td", text="d").findNextSibling("td").findNextSibling("td").contents[0]
                D = soup.find("td", text="D").findNextSibling("td").findNextSibling("td").contents[0]
                B = soup.find("td", text="B").findNextSibling("td").findNextSibling("td").contents[0]
                keys = ["K", ""]
                for key in keys:
                    if key in title:
                        data['category'] = 'Spherical Roller Bearing'
                        data['category_th'] = 'ตลับลูกปืนเม็ดโค้งสองแถวปรับแนวได้เอง '
                        data['dimension'] = d + 'x' + D + 'x' + B
                        data['dimension_text'] = '(' + data['dimension']  + ')'
                        data['title'] = data['title'] + data['category_th']
                        data['title'] = data['title'] + dataBore[key]['value']
                        data['image0'] = dataBore[key]['images']
                        data['height'] = int(B) + 5
                        data['width'] = int(D) + 5
                        data['length'] = int(D) + 5
                        normalisedTitle = title.replace('-', ' ')
                        normalisedTitle = normalisedTitle.replace('/', ' ')
                        break

            #clearance
            for key in dataClearance.keys():
                if key in title:
                    data['title'] = data['title'] + dataClearance[key]['value']
                    break

            data['title'] = data['title'] + normalisedTitle + ' '
            data['title'] = data['title'] + data['dimension_text']
            print data['title']
    return datas




def main():
    datas = importData()
    datas = editTitle(datas)
    toCSV(datas)

def toCSV(datas):
    keys = datas[0].keys()
    try:
        with open("data_updated.csv", 'wb') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(datas)
    except Exception as e:
        raise e

main()

