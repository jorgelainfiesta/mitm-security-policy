#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libmproxy.protocol.http import decoded
from libmproxy.flow import FlowWriter
#from urllib import unquote
#from urllib import quote
from datetime import datetime
import re

import requests
#import json
import sys  

def start(context, argv):
    if len(argv) != 2:
        raise ValueError('Usage: -s "mitm_stream.oy endpoint"')
    #Set system's encoding UTF-8
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
    #If it's from Google
    if "google" in request['host']:
        plain_content = request['content'].decode('utf8', "ignore")
        #Count emails in the payload
        emails = get_emails(plain_content)
        emails_count = sum(1 for _ in emails)
        #If it contains emails, we can assume it's an email: the parser will take care of everything else
        if emails_count > 0:
            response['content'] =plain_content
            r = requests.post(endpoint+"/put?queue=mailOut", json=response)

def get_emails(content):
    email_regex = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                        "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                        "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))
    
    return (email[0] for email in re.findall(email_regex, content) if not email[0].startswith('//'))