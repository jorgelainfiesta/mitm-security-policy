'''
Router

This module receives an HTTPRequest dict, reads its headers and redirects it to the corresponding processor. 
'''

#Recives an HTTPRequest
def redirect(request):
    print(request)