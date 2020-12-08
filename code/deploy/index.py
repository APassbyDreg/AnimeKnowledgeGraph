try:
    from py2neo import Node, Relationship, Graph, NodeMatcher, RelationshipMatcher
    import jieba
except:
    from .packages.py2neo import Node, Relationship, Graph, NodeMatcher, RelationshipMatcher
    from .packages import jieba

import logging
from cgi import parse_qs, escape


graph = Graph('http://121.4.39.249:7474', username='neo4j', password='neo4jadmin')

# To enable the initializer feature (https://help.aliyun.com/document_detail/158208.html)
# please implement the initializer function as below：
# def initializer(context):
#    logger = logging.getLogger()  
#    logger.info('initializing')

def handler(environ, start_response):
    # load params
    params = parse_qs(environ['QUERY_STRING'])
    
    # QA - main

    # response
    status = '200 OK'
    response_headers = [('Content-type', 'json')]
    start_response(status, response_headers)
    res = params
    return [str.encode(str(res))]