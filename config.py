import os.path
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Safari/537.36',
    'Accept' : 'text/html, image/jpeg, image/png, text/*, image/*, */*',
    'Accept-Language': 'en-us',
    'Accept-Charset' : 'utf-8',
    #'Accept-Charset' : 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
    'Accept-Encoding': 'utf-8',
    'Keep-Alive': '300',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0'
}

keys = ['subtitle',
        'price_retail',
        'brand',
        'price_gross',
        'source',
        'image3',
        'image2',
        'image1',
        'mass (kg)',
        'type',
        'price',
        'unit',
        'html',
        'title',
        'done'
       ]

data = 'data.csv'
final = data.split('.')[0] + '_updated.' + data.split('.')[1]

def getFile():
    final = data.split('.')
    final = final[0] + '_updated.' + final[1]
    if os.path.isfile('./' + final):
        return final
    else:
        return data

def getKeys():
    if os.path.isfile('./' + final):
        f = open(final, "r")
        reader = csv.reader(f)
        k = reader.next()
        return set(k)
    else:
        return set(keys)


