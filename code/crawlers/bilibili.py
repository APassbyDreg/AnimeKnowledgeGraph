from bilibili_api import bangumi
from bilibili_api import video

import requests

import time
import json


IGNORE_TITLE = {"僅限", "地區"}


def get_bangumi_index():
    """
        获取番剧基础 ID 列表
    """
    bangumi_list_url = "https://api.bilibili.com/pgc/season/index/result?season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&year=-1&style_id=-1&order=3&st=1&sort=0&season_type=1&pagesize=50&type=1&page={}"
    total_list = {}
    for p in range(1, 65):
        url = bangumi_list_url.format(p)
        response = requests.get(url)
        if response:
            data = json.loads(response.text)
            # go through each page
            for b in data['data']['list']:
                # check valid
                ignore = False
                for ig in IGNORE_TITLE:
                    if ig in b['title']:
                        ignore = True
                        break
                # store data 
                if not ignore:
                    total_list[b['title']] = {'md': b['media_id'], 'ssid': b['season_id']}
        print("scaned {:02d} pages, get {:04d} bangumies".format(p, len(total_list)))
        time.sleep(0.2)
    return total_list


if __name__ == "__main__":
    b = get_bangumi_index()
    f = open('data/bili_index.json', 'w', encoding='utf-8')
    json.dump(b, f, ensure_ascii=False)
