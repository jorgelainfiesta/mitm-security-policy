'''
BaseParser

A parser should process the HTTPRequest to produce a linear dictionary. 
If required, the parser should also clean the input texts from markup and similar.
'''
class BaseParser:
    #Receive an HTTPRequest
    #Return a dictionary with parsed content
    def parse(request):
        return NotImplemented