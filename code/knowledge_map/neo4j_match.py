from py2neo import Node, Relationship, Graph, NodeMatcher, RelationshipMatcher

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
