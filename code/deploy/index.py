from packages import py2neo
from packages import jieba

import logging
from cgi import parse_qs, escape

HELLO_WORLD = b'Hello world!\n'

# To enable the initializer feature (https://help.aliyun.com/document_detail/158208.html)
# please implement the initializer function as below：
# def initializer(context):
#    logger = logging.getLogger()  
#    logger.info('initializing')

def handler(environ, start_response):
    context = environ['fc.context']
    request_uri = environ['fc.request_uri']
    params = parse_qs(environ['QUERY_STRING'])
    # do something here
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return [str.encode(str(params))]