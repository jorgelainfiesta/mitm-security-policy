import re
import json

class Parser:

    # Constructor
    def __init__(self):
        pass
    # Funcion para extraer informacion de correo electronico:
    # Entrada: content : [string]       Contenido del correo electronico.
    # Salida:  data :                   Elementos del correo.
    #                 sender : [string]      Direccion de correo que envia el mensaje.
    #                 recipients : [string]  Listado de direcciones de correo destinatarias.
    #                 subject : [string]     Asunto del correo electronico.
    #                 body : [string]        Cuerpo del correo.
    #          error : [json]           Mensaje de error
    def contentParser(self, content):
  
        # Sender
        senderTemp = content.split('</p>')
        bodyTemp = senderTemp
        sender = senderTemp[len(senderTemp)-1].split('$', 1)
        sender = sender[0]
        sender = re.sub(r'[^\x20-\x7e]','*', sender)
        sender = sender.split('*')
        sender = sender[len(sender)-1]

        # Body
        body = bodyTemp[0].split('<p dir=ltr>')
        headerTemp = body[0]
        body = body[len(body)-1]

        # Subject
        headerTemp2 = headerTemp
        subjectTemp = headerTemp.split('"\x00*\x002')
        subject = subjectTemp[len(subjectTemp)-1]
        subject = re.sub(r'[^\x20-\x7e]','', subject)

        # Recipients
        recipientsList = re.findall('<.*?>',headerTemp2)
        recipients = []
        for element in recipientsList:
            element = element.replace("<", "")
            element = element.replace(">", "")
            recipients.append(element)
	
        return sender , recipients, subject, body

    def passwordParser(content):
        return "NotImplemented"

#content = '\x08\xed\x9c\x8e)#\x08\x00\x10/\x18\x01(\x000\x018\x03@\x01H\x01P\x01X\x00`\x05p\x01x\x01\x01\x01$;\x0b\x08\x02#\x08\x14\x10\x00\x1a\x1c<nnmorales@gmail.com>\x08\x14\x10\x00\x1a\x1c<jorge.lainfiesta@gmail.com>"\x00*\x002\x06Aaaaaa:\x17<p dir=ltr>Holaaaa</p>\nP\x00X\x00p\x01z\x15neryalecorp@gmail.com$\x0c\x10\x02<K\x08\x01\x10\x01\x18\x00 \x01(\x010\x01:\x05en_US@\x04LP\x02'
#parser = Parser()
#sender , recipients, subject, body = parser.contentParser(content)

#print sender
#print recipients
#print subject
#print body