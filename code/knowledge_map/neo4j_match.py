from py2neo import Node, Relationship, Graph, NodeMatcher, RelationshipMatcher

#my_password = ''
#graph = Graph('http://localhost:7474', username='neo4j', password=my_password)

def shortest_path_match(graph, name_1, attrib_1, name_2, attrib_2):
    match_str = "MATCH (p:" + attrib_1 + \
                "{name: '" + name_1 + "' })-[r]-(q:" + attrib_2 + ") RETURN q"
    print(match_str)
    p1 = graph.run(match_str)
    p1 = list(p1)
    return p1
