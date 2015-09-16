import requests
import parser
import json
import sys

#url_base = 'https://mitmendpoint.herokuapp.com/'
#url_base = 'https://localhost:9090/'
def translateMailData(content):
    sender , recipients, subject, body = parser.contentParser(content)

    sender_data = {"status" : "OK", "method" : "getSenderItem", "sender" : sender}
    json_sender_data = json.dumps(sender_data)

    nested_list = dict()
    for i in (len(recipients) + 1):
        recipient = "recipient" + str(i)
        nested_list[recipient] = recipients[i]

    recipients_data = {"status" : "OK", "method" : "getRecipientItem", "recipientList" : nested_list}
    json_recipients_data = json.dumps(recipients_data)

    subject_data = {"status" : "OK", "method" : "getSubjectItem", "subject" : subject}
    json_subject_data = json.dumps(subject_data)

    body_data = {"status" : "OK", "method" : "getMailBodyItem", "body" : body}
    json_body_data = json.dumps(body_data)

    return json_sender_data, json_recipients_data, json_subject_data, json_body_data

def translatePassword(content):
    password = parser.passwordParser(content)

    password_data = {"status" : "OK", "method" : "getPasswordItem", "password" : password}
    json_password_data = json.dumps(password_data)

    return json_password_data

def translate(url_base='https://localhost:9090/'):
    print "Iniciando servicio de traduccion de mensajes EndPoint mitmProxy - Parsers - Analizador..."

    while(True):
        
        #Consultar cola mailOut
        r = requests.get(url_base + 'get?queue=mailOut')
        contentData = eval(r.text)
        status = contentData["status"]
        print "    text: " + r.text
        if(status != "ERROR"):
            if(contentData["size"] > 0):
                content = contentData["elements"]["content"].encode("utf-8")
                json_sender_data, json_recipients_data, json_subject_data, json_body_data = translateMailData(content)
                r = requests.post(url_base + 'put?queue=recipientOut', json_recipients_data)
                r = requests.post(url_base + 'put?queue=subjectOut', json_subject_data)
                r = requests.post(url_base + 'put?queue=mailDataOut', json_body_data)
                #r.text
        else:
            print "    Error: " + contentData["method"].encode("utf-8") + contentData["msg"].encode("utf-8")

        #Consultar cola password
        r = requests.get(url_base + 'get?queue=password')
        passwordData = eval(r.text)
        status = passwordData["status"]
        print "    text: " + r.text
        if(status != "ERROR"):
            if(passwordData["size"] > 0):
                password = passwordData["elements"]["content"].encode("utf-8")
                json_password_data = translatePassword(password)
                r = requests.post(url_base + 'put?queue=passwordOut', json_password_data)
        else:
            print "    Error: " + contentData["method"].encode("utf-8") + contentData["msg"].encode("utf-8")

if __name__ == "__main__":
    translate(*sys.argv[1:])