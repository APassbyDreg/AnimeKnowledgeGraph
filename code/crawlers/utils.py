import json
from lxml import etree
from bangumi import get_subject, is_valid, get_person
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
            if _valid is True:
                dic = crawl(index, header)
                crawl_result[i] = dic
        except:
            continue
        i += 1
        if i % 10 == 0:
            print("turn {} finished".format(i))
        if i > 5000:
            break
        with open("./data/crawl_result.json", 'w', encoding="UTF-8") as fp:
            json.dump(crawl_result, fp, ensure_ascii=False)

def simplify_data(json_path):
    with open(json_path, 'r', encoding="UTF-8") as fp:
        loader = json.load(fp)
    simplify_dic = {}
    i = 0
    actor_cn_name = {}
    for k, v in loader.items():
        comic_info = {}
        comic_info["番剧"] = v["name_cn"]
        comic_info["角色"] = []
        comic_info["工作人员"] = []
        for in_part in v['crt']:
            new_charactor = {}
            if in_part['name_cn'] == '':
                new_charactor['name'] = in_part['name']
            else:
                new_charactor['name'] = in_part['name_cn']
            new_charactor['actors'] = []
            try:
                for actor in in_part['actors']:
                    new_num = actor['id']
                    new_num = str(new_num)
                    if new_num not in actor_cn_name.keys():
                        actor_inform = get_person(new_num)
                        actor_cn_name[new_num] = actor_inform["nameCn"]

                    if actor_cn_name[new_num] != "":
                        new_charactor['actors'].append(actor_cn_name[new_num])
                    elif actor_cn_name[new_num] == "":
                        new_charactor['actors'].append(actor['name  '])
                    print("finish an actor")
                comic_info['角色'].append(new_charactor)
            except:
                comic_info['角色'].append(new_charactor)
                continue

        for in_part in v["staff"]:
            new_worker = {}
            if in_part["name_cn"] == "":
                new_worker['name'] = in_part["name"]
            else:
                new_worker['name'] = in_part["name_cn"]
            try:
                new_worker['job'] = in_part['jobs']
            except:
                new_worker['job'] = []
            comic_info["工作人员"].append(new_worker)
        simplify_dic[k] = comic_info
        i += 1
        if i % 1 == 0:
            print("turn {} is finished".format(i))
    with open("./data/bangumi_simplify.json", 'w', encoding="UTF-8") as fp:
        json.dump(simplify_dic, fp, ensure_ascii=False)


