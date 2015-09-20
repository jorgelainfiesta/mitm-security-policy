#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import parsers.parser as prs
import json
import sys
import ast
from mail_processing import process_mail
import Queue

available_queues = ["error"]
queues = {q: Queue.Queue() for q in available_queues}

def translate(url_base='http://localhost:9090/'):
    print "Iniciando servicio de traduccion de mensajes EndPoint mitmProxy - Parsers - Analizador..."

    while(True):
        errorFlag = False
        try:
            #Consultar cola mailOut
            r = requests.get(url_base + 'get?queue=mailOut')
            contentData = eval(r.text)
        except Exception, err:
            print "    # Error: # error al intentar obtener mensajes."
            print '               %sn' % str(err)
            errorFlag = True

        if(errorFlag == False):
            #r = u'{"status": "OK", "element": {"timestamp_end": "1442540628.99", "date-received": "2015-09-17 19:43:48", "msg":"OK", "content": "\\b\\ud70e)#\\b\\u0000\\u0010:\\u0018\\u0001(\\u00070\\u00018\\u0003@\\u0001H\\u0001P\\u0001X\\u0000`\\u0005p\\u0001x\\u0001\\u0001\\u0000$;\\u000b\\b\\u0003#\\b\\u0014\\u0010\\u0000\\u001a.<jlainfiesta@valsta.io>, <lai11142@uvg.edu.gt>\\"\\u0000*\\u00002\\u000bOtro correo:8<p dir=\\"ltr\\">Holaaaa espero que esto llegue a nery</p>\\nP\\u0000X\\u0000p\\u0001z\\u0015neryalecorp@gmail.com$\\f\\u0010\\u0003<K\\b\\u0001\\u0010\\u0001\\u0018\\u0000 \\u0001(\\u00010\\u0001:\\u0005en_US@\\u0004LP\\u0002", "httpversion": "(1, 1)", "headers": "[[\'Content-Type\', \'application/vnd.google-x-gms-proto; charset=utf-8\'], [\'Expires\', \'Fri, 18 Sep 2015 01:43:49 GMT\'], [\'Date\', \'Fri, 18 Sep 2015 01:43:49 GMT\'], [\'Cache-Control\', \'private, max-age=0\'], [\'X-Content-Type-Options\', \'nosniff\'], [\'X-Frame-Options\', \'SAMEORIGIN\'], [\'X-XSS-Protection\', \'1; mode=block\'], [\'Server\', \'GSE\'], [\'Transfer-Encoding\', \'chunked\']]", "timestamp_start": "1442540628.99"}, "queue": "temporal", "size":1, "method": "get"}'
            #r = eval(r)
            #contentData = r

            status = contentData["status"]
            print status

            print "..."
            if(status != "ERROR"):
                if(contentData["size"] > 0):
                    try:
                        print "    ...Parseando mensaje de correo electronico..."
                        content = contentData["element"]
                        #print content
                        content = content["content"].encode("utf-8")
                        p = prs.Parser()
                        sender, recipients, subject, body = p.contentParser(content)
                        print "        correo: Enviado por " + sender + " para " + recipients + "con asunto " + subject + "."
                        try:
                            sender = "neryalecorp@gmail.com" # Para el día sábado 19 de septiembre de 2015, el emisor ya no aparece en la data capturada.
                            process_mail(sender, recipients, subject, body)
                        except Exception, err:
                            raise Error('Error de procesamiento: '+ '%sn' % str(err))
                    except Exception, err:
                        queues["error"].put(msg)
                        print "    # Error: # "
                        print '%sn' % str(err)
                        print "    Se agrego contenido del mensaje a la cola error."
            else:
                print "    Error: " + contentData["method"].encode("utf-8") + contentData["msg"].encode("utf-8")




if __name__ == "__main__":
    translate(*sys.argv[1:])