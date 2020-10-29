import requests

import json
import time


def is_valid(subject):
    """
        根据预定义规则过滤信息不足的主题
        input:  
            - subject (dict) 参考 #APIS/data-sample/Bangumi/subject{{subject_id}}.json
        output: 
            - validation (boolean)    
    """
    try:
        RATING_THRES = 5
        COLLECT_THRES = 5
        # process
        valid = True
        valid &= subject['rating']['total'] > RATING_THRES
        valid &= subject['collection']['collect'] > COLLECT_THRES
        valid &= subject['crt'] is not None
        valid &= subject['staff'] is not None
        return valid
    except:
        return False



def get_subject(subject_id):
    """
        根据主题 ID 获取 bangumi 信息
        input:  
            - subject id (int / str)
        output: 
            - subject (dict) 参考 #APIS/data-sample/Bangumi/subject{{subject_id}}.json
    """
    url = "https://cdn.jsdelivr.net/npm/anime-sachedule-search-data@0.1.106/dist/subject/{}.json".format(subject_id)
    res = requests.get(url)
    if res:
        data = json.loads(res.text)
    else:
        raise ValueError("invalid subject id")
    return data


def crawl_all(index, dest='data/bangumi_all.json'):
    """
        根据给定的 anime_index 爬取所有来自 bangumi 的信息，并存储到 dest 表示的文件中
        input:
            - index (dict) 参考 data/anime_index@{{TIME}}.json
            - dest (str) 文件地址
        output:
            - records (dict) { subject_id(str) => subject(dict) }
    """
    waitlist = []

    for item in index['items']:
        sites = item.get('sites', {})
        bangumi_subject_id = None
        for s in sites:
            if s['site'] == 'bangumi':
                bangumi_subject_id = s['id']
        if bangumi_subject_id is not None:
            waitlist.append(bangumi_subject_id)
    print("loaded {} subjects to waitlist".format(len(waitlist)))

    FAILED_THRES = 3
    failed_times = {}
    n_repeat = len(waitlist) * 2
    run_times = 0
    records = {}
    while len(waitlist) > 0 and n_repeat > run_times:
        run_times += 1
        subject_id = waitlist.pop(0)
        try:
            subject = get_subject(subject_id)
            if is_valid(subject):
                records[subject_id] = subject
                status = 'valid'
            else:
                status = 'invalid'
        except:
            status = 'failed'
            failed_times[subject_id] = failed_times.get(subject_id, 0) + 1
            if failed_times[subject_id] < FAILED_THRES:
                time.sleep(1)
                waitlist.append(subject_id)
        print("try {} {}: {} crawled, {} remaining".format(run_times, status, len(records), len(waitlist)))
    
    fp = open(dest, 'w', encoding='utf-8')
    json.dump(records, fp, ensure_ascii=False)

    return records