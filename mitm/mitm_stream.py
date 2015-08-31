from libmproxy.protocol.http import decoded
from libmproxy.flow import FlowWriter
from urllib import unquote
from datetime import datetime

'''
Reads responses from MITM proxy and maps relevant info to a dict.
Then calls the router to redirect HTTPResponse dict.
'''
def response(context, flow):
    #Process request
    requestAttrs = ["method", "scheme", "host", "port", "path", "httpversion", "headers", "content", "form_in", "timestamp_start", "timestamp_end"]
    
    requestDict = {}
    
    requestDict['date-sent'] = datetime.now()
    #Build HTTPRequest dict with decoded data
    with decoded(flow.request):
        for attr in requestAttrs:
            try:
                if attr == "content":
                    requestDict[attr] = unquote(flow.request.content)
                else:
                    requestDict[attr] = str(getattr(flow.request, attr))
            except Exception, e:
                requestDict[attr] = str(e)
    
    #Process response
    responseAttrs = ["httpversion", "status_code", "msg", "headers", "content", "timestamp_start", "timestamp_end"]
    
    responseDict = {}
    
    responseDict['date-received'] = datetime.now()
    #Build HTTPResponse dict with decoded data
    with decoded(flow.response):
        for attr in responseAttrs:
            try:
                if attr == "content":
                    responseDict[attr] = unquote(flow.response.content)
                else:
                    responseDict[attr] = str(getattr(flow.response, attr))
            except Exception, e:
                responseDict[attr] = str(e)
    
#    print redirectTo(requestDict, responseDict)

'''
This method receives an HTTPRequest dict and a HTTPResponse dict, reads its headers and redirects it to the corresponding processor. 
'''
def redirectTo(request, response):
    pass