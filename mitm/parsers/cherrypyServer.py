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

available_queues = ["mailIn", "mailOut", "password", "errors", "passwordOut", "recipientOut", "mailDataOut", "subjectOut"]
queues = {q: Queue.Queue() for q in available_queues}

def error_page_404(status, message, traceback, version):
    return "404 Error!"

class HomeController():
    #______________________________________________________________
    # Metodos de entrada:
    #______________________________________________________________

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    # Metodo para recibir mensajes de correo entrantes y contrasenias desde mitm-proxy
    def put(self, **kwargs):
        input_json = cherrypy.request.json
        msg = input_json
        msgOut = ""
        query = parse_query_string(cherrypy.request.query_string)
        queue = str(query["queue"]) 
        
        if queue in available_queues:
            queues[queue].put(msg)
            msgOut = {"status" : "OK", "method" : "put", "queue" : queue, "size" : queues[queue].qsize()}
        else:
            msgOut = {"status" : "ERROR", "method" : "put", "msg" : "Cola no existente."}
        #stomp = Client("http://activemq-mitmactivemq.rhcloud.com", 61613)
        #stomp.connect("producer", "pass")
        #stomp.put(json.dumps(Dict_Message), destination="/queue/test",conf={'Test':'Test123'})
        #stomp.disconnect()
        return msgOut

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    # Metodo para consultar cantidad de mensajes en colas de entrada
    def qSize(self, **kwargs):
        msgOut= ""
        query = parse_query_string(cherrypy.request.query_string)
        queue = str(query["queue"])

        if queue in available_queues:
            msgOut = {"status" : "OK", "method" : "qSize", "queue" : queue, "size" : queues[queue].qsize()}
        else:
            msgOut = {"status" : "ERROR", "method" : "qSize", "msg" : "Cola no existente."}
        return msgOut

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    # Metodo para obtener mensajes de colas de entrada.
    def get(self, **kwargs):
        query = parse_query_string(cherrypy.request.query_string)
        msgOut = ""
        #queue = kwargs["queue"]
        queue = str(query["queue"]) 
        
        if queue in available_queues:
            if queues[queue].qsize() > 0:
                msgOut = {"status" : "OK", "method" : "get", "queue" : queue, "size" : queues[queue].qsize(), "element" : queues[queue].get()}
            else:
                msgOut = {"status" : "OK", "method" : "get", "queue" : queue, "size" : 0}
        else:
            msgOut = {"status" : "ERROR", "method" : "get", "msg" : "Cola no existente."}
            
        return msgOut
        #return queue

    #______________________________________________________________
    # Metodos de salida
    #______________________________________________________________

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    # Metodo para obtencion de contrasenias obtenidas.
    def getPasswordItem(self, **kwargs):
        size = passwordOut.qsize()

        if(size > 0):
            msg = passwordOut.get()
            #msg = json.dumps(passwordData)
        else:
            # Temporal, para pruebas: BEGIN Borrar
            rnd = random.randint(0,3)
            size = rnd
            if(size > 0):
                rnd = random.randint(1,25)
                msg = {"status" : "OK",  "method" : "getPasswordItem", "password" : ''.join(random.sample(string.hexdigits, int(rnd)))}
                #msg = json.dumps(msg)
            else:
                msg = {"status" : "0size","method" : "getPasswordItem", "msg" : "0 elementos sin procesar.", "code" : "2"}
                #msg = json.dumps(msg)
            # Temporal, para pruebas: END Borrar
        #else:
        #    msg = {"status" : "0size","method" : "getPasswordItem", "msg" : "0 elementos sin procesar.", "code" : "2"}


        return msg

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    #Metodo para obtencion de destinatarios
    def getRecipientItem(self, **kwargs):
        size = recipientOut.qsize()

        if(size > 0):
            msg = recipientOut.get()
            #msg = json.dumps(passwordData)
        else:
            # Temporal, para pruebas: BEGIN Borrar
            rnd = random.randint(0,3)
            size = rnd
            if(size > 0):
                rnd = random.randint(1,10)
                nested_list = dict()
                for i in range(1, rnd+1):
                    recipient = "recipient" + str(i)
                    nested_list[recipient] = "" + ''.join(random.sample(string.hexdigits, int(8))) + "@gmail.com"
                msg = {"status" : "OK",  "method" : "getRecipientItem", "recipientList" : nested_list}
                #msg = json.dumps(msg)
            else:
                msg = {"status" : "0size","method" : "getRecipientItem", "msg" : "0 elementos sin procesar.", "code" : "2"}
                #msg = json.dumps(msg)
            # Temporal, para pruebas: END Borrar
        #else:
        #    msg = {"status" : "0size","method" : "getRecipientItem", "msg" : "0 elementos sin procesar.", "code" : "2"}

        return msg

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    #Metodo para obtencion de contenidos de correos electronicos.
    def getMailBodyItem(self, **kwargs):
        size = mailDataOut.qsize()

        if(size > 0):
            msg = mailDataOut.get()
            #msg = json.dumps(passwordData)
        else:
            # Temporal, para pruebas: BEGIN Borrar
            rnd = random.randint(0,3)
            size = rnd
            if(size > 0):
                msg = {"status" : "OK",  "method" : "getMailBodyItem", "body" : "Vuelvo a mi habitacion, y sintiendo toda mi alma abrasada, no tarde en oir de nuevo un golpe, un poco mas fuerte que el primero. \"Seguramente - me dije -, hay algo en las persianas de la ventana; veamos que es y exploremos este misterio: es el viento, y nada mas\". Entonces empuje la persiana y, con un tumultuoso batir de alas, entro majestuoso un cuervo digno de las pasadas epocas. El animal no efectuo la menor reverencia, no se paro, no vacilo un minuto; pero con el aire de un Lord o de una Lady, se coloco por encima de la puerta de mi habitacion; posandose sobre un busto de Palas, precisamente encima de la puerta de mi alcoba; se poso, se instalo y nada mas.Entonces, este pajaro de ebano, por la gravedad de su continente, y por la severidad de su fisonomia, indujo a mi triste imaginacion a sonreir; \"Aunque tu cabeza - le dije - no tenga plumero, ni cimera, seguramente no eres un cobarde, lugubre y viejo cuervo, viajero salido de las riberas de la noche. Dime cual es tu nombre seniorial en las riberas de la Noche plutonica\". El cuervo exclamo: \"Nunca mas\"."}
                #msg = json.dumps(msg)
            else:
                msg = {"status" : "0size","method" : "getMailBodyItem", "msg" : "0 elementos sin procesar.", "code" : "2"}
                #msg = json.dumps(msg)
            # Temporal, para pruebas: END Borrar
        #else:
        #    msg = {"status" : "0size","method" : "getMailBodyItem", "msg" : "0 elementos sin procesar.", "code" : "2"}

        return msg

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    #Metodo para obtencion de asunto de correos electronicos.
    def getSubjectItem(self, **kwargs):
        size = subjectOut.qsize()

        if(size > 0):
            msg = subjectOut.get()
            #msg = json.dumps(passwordData)
        else:
            # Temporal, para pruebas: BEGIN Borrar
            rnd = random.randint(0,3)
            size = rnd
            if(size > 0):
                msg = {"status" : "OK",  "method" : "getSubjectItem", "subject" : "Prueba"}
                #msg = json.dumps(msg)
            else:
                msg = {"status" : "0size","method" : "getSubjectItem", "msg" : "0 elementos sin procesar.", "code" : "2"}
                #msg = json.dumps(msg)
            # Temporal, para pruebas: END Borrar
        #else:
        #    msg = {"status" : "0size","method" : "getSubjectItem", "msg" : "0 elementos sin procesar.", "code" : "2"}

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