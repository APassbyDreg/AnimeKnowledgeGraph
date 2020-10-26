from py2neo import Node, Relationship, Graph, NodeMatcher, RelationshipMatcher
import csv
import json

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
            #label2 = label_list[j]
            #attrs2 = {"name": content[i][j]}
                CreateNode(m_graph, label1, attrs1)
                CreateNode(m_graph, label2, attrs2)
                reValue = CreateRelationship(m_graph, label1,
                                attrs1, label2, attrs2, label_list[j])
        print("finish line {}", i)


def create_from_json(m_graph, json_path):
    return None


# my_password = ''                # do not upload your password
# graph = Graph('http://localhost:7474', username='neo4j', password=my_password)
# 打开数据库
# create_from_csv(graph, './jojo_test.csv')
