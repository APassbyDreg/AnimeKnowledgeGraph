from py2neo import Node, Relationship, Graph, NodeMatcher, RelationshipMatcher
import jieba.posseg as pseg
import jieba
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
    print(match_str)
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
    print(match_str)
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

def Q_and_A():
    special_list = []
    comic_list, actor_list, charactor_list = get_comic_list("./data/bangumi_simplify.json")
    special_list.extend(comic_list)
    special_list.extend(actor_list)
    special_list.extend(charactor_list)
    for word in special_list:
        jieba.suggest_freq(word, True)
    question = input("年轻的孩子，用你的问题换取宅之力吧！")

    words = pseg.cut(question)
    for word, flag in words:
        print(word)
        print(flag)

