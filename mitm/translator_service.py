#!/usr/bin/env python
# -*- coding: utf-8 -*-<2
import requests
import parsers.parser as prs
import json
import sys
import ast
from mail_processing import process_mail
import Queue
import HTMLParser


import cgi
available_queues = ["error"]
queues = {q: Queue.Queue() for q in available_queues}

def change(subject):
    enc = ["\u00e1","\u00e9","\u00ed","\u00f3","\u00fa","\u00c1","\u00c9","\u00cd","\u00d3","\u00da","\u00f1","\u00d1"]
    dec = ["á","é","í","ó","ú","Á","É","Í","Ó","Ú","ñ","Ñ"]

    index = 0
    for rep in enc:
        subject = subject.replace(rep,dec[index])
        index += 1

    return subject


def translate(url_base='http://localhost:9090'):
    print "    Iniciando servicio de traduccion de mensajes EndPoint"
    print "        mitmProxy - Parsers - Analizador..."

    while(True):
        errorFlag = False
        try:
            #Consultar cola mailOut
            r = requests.get(url_base + '/get?queue=mailOut')
            contentData = eval(r.text) #quiero ver todo lo que devuelve esto, me refiero a la ahh hahah
           # print  contentData.keys()    
        except Exception, err:
            print "    # Error: # error al intentar obtener mensajes."
            print '               %sn' % str(err)
            errorFlag = True

        if(errorFlag == False):
            #r = u'{"status": "OK", "element": {"timestamp_end": "1442540628.99", "date-received": "2015-09-17 19:43:48", "msg":"OK", "content": "\\b\\ud70e)#\\b\\u0000\\u0010:\\u0018\\u0001(\\u00070\\u00018\\u0003@\\u0001H\\u0001P\\u0001X\\u0000`\\u0005p\\u0001x\\u0001\\u0001\\u0000$;\\u000b\\b\\u0003#\\b\\u0014\\u0010\\u0000\\u001a.<jlainfiesta@valsta.io>, <lai11142@uvg.edu.gt>\\"\\u0000*\\u00002\\u000bOtro correo:8<p dir=\\"ltr\\">Holaaaa espero que esto llegue a nery</p>\\nP\\u0000X\\u0000p\\u0001z\\u0015neryalecorp@gmail.com$\\f\\u0010\\u0003<K\\b\\u0001\\u0010\\u0001\\u0018\\u0000 \\u0001(\\u00010\\u0001:\\u0005en_US@\\u0004LP\\u0002", "httpversion": "(1, 1)", "headers": "[[\'Content-Type\', \'application/vnd.google-x-gms-proto; charset=utf-8\'], [\'Expires\', \'Fri, 18 Sep 2015 01:43:49 GMT\'], [\'Date\', \'Fri, 18 Sep 2015 01:43:49 GMT\'], [\'Cache-Control\', \'private, max-age=0\'], [\'X-Content-Type-Options\', \'nosniff\'], [\'X-Frame-Options\', \'SAMEORIGIN\'], [\'X-XSS-Protection\', \'1; mode=block\'], [\'Server\', \'GSE\'], [\'Transfer-Encoding\', \'chunked\']]", "timestamp_start": "1442540628.99"}, "queue": "temporal", "size":1, "method": "get"}'
            #r = eval(r)
            #contentData = r

            status = contentData["status"]
            #print "..."
            if(status != "ERROR"):
                if(contentData["size"] > 0):
                    try:
                        print "    ...Parseando mensaje de correo electronico..."
                        content = contentData["element"]
                        print ""
                        print content
                        print ""
                        content = content["content"].encode("utf-8")
                        #subject =  content["subject"].encode("utf-8")
                        print content
                        #       subject =  subject["subject"].encode["utf-8"]
                        p = prs.Parser()
                        sender, recipients, subject, body = p.contentParser(content)
                         
                        print subject
                        #subject = subject.decode('utf8')
                        h = HTMLParser.HTMLParser()
                        subject = h.unescape(subject) 
                        subject = change(subject)
                        print "sujeto: " , subject      

        
                        body = body.decode('utf8')
                        body = h.unescape(body)
                        print "predicado: ", body
 
                        sender = "neryalecorp@gmail.com" # Para el día sábado 19 de septiembre de 2015, el emisor ya no aparece en la data capturada.
                        print "        correo: Enviado por " + sender + " para " + str(recipients) + " con asunto " + ". " + body 
                        #break
                        #cadena = u"día niño áéíóú".encode('latin_1')
                        #cadena = "día niño áéíóú"
                        #print (((cadena).encode('utf-8')).encode('latin_1')).decode('latin_1')
                        #print cadena.decode('utf8')

                        break
                        #try:
                            #process_mail(sender, recipients, subject, body)
                        #except Exception, err:
                        #    raise ValueError('Error de procesamiento: '+ '%sn' % str(err))
                    except Exception, err:
                        queues["error"].put(contentData)
                        print "    # Error: # "
                        print '%sn' % str(err)
                        print "    Se agrego contenido del mensaje a la cola error."
            else:
                print "    Error: " + contentData["method"].encode("utf-8") + contentData["msg"].encode("utf-8")




if __name__ == "__main__":
    translate(*sys.argv[1:])