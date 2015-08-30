'''
BaseProcessor

A processor should process a raw HTTPRequest.
It is responsible for parsing the HTTPRequest and any further operations.
'''
class BaseProcessor:
    def process(request):
        return NotImplemented