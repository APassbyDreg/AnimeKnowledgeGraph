import json
from lxml import etree
from bangumi import get_subject,is_valid
import requests
"""
    输入一个有效数据，返回爬取的数据,以字典方式存储
    input1:(int)num
    input2:(str)header_agent
    output:(dict)dic
"""
def crawl(num, header):
    subject = get_subject(num)
    """
    with open('./test.json','w', encoding='utf-8') as f:
        json.dump(subject, f, ensure_ascii=False)
    if is_valid(subject):
        print(subject)
        print(subject['rating']['total'])
        print(subject['collection']['collect'])
        print(subject['crt'])
        print(subject['staff'])
    """
    headers = {
        'User-Agent':header
    }
    if is_valid(subject):
        url = subject['url']
        response =  requests.get(url=url,params=None,headers=headers)
        # print(response.encoding)
        # response.encoding = 'gbk'
        if response.encoding == 'ISO-8859-1':
            encodings = requests.utils.get_encodings_from_content(response.text)
            if encodings:
                encoding = encodings[0]
            else:
                encoding = response.apparent_encoding
        else:
            encoding = response.encoding
        encode_content = response.content.decode(encoding,'replace').encode('utf-8','replace').decode('utf-8')
        tree = etree.HTML(encode_content)
        dic = dict()
        for i in range(1,30):
            attribute = tree.xpath('//body//div[@class="infobox"]/ul/li[{}]/span/text()'.format(i))
            value_a = tree.xpath('//body//div[@class="infobox"]/ul/li[{}]/a/text()'.format(i))
            value_b = tree.xpath('//body//div[@class="infobox"]/ul/li[{}]/text()'.format(i))
            if attribute == []:
                break
            attribute = str(attribute)
            attribute = attribute.replace("[",'')
            attribute = attribute.replace("]",'')
            attribute = attribute.replace(" ",'')
            attribute = attribute.replace("'",'')
            attribute = attribute.replace(":",'')
            if value_a == []:
                dic[str(attribute)] = value_b
            else:
                dic[str(attribute)] = value_a
    #print(dic)
    return dic

def get_final_json(json_path, header):
    with open(json_path, 'r', encoding="UTF-8") as fp:
        json_list = json.load(fp)
    i = 0
    crawl_result = {}
    for index in json_list:
        try:
            subject = get_subject(index)
            _valid = is_valid(subject)
        except:
            continue
        if _valid is True:
            dic = crawl(index, header)
            crawl_result[i] = dic
        i += 1
        if i % 10 == 0:
            print("turn {} finished".format(i))
        if i > 5000:
            break
    with open("./data/crawl_result.json", 'w', encoding="UTF-8") as fp:
        json.dump(crawl_result, fp, ensure_ascii=False)