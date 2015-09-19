import requests
import parsers.parser as prs
import json
import sys


import ast
#url_base = 'https://mitmendpoint.herokuapp.com/'
#url_base = 'https://localhost:9090/'

def translateMailData(content):
    p = prs.Parser()
    recipients, subject, body = p.contentParser(content)

    #sender_data = {"status" : "OK", "method" : "getSenderItem", "sender" : sender}
    #json_sender_data = json.dumps(sender_data)

    nested_list = dict()

    for i in range (0, len(recipients)):
        recipient = "recipient" + str(i)
        nested_list[recipient] = recipients[i]

    recipients_data = {"status" : "OK", "method" : "getRecipientItem", "recipientList" : nested_list}
    json_recipients_data = json.dumps(recipients_data)

    subject_data = {"status" : "OK", "method" : "getSubjectItem", "subject" : subject}
    json_subject_data = json.dumps(subject_data)

    body_data = {"status" : "OK", "method" : "getMailBodyItem", "body" : body}
    json_body_data = json.dumps(body_data)

    return json_recipients_data, json_subject_data, json_body_data

def translatePassword(content):
    p = prs.Parser()
    password = p.passwordParser(content)

    password_data = {"status" : "OK", "method" : "getPasswordItem", "password" : password}
    json_password_data = json.dumps(password_data)

    return json_password_data

def translate(url_base='http://localhost:9090/'):
    print "Iniciando servicio de traduccion de mensajes EndPoint mitmProxy - Parsers - Analizador..."

    while(True):
        
        #Consultar cola mailOut
        r = requests.get(url_base + 'get?queue=mailOut')
        contentData = json.loads(r.text.encode("utf-8"))
        status = contentData["status"]
        

        print "..."
        if(status != "ERROR"):
            if(contentData["size"] > 0):
                #try:
                    print "...Parseando mensaje de correo electronico..."
                    c = contentData["element"]
                    content = ast.literal_eval(c)
                    print content
                    content = content["content"].encode("utf-8")
                    #break
                    json_recipients_data, json_subject_data, json_body_data = translateMailData(content)
                    r = requests.post(url_base + 'put?queue=recipientOut', json= json.dumps(json_recipients_data))
                    r = requests.post(url_base + 'put?queue=subjectOut', json= json.dumps(json_subject_data))
                    r = requests.post(url_base + 'put?queue=mailDataOut', json= json.dumps(json_body_data))
                    #r.text
                #except Exception, err:
                #    r = requests.post(url_base + 'put?queue=error', json=json.dumps(contentData))
                #    print "    # Error: # " + '%sn' % str(err)
                #    print "    Se agrego contenido del mensaje a la cola error."
        else:
            print "    Error: " + contentData["method"].encode("utf-8") + contentData["msg"].encode("utf-8")

        #Consultar cola password
        r = requests.get(url_base + 'get?queue=password')
        passwordData = eval(r.text)
        status = passwordData["status"]
        print "..."
        if(status != "ERROR"):
            if(passwordData["size"] > 0):
                try:
                    print "...Parseando mensaje con contraseniaa..."
                    password = passwordData["element"]["content"].encode("utf-8")
                    json_password_data = translatePassword(password)
                    r = requests.post(url_base + 'put?queue=passwordOut', json= json.dumps(json_password_data))
                except Exception, err:
                    r = requests.post(url_base + 'put?queue=error', json=json.dumps(passwordData))
                    print "    # Error: # " + '%sn' % str(err)
                    print "    Se agrego contenido del mensaje a la cola error."

        else:
            print "    Error: " + contentData["method"].encode("utf-8") + contentData["msg"].encode("utf-8")

if __name__ == "__main__":
    translate(*sys.argv[1:])