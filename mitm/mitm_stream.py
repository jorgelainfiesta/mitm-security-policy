#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libmproxy.protocol.http import decoded
from libmproxy.flow import FlowWriter
from urllib import unquote
from urllib import quote
from datetime import datetime

import requests
import json
import sys  

def start(context, argv):
    if len(argv) != 2:
        raise ValueError('Usage: -s "mitm_stream.oy endpoint"')
    context.endpoint = argv[1]
    reload(sys)  
    sys.setdefaultencoding('utf8')
    
'''
Reads responses from MITM proxy and maps relevant info to a dict.
Then calls the router to redirect HTTPResponse dict.
'''
def response(context, flow):
    #Process request
    requestAttrs = ["method", "scheme", "host", "port", "path", "httpversion", "headers", "content", "form_in", "timestamp_start", "timestamp_end"]
    
    requestDict = {}
    
    requestDict['date-sent'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #Build HTTPRequest dict with decoded data
    with decoded(flow.request):
        for attr in requestAttrs:
            try:
                if attr == "content":
#                    unocnt = unicode(flow.request.content, errors="xmlcharrefreplace", encoding="utf8")
                    requestDict[attr] = flow.request.content
                else:
                    requestDict[attr] = str(getattr(flow.request, attr))
            except Exception, e:
                requestDict[attr] = str(e)
    
    #Process response
    responseAttrs = ["httpversion", "msg", "headers", "content", "timestamp_start", "timestamp_end"]
    
    responseDict = {}
    
    responseDict['date-received'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #Build HTTPResponse dict with decoded data
    with decoded(flow.response):
        for attr in responseAttrs:
            try:
                if attr == "content":
                    responseDict[attr] = flow.response.content
                else:
                    responseDict[attr] = str(getattr(flow.response, attr))
            except Exception, e:
                responseDict[attr] = str(e)
                
    #Redirect messages to appropaite destinations
    redirect(requestDict, responseDict, context.endpoint)
    
'''
This method receives an HTTPRequest dict and a HTTPResponse dict, reads its headers and redirects it to the corresponding processor. 
'''
def redirect(request, response, endpoint):
    #Signatures to recognize messages
    out_signature = [8, 237, 156, 142, 161, 242, 41, 35, 8, 0, 16, 204, 40, 24, 200, 1, 40, 0, 48, 1, 56, 3, 64, 1, 72, 1, 80, 1, 88, 0, 96, 5, 112, 1, 120, 1, 128, 1, 1, 36, 59, 11, 8]
    
    if check_signature(request['content'], out_signature):
        response['content'] = request['content'].decode('utf8', "ignore")
        r = requests.post(endpoint+"/mail-out", data=json.dumps(response))
        print r.text
        
def check_signature(sequence, signature, tolerance=2):
    if len(sequence) < len(signature):
        return False
    
    failed = 0
    for i in xrange(len(signature)):
        if ord(sequence[i]) != signature[i]:
            failed += 1
        if failed > tolerance:
            break
    return failed <= tolerance