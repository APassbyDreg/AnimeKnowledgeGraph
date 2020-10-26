import requests

import json


def is_valid(subject):
    """
        根据预定义规则过滤信息不足的主题
        input:  subject (dict)
        output: validation (boolean)    
    """
    RATING_THRES = 5
    COLLECT_THRES = 10
    # process
    valid = True
    valid &= subject['rating']['total'] > RATING_THRES
    valid &= subject['collection']['collect'] > COLLECT_THRES
    valid &= subject['crt'] is not None
    valid &= subject['staff'] is not None
    return valid



def get_subject(subject_id):
    """
        根据主题 ID 获取 bangumi 信息
        input:  subject id (int)
        output: subject (dict)
    """
    url = "https://cdn.jsdelivr.net/npm/anime-sachedule-search-data@0.1.106/dist/subject/{}.json".format(subject_id)
    res = requests.get(url)
    
    if res:
        data = json.loads(res.text)
    else:
        raise ValueError("invalid subject id")

    return data
