from libmproxy.protocol.http import decoded
from libmproxy.flow import FlowWriter
from urllib import unquote
from datetime import datetime

from router import redirect

'''
Reads responses from MITM proxy and maps relevant info to a dict.
Then calls the router to redirect HTTPResponse dict.
'''
def response(context, flow):
    responseAttrs = ["httpversion", "status_code", "msg", "headers", "content", "timestamp_start", "timestamp_end"]
    
    responseDict = {}
    
    responseDict['date-received'] = datetime.now()
    #Build HTTPResponse dict with decoded data
    with decoded(flow.response):
        for attr in responseAttrs:
            try:
                if attr == "headers":
                    responseDict[attr] = flow.response.headers
                if attr == "content":
                    responseDict[attr] = unquote(flow.response.content)
                else:
                    responseDict[attr] = str(getattr(flow.response, attr))
            except Exception, e:
                responseDict[attr] = str(e)
    redirect.redirect(responseDict)