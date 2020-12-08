from py2neo import Node, Relationship, Graph, NodeMatcher, RelationshipMatcher
import csv
import json
from tqdm import tqdm

def ClearDB(graph):
    graph.run("MATCH (n)")
    graph.run("DETACH DELETE n")

def CreateNode(m_graph, m_label, m_attrs):
    matcher = NodeMatcher(m_graph)
    re_value = matcher.match(m_label, **m_attrs).first()
    if re_value is None:
        m_node = Node(m_label, **m_attrs)
        n = m_graph.create(m_node)
        return n
    return None

def MatchNode(m_graph, m_label, m_attrs):
    matcher = NodeMatcher(m_graph)
    re_value = matcher.match(m_label, **m_attrs).first()
    return re_value

def CreateRelationship(m_graph, m_label1, m_attrs1,
                       m_label2, m_attrs2, m_relation):
    re_value1 = MatchNode(m_graph, m_label1, m_attrs1)
    re_value2 = MatchNode(m_graph, m_label2, m_attrs2)
    if re_value1 is None or re_value2 is None:
        return False
    m_r = Relationship(re_value1, m_relation, re_value2)
    n = m_graph.create(m_r)
    return n

def create_from_csv(m_graph, csv_path):
    csv_file = csv.reader(open(csv_path, 'r', encoding='UTF-8'))
    content = []
    for line in csv_file:
        content.append(line)
    label_list = content[0]
    for i in range(1, len(content)):
        for j in range(1, len(label_list)):
            label1 = label_list[0]
            attrs1 = {"name": content[i][0]}
            ele_list = content[i][j]
            ele_list = ele_list.strip('[')
            ele_list = ele_list.strip(']')
            ele_list = ele_list.split(", ")
            for element in ele_list:
                label2 = label_list[j]
                attrs2 = {"name": element}
                CreateNode(m_graph, label1, attrs1)
                CreateNode(m_graph, label2, attrs2)
                reValue = CreateRelationship(m_graph, label1,
                                attrs1, label2, attrs2, label_list[j])
        print("finish line {}", i)


def create_from_json(m_graph, json_path):
    ClearDB(m_graph)
    with open("./edge_classes.json", 'r', encoding="UTF-8") as fp:
        job_class_loader = json.load(fp)
        job_class_loader = job_class_loader["staff"]["bangumi"]
    with open(json_path, 'r', encoding="UTF-8") as fp:
        loader = json.load(fp)
    for k, v in tqdm(loader.items()):
        label_comic = "bangumi"
        attrs_comic = {"name": v["番剧"]}
        CreateNode(m_graph, label_comic, attrs_comic)
        for crt in v["角色"]:
            label_charactor = "character"
            attrs_charactor = {"name": crt["name"], "source": v["番剧"]}
            CreateNode(m_graph, label_charactor, attrs_charactor)
            ch_com_re = "出场"
            res = CreateRelationship(m_graph, label_charactor, attrs_charactor,
                               label_comic, attrs_comic, ch_com_re)
            label_actor = "staff"
            for actor in crt["actors"]:
                attrs_actor = {"name": actor}
                CreateNode(m_graph, label_actor, attrs_actor)
                at_ch_re = "声优"
                pre_com_re = "参与配音"
                res = CreateRelationship(m_graph, label_actor, attrs_actor,
                                   label_charactor, attrs_charactor, at_ch_re)
                res = CreateRelationship(m_graph, label_actor, attrs_actor,
                                   label_comic, attrs_comic, pre_com_re)

        for staff in v["工作人员"]:
            label_staff = "staff"
            attrs_staff = {"name": staff['name']}
            CreateNode(m_graph, label_staff, attrs_staff)
            job_list = staff['job']
            for job in job_list:
                for key, value in job_class_loader.items():
                    if job in value:
                        pre_com_re = key
                res = CreateRelationship(m_graph, label_staff, attrs_staff,
                               label_comic, attrs_comic, pre_com_re)




graph = Graph('http://121.4.39.249:7474', username='neo4j', password='neo4jadmin')
# 打开数据库
# create_from_csv(graph, './jojo_test.csv')
create_from_json(graph, './data/bangumi_simplify.json')
