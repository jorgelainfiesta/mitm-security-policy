#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import json
import urllib

class Parser(object):

    # Constructor
    def __init__(self):
        return

    def contentParser(self, content):
        """
        Funcion para extraer informacion de correo electronico:
        content :    [string]       Contenido del correo electronico.
        return
        sender :     [string] Direccion de correo que envia el mensaje.
        recipients : [string list] Listado de direcciones de correo destinatarias.
        subject :    [string] Asunto del correo electronico.
        body :       [string] Cuerpo del correo.
        error :      [json] Mensaje de error
        """

        # Body
        bodyTemp = re.findall('<p dir=\"ltr\">.*?</p>',content)
        body = bodyTemp[0].replace('<p dir=\"ltr\">', '').replace('</p>', '')
        #if "<div class=\"gmail_quote\">" in content:
        #    boby = body + " " + re.findall('<div class=\"gmail_quote\">.*?</div>',content)[0]

        # Sender
        sender= re.compile('&lt;(.*?)&gt;', re.DOTALL |  re.IGNORECASE).findall(body)
        
        if(len(sender) > 0):
            sender = sender[0]
            body = body.split(sender)[0]
        else:
            sender= ""

        # Subject
        subjectTemp = re.compile(';(.*?)<p dir=\"ltr\">', re.DOTALL |  re.IGNORECASE).findall(content)
        subjectTemp = subjectTemp[0]

        if('\u0000*\u00002\u0016' in subjectTemp):
            subjectTemp = subjectTemp.split('\u0000*\u00002\u0016')
            subjectTemp = subjectTemp[1]
        elif('>2\u0016' in subjectTemp):
            subjectTemp = subjectTemp.split('>2\u0016')
            subjectTemp = subjectTemp[1]
        elif('\u0000*\u00002\x0c' in subjectTemp):
            subjectTemp = subjectTemp.split('\u0000*\u00002\x0c')
            subjectTemp = subjectTemp[1]
        elif('\u0000*\u00002\u0012' in subjectTemp):
            subjectTemp = subjectTemp.split('\u0000*\u00002\u0012')
            subjectTemp = subjectTemp[1]
        elif('>2\u0012' in subjectTemp):
            subjectTemp = subjectTemp.split('>2\u0012')
            subjectTemp = subjectTemp[1]
        elif('>2\x0c' in subjectTemp):
            subjectTemp = subjectTemp.split('>2\x0c')
            subjectTemp = subjectTemp[1]
        elif('\u0000*\u00002' in subjectTemp):
            subjectTemp = subjectTemp.split('\u0000*\u00002')
            subjectTemp = subjectTemp[1]
            subjectTemp = subjectTemp[6:]
        
        if('Re:' in subjectTemp):
            subjectTemp = subjectTemp.split('Re:')
            subjectTemp = "Re:" + subjectTemp[1]

        subjectTemp = subjectTemp.split(":")
        subject = ""
        counter = 0
        # Se ignora únicamente el ":" que aparece como delimitador en la cadena y se reestablecen los que se ecuentren el en subject.
        for i in subjectTemp:
            if(counter < len(subjectTemp) - 1):
                subject += str(i) + ":"
            else: 
                subject = subject[:-1]
                break
            counter +=1

        recipientsList = re.compile(';(.*?)<p dir=\"ltr\">', re.DOTALL |  re.IGNORECASE).findall(content)
        rL = recipientsList[0]#[1:]
        if "<\\f" in rL:
            rL = rL[1:]
        recipients = []
        recipientsList = re.findall('<.*?>',rL)
        for element in recipientsList:
            element = element.replace("<", "")
            element = element.replace(">", "")
            recipients.append(element)

        return sender, recipients, subject, body

#content = "\\b\\ud70e)#\\b\\u0000\\u00109\\u0018\\u0001(\\u00070\\u00018\\u0003@\\u0001H\\u0001P\\u0001X\\u0000`\\u0005p\\u0001x\\u0001\\u0001\\u0000$;\\u000b\\b\\u0003;\\n\\blabel:^f\\u00109<\\f\\u000b\\b\\u0003#\\b\\u0014\\u0010\\u0000\\u001a3<jorge.lainfiesta@gmail.com>, <lai11142@uvg.edu.gt>\"\\u0000*\\u00002\\u0012Dos destinatarios :\\u001c<p dir=\"ltr\">Hola aaaaa</p>\nP\\u0000X\\u0000p\\u0001z\\u0015neryalecorp@gmail.com$\\f\\u0010\\u0003<K\\b\\u0001\\u0010\\u0001\\u0018\\u0000 \\u0001(\\u00010\\u0001:\\u0005en_US@\\u0004LP\\u0002"
#parser = Parser()
#sender, recipients, subject, body = parser.contentParser(content)

#print ""
#print sender
#print recipients
#print subject
#print body