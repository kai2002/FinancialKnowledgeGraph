import csv
import urllib
from urllib import request
from bs4 import BeautifulSoup


def get_html_by_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Cookie': 'Hm_lvt_cb1b8b99a89c43761f616e8565c9107f=1525743573; __jsluid=4a39397901657f14ea83f429afe2b980; vjuids=11155ae0c4.15fb58131a6.0.9bce6acd413b6; hxck_webdev1_general=stocklist=000001_2; UM_distinctid=1634353d8e7627-0fd45d778c6bef-24414032-100200-1634353d8e8e6; CNZZDATA1261865322=532870799-1525839818-%7C1525839818; HexunTrack=SID=20180509131558013a67c883f99ce4dd08db7ca02eea8559b&CITY=44&TOWN=0'}
    req = urllib.request.Request(url=url, headers=headers)
    html = urllib.request.urlopen(req)
    return html


if __name__ == '__main__':
    data = []
    with open('../../Data/add_code.csv', 'r', newline='') as fin:
        csv_reader = csv.reader(fin)
        for line in csv_reader:
            data.append(line[0][0:6])
    company = []
    for id in data:
        url = 'http://stockdata.stock.hexun.com/gszl/s{0}.shtml'.format(id)
        html = get_html_by_url(url)
        soup = BeautifulSoup(html.read(), 'html.parser', from_encoding='utf-8')  # 乱码时设置：fromEncoding='gb18030'
        trs = soup.find('div', class_='xinx_l marr10').find('tbody').find_all('tr')
        mess = {}
        for tr in trs:
            tds = tr.find_all('td')
            key = tds[0].get_text().replace('\n', '').replace('\t', '').replace('\r', '')
            value = tds[1].get_text().replace('\n', '').replace('\t', '').replace('\r', '')
            mess[key] = value
        # print(mess)
        with open('../../Data/add_company.csv', 'a', encoding='utf-8', newline='') as fout:
            csvwriter = csv.writer(fout, delimiter=';')
            list = []
            try:
                dict = mess
                list.append(dict['股票代码'])
                list.append(dict['公司简称'])
                list.append(dict['公司全称'])
                list.append(dict['公司英文名称'])
                list.append(dict['成立日期'])
                list.append(dict['所属地域'])
                list.append(dict['曾用名'])
                list.append(dict['法定代表人'])
                list.append(dict['独立董事'])
                list.append(dict['会计师事务所'])
                list.append(dict['证券事务代表'])
                list.append(dict['咨询服务机构'])
                list.append(dict['所属概念'])
                list.append(dict['所属行业'])
                if list[0] == '':
                    print(id)
                else:
                    csvwriter.writerow(list)
            except:
                print(id)
