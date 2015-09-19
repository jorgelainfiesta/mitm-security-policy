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
        #r = requests.get(url_base + 'get?queue=mailOut')
        #contentData = eval(r.text)

        ##contentData = json.loads(r.text.encode("utf-8"))
        #r = u'{"status": "OK", "element": {"timestamp_end": "1442540628.99", "date-received": "2015-09-17 19:43:48", "msg":"OK", "content": "\\b\\ud70e)#\\b\\u0000\\u00109\\u0018\\u0001(\\u00070\\u00018\\u0003@\\u0001H\\u0001P\\u0001X\\u0000`\\u0005p\\u0001x\\u0001\\u0001\\u0000$;\\u000b\\b\\u0003;\\n\\blabel:^f\\u00109<\\f\\u000b\\b\\u0003#\\b\\u0014\\u0010\\u0000\\u001a3<jorge.lainfiesta@gmail.com>, <lai11142@uvg.edu.gt>\\"\\u0000*\\u00002\\u0012Dos destinatarios :\\u001c<p dir=\\"ltr\\">Hola aaaaa</p>\\nP\\u0000X\\u0000p\\u0001z\\u0015neryalecorp@gmail.com$\\f\\u0010\\u0003<K\\b\\u0001\\u0010\\u0001\\u0018\\u0000 \\u0001(\\u00010\\u0001:\\u0005en_US@\\u0004LP\\u0002", "httpversion": "(1, 1)", "headers": "[[\'Content-Type\', \'application/vnd.google-x-gms-proto; charset=utf-8\'], [\'Expires\', \'Fri, 18 Sep 2015 01:43:49 GMT\'], [\'Date\', \'Fri, 18 Sep 2015 01:43:49 GMT\'], [\'Cache-Control\', \'private, max-age=0\'], [\'X-Content-Type-Options\', \'nosniff\'], [\'X-Frame-Options\', \'SAMEORIGIN\'], [\'X-XSS-Protection\', \'1; mode=block\'], [\'Server\', \'GSE\'], [\'Transfer-Encoding\', \'chunked\']]", "timestamp_start": "1442540628.99"}, "queue": "temporal", "size":1, "method": "get"}'
        r = u'{"status": "OK", "element": {"timestamp_end": "1442540628.99", "date-received": "2015-09-17 19:43:48", "msg":"OK", "content": "\\b\\ud70e)#\\b\\u0000\\u0010:\\u0018\\u0001(\\u00070\\u00018\\u0003@\\u0001H\\u0001P\\u0001X\\u0000`\\u0005p\\u0001x\\u0001\\u0001\\u0000$;\\u000b\\b\\u0003#\\b\\u0014\\u0010\\u0000\\u001a.<jlainfiesta@valsta.io>, <lai11142@uvg.edu.gt>\\"\\u0000*\\u00002\\u000bOtro correo:8<p dir=\\"ltr\\">Holaaaa espero que esto llegue a nery</p>\\nP\\u0000X\\u0000p\\u0001z\\u0015neryalecorp@gmail.com$\\f\\u0010\\u0003<K\\b\\u0001\\u0010\\u0001\\u0018\\u0000 \\u0001(\\u00010\\u0001:\\u0005en_US@\\u0004LP\\u0002", "httpversion": "(1, 1)", "headers": "[[\'Content-Type\', \'application/vnd.google-x-gms-proto; charset=utf-8\'], [\'Expires\', \'Fri, 18 Sep 2015 01:43:49 GMT\'], [\'Date\', \'Fri, 18 Sep 2015 01:43:49 GMT\'], [\'Cache-Control\', \'private, max-age=0\'], [\'X-Content-Type-Options\', \'nosniff\'], [\'X-Frame-Options\', \'SAMEORIGIN\'], [\'X-XSS-Protection\', \'1; mode=block\'], [\'Server\', \'GSE\'], [\'Transfer-Encoding\', \'chunked\']]", "timestamp_start": "1442540628.99"}, "queue": "temporal", "size":1, "method": "get"}'
        r = eval(r)
        contentData = r

        status = contentData["status"]
        print status

        print "..."
        if(status != "ERROR"):
            if(contentData["size"] > 0):
                #try:
                    print "...Parseando mensaje de correo electronico..."
                    content = contentData["element"]
                    #content = eval(c)
                    print content
                    content = content["content"].encode("utf-8")
                    #break
                    json_recipients_data, json_subject_data, json_body_data = translateMailData(content)
                    r = requests.post(url_base + 'put?queue=recipientOut', json= json.dumps(json_recipients_data))
                    r = requests.post(url_base + 'put?queue=subjectOut', json= json.dumps(json_subject_data))
                    r = requests.post(url_base + 'put?queue=mailDataOut', json= json.dumps(json_body_data))
                    break
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