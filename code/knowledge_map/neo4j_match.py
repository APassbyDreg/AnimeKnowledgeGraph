from py2neo import Node, Relationship, Graph, NodeMatcher, RelationshipMatcher
import jieba.posseg as pseg
import jieba
import random
import json

#my_password = ''
#graph = Graph('http://localhost:7474', username='neo4j', password=my_password)

def shortest_path_match(graph, name_1, label_1, relation, label_2):
    """
    用于查找单个关系
    for example: p = shortest_path_match(graph, "悠木碧", "staff", "配音", "charactor")
    """
    match_str = "MATCH (p:" + label_1 + \
                "{name: '" + name_1 + "' })-[" + relation + "]-(q:" + label_2 + ") RETURN q.name"
    #print(match_str)
    p1 = list(graph.run(match_str))
    record_list = []
    for point in p1:
        record_list.append(point['q.name'])
    if len(record_list) > 15:
        record_list = random.sample(record_list, 15)
    return '、'.join(list(set(record_list)))

def recommend_path(graph, name_1, label_1, relation_1, label_2, relation_2, label_3):
    """
    这部分用于推荐
    for example: p = recommend_path(graph, "恋如雨止", "bangumi", "出场", "character", "声优", "staff")
    """
    match_str = "MATCH (p:" + label_1 + \
                "{name: '" + name_1 + "' })-[r:" + relation_1 + "]-(q:" + label_2 + \
                ")-[t:" + relation_2 + "]-(w:" + label_3 + ") RETURN w.name"
    #print(match_str)
    p1 = list(graph.run(match_str))
    record_list = []
    for point in p1:
        record_list.append(point['w.name'])
    if len(record_list) > 15:
        record_list = random.sample(record_list, 15)
    return '、'.join(list(set(record_list)))

def special_deal_for_actor(graph, name_1, label_1, label_2):
    match_str = "MATCH (p:" + label_1 + \
                "{name: '" + name_1 + "' })-[r:出场]-(q:character)-[t:声优]-(w:" \
                + label_2 + ")-[v:参与配音]-(s:" + label_1 + "{name: '" + name_1 + "' }) RETURN w.name"
    # print(match_str)
    p1 = list(graph.run(match_str))
    record_list = []
    for point in p1:
        record_list.append(point['w.name'])
    if len(record_list) > 15:
        record_list = random.sample(record_list, 15)
    return '、'.join(list(set(record_list)))

def get_comic_list(json_path):
    """
    获得全部comic的名字以及其中声优和charactor的名字
    """
    with open(json_path, 'r', encoding="UTF-8") as fp:
        dict = json.load(fp)
    comic_list = []
    actor_list = []
    staff_list = []
    charactor_list = []
    bangumi_inform_json = {}
    for key, value in dict.items():
        comic_list.append(value["番剧"])
        for charactor_inform in value["角色"]:
            if charactor_inform["name"] not in charactor_list:
                charactor_list.append(charactor_inform["name"])
            for actor in charactor_inform["actors"]:
                if actor not in actor_list:
                    actor_list.append(actor)
        for staff_inform in value["工作人员"]:
            if staff_inform['name'] not in actor_list:
                staff_list.append(staff_inform['name'])
    bangumi_inform_json["bangumi_list"] = comic_list
    bangumi_inform_json["staff_list"] = staff_list
    bangumi_inform_json["actor_list"] = actor_list
    bangumi_inform_json["character_list"] = charactor_list
    with open("./data/bangumi_inform_collect.json", 'w', encoding="UTF-8") as fp:
        json.dump(bangumi_inform_json, fp ,ensure_ascii=False)
    #return comic_list, staff_list, actor_list, charactor_list

# def Q_and_A(graph):
#     flag_list = ['番剧', '角色', '配音', '演员', '推荐', '配音演员', '登场人物', "喜欢",
#                  "番", "声优", "音乐", "剧情", "画风"]
#     special_list = []
#     comic_list, staff_list, actor_list, charactor_list = get_comic_list("./data/bangumi_simplify.json")
#     special_list.extend(comic_list)
#     special_list.extend(actor_list)
#     special_list.extend(charactor_list)
#     special_list.extend(staff_list)
#     special_list.extend(flag_list)
#     for word in special_list:
#         jieba.suggest_freq(word, True)
#     while True:
#         question = input("年轻的孩子，用你的问题换取宅之力吧！")
#         if question == "没什么想问的了":
#             break
#         words = pseg.cut(question)
#         sentence_special_list = []
#         sentence_flag_list = []
#         sentence_comic_list = []
#         sentence_actor_list = []
#         sentence_charactor_list = []
#         for word, flag in words:
#             #print(word)
#             if word in special_list:
#                 sentence_special_list.append(word)
#             if word in comic_list:
#                 sentence_comic_list.append(word)
#             if word in actor_list:
#                 sentence_actor_list.append(word)
#             if word in charactor_list:
#                 sentence_charactor_list.append(word)
#             elif word in flag_list:
#                 sentence_flag_list.append(word)
#         if len(sentence_special_list) == 0:
#             print("抱歉，不知道您具体指什么")
#             continue
#         if len(sentence_flag_list) == 0:
#             print("您在说什么？？")
#             continue
#         for special_word in sentence_special_list:
#             if special_word in comic_list:
#                 if "配音演员" in sentence_flag_list or "声优" in sentence_flag_list or \
#                             "配音" in sentence_flag_list and len(sentence_charactor_list) == 0 and \
#                         len(sentence_actor_list) == 0:
#                     return_list = recommend_path(graph, special_word,
#                                                      'bangumi', '出场', 'character', '声优', 'staff')
#                     #return_list = shortest_path_match(graph, special_word, "bangumi", "参与配音", "staff")
#                     print("对于"+special_word+"您可能想了解的配音演员有", return_list)
#
#                 if "角色" in sentence_flag_list or "登场人物" in sentence_flag_list and \
#                         len(sentence_charactor_list) == 0:
#                     return_list = shortest_path_match(graph, special_word,
#                                                         'bangumi', '出场', 'character')
#                     print(special_word + "的主要人物包括了", return_list)
#
#                 if "音乐" in sentence_flag_list and "喜欢" in sentence_flag_list or "推荐" in sentence_flag_list:
#                     return_list = recommend_path(graph, special_word, 'bangumi',
#                                                  '参与音乐制作', 'staff', '参与音乐制作', 'bangumi')
#                     if len(return_list) > 10:
#                         return_list = random.sample(return_list, 10)
#                     print("推测您可能喜欢以下番剧", return_list)
#
#                 if "画风" in sentence_flag_list and "喜欢" in sentence_flag_list or "推荐" in sentence_flag_list:
#                     return_list = recommend_path(graph, special_word, 'bangumi',
#                                                  '参与原画制作', 'staff', '参与原画制作', 'bangumi')
#                     if len(return_list) > 10:
#                         return_list = random.sample(return_list, 10)
#                     print("推测您可能喜欢以下番剧", return_list)
#
#                 if "剧情" in sentence_flag_list and "喜欢" in sentence_flag_list or "推荐" in sentence_flag_list:
#                     return_list = recommend_path(graph, special_word, 'bangumi',
#                                                  '参与内容制作', 'staff', '参与内容制作', 'bangumi')
#                     if len(return_list) > 10:
#                         return_list = random.sample(return_list, 10)
#                     print("推测您可能喜欢以下番剧", return_list)
#
#             elif special_word in charactor_list:
#                 if "配音演员" in sentence_flag_list or "声优" in sentence_flag_list or \
#                         "配音" in sentence_flag_list:
#                     return_list = shortest_path_match(graph, special_word,
#                                                       'character', '声优', 'staff')
#                     #print(special_word + "的配音演员是", return_list)
#                     return_list = list(set(return_list))
#                     print(special_word + "的配音演员是", return_list)
#                 if "番剧" in sentence_flag_list or "番" in sentence_flag_list:
#                     return_list = shortest_path_match(graph, special_word,
#                                                       'character', '出场', 'bangumi')
#                     print(special_word + "出场于", return_list)
#             elif special_word in actor_list:
#                 if "配音" in sentence_flag_list and '角色' in sentence_flag_list:
#                     return_list = shortest_path_match(graph, special_word,
#                                                       'staff', '声优', 'character')
#                     if len(return_list) > 10:
#                         return_list = random.sample(return_list, 10)
#                     print(special_word + "配音了", return_list)
#                 if "番剧" in sentence_flag_list or "番" in sentence_flag_list:
#                     return_list = shortest_path_match(graph, special_word,
#                                                       'staff', '参与配音', 'bangumi')
#                     print(special_word + "参与配音", return_list)

def Q_and_A_new(graph, question):
    flag_list = ['番剧', '角色', '配音', '演员', '推荐', '配音演员', '登场人物', "喜欢",
                 "番", "声优", "音乐", "剧情", "画风"]
    special_list = []
    with open("./data/bangumi_inform_collect.json", "r", encoding="UTF-8") as fp:
        bangumi_loader = json.load(fp)
    comic_list = bangumi_loader["bangumi_list"]
    staff_list = bangumi_loader["staff_list"]
    actor_list = bangumi_loader["actor_list"]
    charactor_list = bangumi_loader["character_list"]
    special_list.extend(comic_list)
    special_list.extend(actor_list)
    special_list.extend(charactor_list)
    special_list.extend(staff_list)
    special_list.extend(flag_list)
    for word in special_list:
        jieba.suggest_freq(word, True)
    words = pseg.cut(question)
    sentence_special_list = []
    sentence_flag_list = []
    sentence_comic_list = []
    sentence_actor_list = []
    sentence_charactor_list = []
    for word, flag in words:
        # print(word)
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
        return "抱歉，不知道您具体指什么"
    if len(sentence_flag_list) == 0:
        return "您在说什么？？"
    for special_word in sentence_special_list:
        if special_word in comic_list:
            if "配音演员" in sentence_flag_list or "声优" in sentence_flag_list or \
                    "配音" in sentence_flag_list and len(sentence_charactor_list) == 0 and \
                    len(sentence_actor_list) == 0:
                # return_list = recommend_path(graph, special_word,
                #                              'bangumi', '出场', 'character', '声优', 'staff')
                return_list = special_deal_for_actor(graph, special_word, "bangumi", "staff")
                # return_list = shortest_path_match(graph, special_word, "bangumi", "参与配音", "staff")
                return "对于" + special_word + "您可能想了解的配音演员有:" + str(return_list)

            if "角色" in sentence_flag_list or "登场人物" in sentence_flag_list and \
                    len(sentence_charactor_list) == 0:
                return_list = shortest_path_match(graph, special_word,
                                                  'bangumi', '出场', 'character')
                return special_word + "的主要人物包括了:" + str(return_list)

            if "音乐" in sentence_flag_list and ("喜欢" in sentence_flag_list or "推荐" in sentence_flag_list):
                return_list = recommend_path(graph, special_word, 'bangumi',
                                             '参与音乐制作', 'staff', '参与音乐制作', 'bangumi')
                # if len(return_list) > 10:
                #     return_list = random.sample(return_list, 10)
                return "推测您可能喜欢以下番剧:" + str(return_list)

            if "画风" in sentence_flag_list and ("喜欢" in sentence_flag_list or "推荐" in sentence_flag_list):
                return_list = recommend_path(graph, special_word, 'bangumi',
                                             '参与原画制作', 'staff', '参与原画制作', 'bangumi')
                # if len(return_list) > 10:
                #     return_list = random.sample(return_list, 10)
                return "推测您可能喜欢以下番剧:" + str(return_list)

            if "剧情" in sentence_flag_list and ("喜欢" in sentence_flag_list or "推荐" in sentence_flag_list):
                return_list = recommend_path(graph, special_word, 'bangumi',
                                             '参与内容制作', 'staff', '参与内容制作', 'bangumi')
                # if len(return_list) > 10:
                #     return_list = random.sample(return_list, 10)
                return "推测您可能喜欢以下番剧:" + str(return_list)

        if special_word in charactor_list:
            if "配音演员" in sentence_flag_list or "声优" in sentence_flag_list or \
                    "配音" in sentence_flag_list:
                return_list = shortest_path_match(graph, special_word,
                                                  'character', '声优', 'staff')
                # print(special_word + "的配音演员是", return_list)
                # return_list = list(set(return_list))
                return special_word + "的配音演员有:" + str(return_list)
            if "番剧" in sentence_flag_list or "番" in sentence_flag_list:
                return_list = shortest_path_match(graph, special_word,
                                                  'character', '出场', 'bangumi')
                return special_word + "出场于" + str(return_list)
                
        if special_word in actor_list:
            if "配音" in sentence_flag_list and '角色' in sentence_flag_list:
                return_list = shortest_path_match(graph, special_word,
                                                  'staff', '声优', 'character')
                # if len(return_list) > 10:
                #     return_list = random.sample(return_list, 10)
                return special_word + "配音了这些角色:" + str(return_list)
            if "番剧" in sentence_flag_list or "番" in sentence_flag_list:
                return_list = shortest_path_match(graph, special_word,
                                                  'staff', '参与配音', 'bangumi')
                return special_word + "参与配音的番剧有:" + str(return_list)

