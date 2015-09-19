import re
import json
import urllib

class Parser(object):

    # Constructor
    def __init__(self):
        return
    # Funcion para extraer informacion de correo electronico:
    # Entrada: content : [string]       Contenido del correo electronico.
    # Salida:  data :                   Elementos del correo.
    #                 sender : [string]      Direccion de correo que envia el mensaje.
    #                 recipients : [string]  Listado de direcciones de correo destinatarias.
    #                 subject : [string]     Asunto del correo electronico.
    #                 body : [string]        Cuerpo del correo.
    #          error : [json]           Mensaje de error
    def contentParser(self, content):
        # Body
        body = re.findall('<p dir=\"ltr\">.*?</p>',content)
        body = body[0].replace('<p dir=\"ltr\">', '').replace('</p>', '')

        # Subject
        subject = re.compile('\"(.*?)<p dir=\"ltr\">', re.DOTALL |  re.IGNORECASE).findall(content)
        #subject = subject[0].replace(r'\u0000*\u00002', '')[6:-7]
        subject = subject[0].replace(r'\u0000*\u00002', '')[6:]
        subject = subject.split(":")[0]

        # Recipients
        recipientsList = re.findall('<.*?>\"',content)
        rL = recipientsList[0]#[1:]
        recipients = []
        recipientsList = re.findall('<.*?>',rL)
        for element in recipientsList:
            element = element.replace("<", "")
            element = element.replace(">", "")
            recipients.append(element)

        return recipients, subject, body

    def passwordParser(self, content):
        return "NotImplemented"

#content = '\x08\xed\x9c\x8e)#\x08\x00\x10/\x18\x01(\x000\x018\x03@\x01H\x01P\x01X\x00`\x05p\x01x\x01\x01\x01$;\x0b\x08\x02#\x08\x14\x10\x00\x1a\x1c<nnmorales@gmail.com>\x08\x14\x10\x00\x1a\x1c<jorge.lainfiesta@gmail.com>"\x00*\x002\x06Aaaaaa:\x17<p dir=ltr>Holaaaa</p>\nP\x00X\x00p\x01z\x15neryalecorp@gmail.com$\x0c\x10\x02<K\x08\x01\x10\x01\x18\x00 \x01(\x010\x01:\x05en_US@\x04LP\x02'
#content = "\\b\\ud70e)#\\b\\u0000\\u00109\\u0018\\u0001(\\u00070\\u00018\\u0003@\\u0001H\\u0001P\\u0001X\\u0000`\\u0005p\\u0001x\\u0001\\u0001\\u0000$;\\u000b\\b\\u0003;\\n\\blabel:^f\\u00109<\\f\\u000b\\b\\u0003#\\b\\u0014\\u0010\\u0000\\u001a3<jorge.lainfiesta@gmail.com>, <lai11142@uvg.edu.gt>\"\\u0000*\\u00002\\u0012Dos destinatarios :\\u001c<p dir=\"ltr\">Hola aaaaa</p>\\nP\\u0000X\\u0000p\\u0001z\\u0015neryalecorp@gmail.com$\\f\\u0010\\u0003<K\\b\\u0001\\u0010\\u0001\\u0018\\u0000 \\u0001(\\u00010\\u0001:\\u0005en_US@\\u0004LP\\u0002"
#parser = Parser()
#recipients, subject, body = parser.contentParser(content)

#print ""
#print recipients
#print subject
#print body