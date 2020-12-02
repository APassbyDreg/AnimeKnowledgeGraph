from py2neo import Node, Relationship, Graph, NodeMatcher, RelationshipMatcher
import jieba.posseg as pseg
import jieba
import random
import json

#my_password = ''
#graph = Graph('http://localhost:7474', username='neo4j', password=my_password)

def shortest_path_match(graph, name_1, attrib_1, attrib_2):
    """
    用于查找单个关系
    for example: p = shortest_path_match(graph, "悠木碧", "actor", "charactor")
    """
    match_str = "MATCH (p:" + attrib_1 + \
                "{name: '" + name_1 + "' })-[r]-(q:" + attrib_2 + ") RETURN q"
    #print(match_str)
    p1 = graph.run(match_str)
    p1 = list(p1)
    return p1

def recommend_path(graph, name_1, attrib_1, attrib_2, attrib_3):
    """
    这部分用于推荐
    for example: p = recommend_path(graph, "恋如雨止", "comic", "actor", "comic")
    """
    match_str = "MATCH (p:" + attrib_1 + \
                "{name: '" + name_1 + "' })-[r]-(q:" + attrib_2 + \
                ")-[t]-(w:" + attrib_3 + ") RETURN w"
    #print(match_str)
    p1 = graph.run(match_str)
    p1 = list(p1)
    return p1

def get_comic_list(json_path):
    """
    获得全部comic的名字以及其中声优和charactor的名字
    """
    with open(json_path, 'r', encoding="UTF-8") as fp:
        dict = json.load(fp)
    comic_list = []
    actor_list = []
    charactor_list = []
    for key, value in dict.items():
        comic_list.append(value["番剧"])
        for charactor_inform in value["角色"]:
            if charactor_inform["name"] not in charactor_list:
                charactor_list.append(charactor_inform["name"])
            for actor in charactor_inform["actors"]:
                if actor not in actor_list:
                    actor_list.append(actor)
    return comic_list, actor_list, charactor_list

def Q_and_A(graph):
    flag_list = ['番剧', '角色', '配音', '演员', '推荐', '配音演员', '登场人物', "喜欢"]
    special_list = []
    comic_list, actor_list, charactor_list = get_comic_list("./data/bangumi_simplify.json")
    special_list.extend(comic_list)
    special_list.extend(actor_list)
    special_list.extend(charactor_list)
    special_list.extend(flag_list)
    for word in special_list:
        jieba.suggest_freq(word, True)
    while True:
        question = input("年轻的孩子，用你的问题换取宅之力吧！")
        if question == "没什么想问的了":
            break
        words = pseg.cut(question)
        sentence_special_list = []
        sentence_flag_list = []
        sentence_comic_list = []
        sentence_actor_list = []
        sentence_charactor_list = []
        for word, flag in words:
            #print(word)
            if word in special_list:
                sentence_special_list.append(word)
            if word in comic_list:
                sentence_comic_list.append(word)
            if word in actor_list:
                sentence_actor_list.append(word)
            if word in charactor_list:
                sentence_charactor_list.append(word)
            elif word in flag_list:
                sentence_flag_list.append(word)
        if len(sentence_special_list) == 0:
            print("抱歉，不知道您具体指什么")
            continue
        if len(sentence_flag_list) == 0:
            print("您在说什么？？")
            continue
        for special_word in sentence_special_list:
            if special_word in comic_list:
                if "配音演员" in sentence_flag_list or "声优" in sentence_flag_list or \
                            "配音" in sentence_flag_list and len(sentence_actor_list) == 0:
                    return_list = shortest_path_match(graph, special_word,
                                                        'comic', 'actor')
                    print("您想了解的配音演员有", return_list)
                    if "喜欢" in sentence_flag_list and "推荐" in sentence_flag_list:
                        return_list = recommend_path(graph, special_word, 'comic', 'actor', 'comic')
                        if len(return_list) > 10:
                            return_list = random.sample(return_list, 10)
                        print("推测您可能喜欢以下番剧", return_list)
                if "角色" in sentence_flag_list or "登场人物" in sentence_flag_list:
                    return_list = shortest_path_match(graph, special_word,
                                                        'comic', 'charactor')
                    print(special_word + "的主要人物包括了", return_list)


