from libmproxy.protocol.http import decoded
from libmproxy.flow import FlowWriter
from urllib import unquote
from datetime import datetime

import requests
import json

def start(context, argv):
    if len(argv) != 2:
        raise ValueError('Usage: -s "mitm_stream.oy endpoint"')
    context.endpoint = argv[1]
    
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
                    requestDict[attr] = unicode(unquote(flow.request.content), "utf-8")
                else:
                    requestDict[attr] = str(getattr(flow.request, attr))
            except Exception, e:
                requestDict[attr] = str(e)
    
    #Process response
    responseAttrs = ["httpversion", "status_code", "msg", "headers", "content", "timestamp_start", "timestamp_end"]
    
    responseDict = {}
    
    responseDict['date-received'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #Build HTTPResponse dict with decoded data
    with decoded(flow.response):
        for attr in responseAttrs:
            try:
                if attr == "content":
                    responseDict[attr] = unicode(unquote(flow.response.content), "ISO-8859-1")
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
    #Send test request
#    r = requests.post(endpoint, data=json.dumps(requestDict))
#    print r.text
    
    pass