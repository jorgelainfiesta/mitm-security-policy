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
            contentData = eval(r.text)

        except Exception, err:
            print "    # Error: # error al intentar obtener mensajes."
            print '               %sn' % str(err)
            errorFlag = True

        if(errorFlag == False):
            status = contentData["status"]
            #print "..."
            if(status != "ERROR"):
                if(contentData["size"] > 0):
                    try:
                        print "    ...Parseando mensaje de correo electronico..."
                        content = contentData["element"]
                        #print ""
                        #print content
                        #print ""
                        content = content["content"].encode("utf-8")
                        p = prs.Parser()
                        sender, recipients, subject, body = p.contentParser(content)
                         
                        #print subject
                        h = HTMLParser.HTMLParser()
                        subject = h.unescape(subject) 
                        subject = change(subject)
                        #print "sujeto: " , subject      

        
                        body = body.decode('utf8')
                        body = h.unescape(body)
                        #print "contenido: ", body
 
                        if (sender == ""):
                            sender = "neryalecorp@gmail.com" # Para el día sábado 19 de septiembre de 2015, el emisor ya no aparece en la data capturada.
                        print "        correo: Enviado por " + sender + " para " + str(recipients)
                        print "                con asunto " + subject + " ."
                        print "                Contenido: " + body 

                        #break
                        try:
                            process_mail(sender, recipients, subject, body)
                        except Exception, err:
                            raise ValueError('Error de procesamiento: '+ '%sn' % str(err))
                    except Exception, err:
                        queues["error"].put(contentData)
                        print "    # Error: # "
                        print '%sn' % str(err)
                        print "    Se agrego contenido del mensaje a la cola error."
            else:
                print "    Error: " + contentData["method"].encode("utf-8") + contentData["msg"].encode("utf-8")




if __name__ == "__main__":
    translate(*sys.argv[1:])