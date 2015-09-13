import os
import json
import cherrypy
from cherrypy import tools
from stompy.simple import Client
import Queue

from cherrypy.lib.httputil import parse_query_string

## Temporal
import random
import string

mailIn = Queue.Queue()
mailOut = Queue.Queue()
password = Queue.Queue()
errors = Queue.Queue()

passwordOut = Queue.Queue()
recipientOut = Queue.Queue()
mailDataOut = Queue.Queue()

def error_page_404(status, message, traceback, version):
    return "404 Error!"

class HomeController():
    #______________________________________________________________
    # Métodos de entrada:
    #______________________________________________________________

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    # Método para recibir mensajes de correo entrantes y contraseñas desde mitm-proxy
    def put(self, **kwargs):
        input_json = cherrypy.request.json
        msg = input_json
        msgOut = ""
        query = parse_query_string(cherrypy.request.query_string)
        queue = str(query["queue"]) 

        if(queue== "mailIn"):
            mailIn.put(msg)
            Dict_Message = dict()
            Dict_Message["status"] = "OK"
            Dict_Message["method"] = "put"
            Dict_Message["queue"] = "mailIn"
            Dict_Message["size"] = str(mailIn.qsize())
            msgOut = json.dumps(Dict_Message)
        elif(queue== "mailOut"):
            mailOut.put(msg)
            Dict_Message = dict()
            Dict_Message["status"] = "OK"
            Dict_Message["method"] = "put"
            Dict_Message["queue"] = "mailOut"
            Dict_Message["size"] = str(mailOut.qsize())
            msgOut = json.dumps(Dict_Message)
        elif(queue== "password"):
            password.put(msg)
            Dict_Message = dict()
            Dict_Message["status"] = "OK"
            Dict_Message["method"] = "put"
            Dict_Message["queue"] = "password"
            Dict_Message["size"] = str(password.qsize())
            msgOut = json.dumps(Dict_Message)
        else:
            Dict_Message = dict()
            Dict_Message["status"] = "ERROR"
            Dict_Message["method"] = "put"
            Dict_Message["msg"] = "Cola no existente."
            Dict_Message["code"] = "1"
            msgOut = json.dumps(Dict_Message)
            eMsg = msgOut
            errorMsg.put(eMsg)
        #stomp = Client("http://activemq-mitmactivemq.rhcloud.com", 61613)
        #stomp.connect("producer", "pass")
        #stomp.put(json.dumps(Dict_Message), destination="/queue/test",conf={'Test':'Test123'})
        #stomp.disconnect()
        return msgOut

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    # Método para consultar cantidad de mensajes en colas de entrada
    def qSize(self, **kwargs):
        msg= ""
        query = parse_query_string(cherrypy.request.query_string)
        queue = str(query["queue"]) 


        if(queue== "mailIn"):
            Dict_Message = dict()
            Dict_Message["status"] = "OK"
            Dict_Message["method"] = "qSize"
            Dict_Message["queue"] = "mailIn"
            Dict_Message["size"] = str(mailIn.qsize())
            msg = json.dumps(Dict_Message)
        elif(queue== "mailOut"):
            Dict_Message = dict()
            Dict_Message["status"] = "OK"
            Dict_Message["method"] = "qSize"
            Dict_Message["queue"] = "mailOut"
            Dict_Message["size"] = str(mailOut.qsize())
            msg = json.dumps(Dict_Message)
        elif(queue== "password"):
            Dict_Message = dict()
            Dict_Message["status"] = "OK"
            Dict_Message["method"] = "qSize"
            Dict_Message["queue"] = "password"
            Dict_Message["size"] = str(password.qsize())
            msg = json.dumps(Dict_Message)
        else:
            Dict_Message = dict()
            Dict_Message["status"] = "ERROR"
            Dict_Message["method"] = "qSize"
            Dict_Message["msg"] = "Cola no existente."
            Dict_Message["code"] = "1"
            msg = json.dumps(Dict_Message)
            eMsg = msg
            errorMsg.put(eMsg)
        return msg

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    # Método para obtener mensajes de colas de entrada.
    def get(self, **kwargs):
        query = parse_query_string(cherrypy.request.query_string)
        msg = ""
        #queue = kwargs["queue"]
        queue = str(query["queue"]) 

        if(queue== "mailIn"):
            if(mailIn.qsize() > 0):
                Dict_Message = dict()
                Dict_Message["status"] = "OK"
                Dict_Message["method"] = "get"
                Dict_Message["queue"] = "mailIn"
                Dict_Message["size"] = str(mailIn.qsize())
                Dict_Message["element"] = mailIn.get()
                msg = json.dumps(Dict_Message)
            else:
                Dict_Message = dict()
                Dict_Message["status"] = "OK"
                Dict_Message["method"] = "get"
                Dict_Message["queue"] = "mailIn"
                Dict_Message["size"] = "0"
                Dict_Message["element"] = ""
                msg = json.dumps(Dict_Message)
        elif(queue== "mailOut"):
            if(mailOut.qsize() > 0):
                Dict_Message = dict()
                Dict_Message["status"] = "OK"
                Dict_Message["method"] = "get"
                Dict_Message["queue"] = "mailIn"
                Dict_Message["size"] = str(mailOut.qsize())
                Dict_Message["element"] = mailOut.get()
                msg = json.dumps(Dict_Message)
            else:
                Dict_Message = dict()
                Dict_Message["status"] = "OK"
                Dict_Message["method"] = "get"
                Dict_Message["queue"] = "mailIn"
                Dict_Message["size"] = "0"
                Dict_Message["element"] = ""
                msg = json.dumps(Dict_Message)

        elif(queue== "password"):
            if(mailIn.qsize() > 0):
                Dict_Message = dict()
                Dict_Message["status"] = "OK"
                Dict_Message["method"] = "get"
                Dict_Message["queue"] = "password"
                Dict_Message["size"] = str(mailOut.qsize())
                Dict_Message["element"] = mailOut.get()
                msg = json.dumps(Dict_Message)
            else:
                Dict_Message = dict()
                Dict_Message["queue"] = "mailOut"
                Dict_Message["method"] = "get"
                Dict_Message["size"] = "0"
                Dict_Message["element"] = ""
                msg = json.dumps(Dict_Message)

        else:
            Dict_Message = dict()
            Dict_Message["status"] = "ERROR"
            Dict_Message["method"] = "get"
            Dict_Message["queue"] = queue
            Dict_Message["msg"] = "Cola no existente."
            Dict_Message["code"] = "1"
            msg = json.dumps(Dict_Message)
            eMsg = msg
            errorMsg.put(eMsg)
        return msg
        #return queue

    #______________________________________________________________
    # Métodos de salida
    #______________________________________________________________

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    # Método para obtención de contraseñas obtenidas.
    def getPasswordItem(self, **kwargs):
        rnd = random.randint(0,3)
        size = passwordOut.qsize()
        size = rnd
        if(size > 0):
            Dict_Message = dict()
            rnd = random.randint(1,25)
            Dict_Message["status"] = "OK"
            Dict_Message["method"] = "getPasswordItem"
            Dict_Message["password"] = ''.join(random.sample(string.hexdigits, int(rnd)))
            msg = json.dumps(Dict_Message)
        else:
            Dict_Message = dict()
            Dict_Message["method"] = "getPasswordItem"
            Dict_Message["msg"] = "0 elementos sin procesar."
            Dict_Message["code"] = "2"
            msg = json.dumps(Dict_Message)

        return msg

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    #Método para obtención de destinatarios
    def getRecipientItem(self, **kwargs):
        rnd = random.randint(0,3)
        size = recipientOut.qsize()
        size = rnd
        if(size > 0):
            Dict_Message = dict()
            rnd = random.randint(1,10)
            Dict_Message["status"] = "OK"
            Dict_Message["method"] = "getRecipientItem"
            nested_list = dict()
            for i in range(1, rnd+1):
                recipient = "recipient" + str(i)
                nested_list[recipient] = "" + ''.join(random.sample(string.hexdigits, int(8))) + "@gmail.com"
            Dict_Message["recipientList"] = nested_list
            msg = json.dumps(Dict_Message)
        else:
            Dict_Message = dict()
            Dict_Message["method"] = "getRecipientItem"
            Dict_Message["msg"] = "0 elementos sin procesar."
            Dict_Message["code"] = "2"
            msg = json.dumps(Dict_Message)
        return msg

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    #Método para obtención de contenidos de correos electrónicos.
    def getMailBodyItem(self, **kwargs):
        rnd = random.randint(0,3)
        size = mailDataOut.qsize()
        size = rnd
        if(size > 0):
            Dict_Message = dict()
            Dict_Message["status"] = "OK"
            Dict_Message["method"] = "getMailBodyItem"
            Dict_Message["body"] = "Vuelvo a mi habitacion, y sintiendo toda mi alma abrasada, no tarde en oir de nuevo un golpe, un poco mas fuerte que el primero. \"Seguramente - me dije -, hay algo en las persianas de la ventana; veamos que es y exploremos este misterio: es el viento, y nada mas\". Entonces empuje la persiana y, con un tumultuoso batir de alas, entro majestuoso un cuervo digno de las pasadas epocas. El animal no efectuo la menor reverencia, no se paro, no vacilo un minuto; pero con el aire de un Lord o de una Lady, se coloco por encima de la puerta de mi habitacion; posandose sobre un busto de Palas, precisamente encima de la puerta de mi alcoba; se poso, se instalo y nada mas.Entonces, este pajaro de ebano, por la gravedad de su continente, y por la severidad de su fisonomia, indujo a mi triste imaginacion a sonreir; \"Aunque tu cabeza - le dije - no tenga plumero, ni cimera, seguramente no eres un cobarde, lugubre y viejo cuervo, viajero salido de las riberas de la noche. Dime cual es tu nombre seniorial en las riberas de la Noche plutonica\". El cuervo exclamo: \"Nunca mas\"."
            msg = json.dumps(Dict_Message)
        else:
            Dict_Message = dict()
            Dict_Message["method"] = "getMailBodyItem"
            Dict_Message["msg"] = "0 elementos sin procesar."
            Dict_Message["code"] = "2"
            msg = json.dumps(Dict_Message)
        return msg
        
def start_server():

    cherrypy.tree.mount(HomeController(), '/')
    cherrypy.config.update({'error_page.404': error_page_404})

    cherrypy.config.update({'server.socket_host': '0.0.0.0',})
    cherrypy.config.update({'server.socket_port': int(os.environ.get('PORT', '9090')),})
    cherrypy.quickstart(HomeController())
    cherrypy.engine.start()

if __name__ == '__main__':
    start_server()


##############################################
# Cliente
#import requests
#r = requests.post('https://mitmendpoint.herokuapp.com/post', json={'tag': 'algo'})
#r.text

#r = requests.get('https://mitmendpoint.herokuapp.com/getMsg')
#r.text

#r = requests.get('https://mitmendpoint.herokuapp.com/gstatus')
#r.text

#QUEUES: mailIn, mailOut, password
# Enviar mensaje
#r = requests.post('https://mitmendpoint.herokuapp.com/put?queue=mailIn', json={'tag': 'algo'})
#r.text
#Posibles respuestas:
#    Sin errores
#            {"status": "OK", 
#             "method":"put",
#             "queue": "mailIn",
#             "size": "cantidad de mensajes en la cola"
#            }
#    Con errores
#            {"status" : "ERROR",
#             "method" = "put",
#             "msg" = "Cola no existente.",
#             "code" = "1"
#            }

#Consultar size de las distintas colas
#r = requests.get('https://mitmendpoint.herokuapp.com/qSize?queue=mailIn')
#r.text
#Posibles respuestas:
#    Sin errores
#            {"status": "OK", 
#             "method":"qSize",
#             "queue": "mailIn",
#             "size": "cantidad de mensajes en la cola"
#            }
#    Con errores
#            {"status" : "ERROR",
#             "method" = "qSize",
#             "msg" = "Cola no existente.",
#             "code" = "1"
#            }

#Obtener mensajes almacenados
#r = requests.get('https://mitmendpoint.herokuapp.com/get?queue=mailIn')
#r.text
#Posibles respuestas:
#    Sin errores
#            {"status" : "OK",
#              "method" : "get",
#              "queue" : "mailIn",
#              "size" : "cantidad de mensajes en la cola",
#              "element" : "mensaje obtenido de la cola",
#            }
#    Con errores
#            {"status" : "ERROR",
#             "method" = "get",
#             "msg" = "Cola no existente.",
#             "code" = "1"
#            }

## EndPoint Parsers-Analisis

# PASSWORDS

#import requests
#r = requests.get('https://mitmendpoint.herokuapp.com/getPasswordItem')
#r.text

#Posibles respuestas:
#    Sin errores
#            { "status" : "OK"
#              "method" : "getPasswordItem"           
#              "password" : "password generado al azar"
#            }
#    Cuando no hay elementos que procesar
#            { "method" : "getPasswordItem"
#              "msg" : "0 elementos sin procesar."
#              "code" : "2"
#            }

# RECIPIENTS
#import requests
#r = requests.get('https://mitmendpoint.herokuapp.com/getRecipientItem')
#r.text

#Posibles respuestas:
#    Sin errores
#            { "status" : "OK"
#              "method" : "getRecipientItem"           
#              "recipientList" : {
#                                    "recipient1" : "email generado al azar"
#                                     ...
#                                    "recipientN" : "email generado al azar"
#                                }
#            }
#    Cuando no hay elementos que procesar
#            { "method" : "getRecipientItem"
#              "msg" : "0 elementos sin procesar."
#              "code" : "2"
#            }

# MAIL BODY

#import requests
#r = requests.get('https://mitmendpoint.herokuapp.com/getMailBodyItem')
#r.text

#Posibles respuestas:
#    Sin errores
#            { "status" : "OK"
#              "method" : "getMailBodyItem"           
#              "body"] = "Vuelvo a mi habitacion, y sintiendo toda mi alma abrasada, 
#                         no tarde en oir de nuevo un golpe, un poco mas fuerte que el primero. 
#                         \"Seguramente - me dije -, hay algo en las persianas de la ventana; 
#                         veamos que es y exploremos este misterio: es el viento, y nada mas\". 
#                         Entonces empuje la persiana y, con un tumultuoso batir de alas, 
#                         entro majestuoso un cuervo digno de las pasadas epocas. 
#                         El animal no efectuo la menor reverencia, no se paro, no vacilo un minuto;
#                         pero con el aire de un Lord o de una Lady, se coloco por encima de la puerta de
#                         mi habitacion; posandose sobre un busto de Palas, precisamente encima de
#                         la puerta de mi alcoba; se poso, se instalo y nada mas.
#                         Entonces, este pajaro de ebano, por la gravedad de su continente,
#                         y por la severidad de su fisonomia, indujo a mi triste imaginacion a sonreir;
#                         \"Aunque tu cabeza - le dije - no tenga plumero, ni cimera, seguramente 
#                         no eres un cobarde, lugubre y viejo cuervo, viajero salido de las riberas de
#                         la noche. Dime cual es tu nombre seniorial en las riberas de la Noche plutonica\".
#                         El cuervo exclamo: \"Nunca mas\"."
#            }
#    Cuando no hay elementos que procesar
#            { "method" : "getMailBodyItem"
#              "msg" : "0 elementos sin procesar."
#              "code" : "2"
#            }