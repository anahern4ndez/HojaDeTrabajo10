# -*- coding: cp1252 -*-
#Universidad del valle de Guatemala
#Algoritmos y estructura de datos, seccion:10
#hdt10.py
#Hoja de trabajo 10 - utilizando neo4J y creando recomendaciones
#Maria Fernanda Lopez - 17160
#Ana Lucia Hernandez  - 17138
#Andrea Carolina Arguello - 17801
#18/05/2018

from neo4jrestclient.client import GraphDatabase
from neo4jrestclient import client
import sys

driver = GraphDatabase("http://localhost:7474", username="neo4j", password="mypassword")


pacientes = driver.labels.create("Paciente")
doctores = driver.labels.create("Doctor")
medicinas = driver.labels.create("Medicinas")

# ------------ CREACION NODOS ---------------
def add_Paciente(nombre, telefono):
    p1 = driver.nodes.create(Nombre=nombre, Telefono=telefono)
    pacientes.add(p1)
    return p1
    print ("\n¡Paciente agregado!")
    
def add_Doctor(nombre, telefono, colegiado, especialidad):
    d = driver.nodes.create(Nombre=nombre, Telefono=telefono, Colegiado=colegiado, Especialidad=especialidad)
    doctores.add(d)
    return d
    print ("\n¡Doctor agregado!")

def add_Medicina(nombre, desdeFecha, hastaFecha, dosis):
    m = driver.nodes.create(Nombre=nombre, desdeFecha=desdeFecha, hastaFecha=desdeFecha, Dosis=dosis)
    medicinas.add(m)
    return m
    print ("\n¡Medicina agregada!")

def registrarVisita(paciente,doctor,fecha,medicina,desde,hasta,dosis):
    med=add_Medicina(medicina,desde,hasta,dosis)
    visitaDP(paciente,doctor,fecha)
    relacionPM(paciente,med)
    relacionDM(doctor,med)

# ------------ CREACION RELACIONES ---------------
def visitaDP(paciente, doctor, fecha):
    paciente.relationships.create("FECHA", doctor)
    #q = 'MATCH ("'+paciente+'")-[r:CONOCE]->("'+doctor+'") SET r.Fecha =\"'+fecha+'\" RETURN r'    

def relacionPM(paciente, medicina):
    q='MATCH (u:Paciente) WHERE u.Nombre="'+paciente+'"RETURN u'
    pacientes = driver.query(q,returns=(client.Node,str,client.Node))
    for p in pacientes:
        print("(%s)" % (p[0]["Nombre"]))
    p1=p[0]

    r='MATCH (u:Medicina) WHERE u.Nombre="'+medicina+'"RETURN u'
    medicinas = driver.query(r,returns=(client.Node,str,client.Node))
    for r in medicinas:
        print("(%s)" % (r[0]["Nombre"]))
    med=r[0]
    p1.relationships.create("TOMA", med)

def relacionDM(doctor, medicina):
    q='MATCH (u:Doctor) WHERE u.Nombre="'+doctor+'"RETURN u'
    doctores = driver.query(q,returns=(client.Node,str,client.Node))
    for p in doctores:
        print("(%s)" % (p[0]["Nombre"]))
    p1=p[0]

    r='MATCH (u:Medicina) WHERE u.Nombre="'+medicina+'"RETURN u'
    medicinas = driver.query(r,returns=(client.Node,str,client.Node))
    for r in medicinas:
        print("(%s)" % (r[0]["Nombre"]))
    med=r[0]
    p1.relationships.create("PRESCRIBE", med)

def relacionPP(paciente, paciente1):
    q='MATCH (u:Paciente) WHERE u.Nombre="'+paciente+'"RETURN u'
    pacientes = driver.query(q,returns=(client.Node,str,client.Node))
    for p in pacientes:
        print("(%s)" % (p[0]["Nombre"]))
    p1=p[0]

    r='MATCH (u:Paciente) WHERE u.Nombre="'+paciente1+'"RETURN u'
    pacientes2 = driver.query(r,returns=(client.Node,str,client.Node))
    for r in pacientes2:
        print("(%s)" % (r[0]["Nombre"]))
    p2=r[0]
    p1.relationships.create("CONOCE", p2)
    p2.relationships.create("CONOCE",p1)

def relacionDP(doctor, paciente):
    q='MATCH (u:Paciente) WHERE u.Nombre="'+paciente+'"RETURN u'
    pacientes = driver.query(q,returns=(client.Node,str,client.Node))
    for p in pacientes:
        print("(%s)" % (p[0]["Nombre"]))
    p1=p[0]

    r='MATCH (u:Doctor) WHERE u.Nombre="'+doctor+'"RETURN u'
    doctores = driver.query(r,returns=(client.Node,str,client.Node))
    for r in doctores:
        print("(%s)" % (r[0]["Nombre"]))
    d1=r[0]
    d1.relationships.create("CONOCE", p1)
    p1.relationships.create("CONOCE", d1)
    

# ------------ QUERYS ---------------

#Esta relacion va a servir para la segunda recomendacion
def relacionDD(doctor, doctor1):
    q='MATCH (u:Doctor) WHERE u.Nombre="'+doctor1+'"RETURN u'
    doctores1 = driver.query(q,returns=(client.Node,str,client.Node))
    for p in doctores1:
        print("(%s)" % (p[0]["Nombre"]))
    p1=p[0]

    r='MATCH (u:Doctor) WHERE u.Nombre="'+doctor+'"RETURN u'
    doctores = driver.query(r,returns=(client.Node,str,client.Node))
    for r in doctores:
        print("(%s)" % (r[0]["Nombre"]))
    d1=r[0]
    d1.relationships.create("CONOCE", p1)
    p1.relationships.create("CONOCE", d1)

#funcion que retorna todos los doctores que tienen cierta especialidad
def queryEsp(especialidad):
    q = 'MATCH (u:Doctor) WHERE u.Especialidad = \"'+ especialidad +'\" RETURN u'
    resultados = driver.query(q, returns=(client.Node))
    if len(resultados) ==0:
        print("\nNo hay doctores con esa especialidad")
    else:
        for r in resultados:
            print("--> %s" % (r[0]["Nombre"]))

#obtiene una lista con los conocidos de los conocidos del paciente
def getConocidosPa(nombrePa):
    conocidosL=[]
    q = 'MATCH (u:Paciente)-[r:CONOCE]->(m:Paciente) WHERE u.Nombre=\"'+ nombrePa +'\" RETURN u, type(r), m'
    conocidos = driver.query(q, returns=(client.Node, str, client.Node))
    if len(conocidos) ==0:
        print("\n La persona que ingreso no tiene conocidos :(")
    else:
        for r in conocidos:
            conocidosL.append(r[2]["Nombre"])
        return conocidos
    

#paciente es el nombre del paciente del cual se va a empezar a buscar
#en esta si no estoy mal hace falta comparar que esos doctores que son el resultado
#sean iguales a los doctores que tenien la especialidad que se busca
#lo que hice fue buscar al paciente que se pide y de alli jalar sus conocidos para despues
#buscar las relaciones de visitas a doctores por cada uno de estos conocidos
def recomendacionPinche1(paciente, especialidad):
    q = 'MATCH (u:Paciente) WHERE u.Nombre = "'+paciente+'" RETURN u'
    paciente = driver.query(q, returns=(client.Node))
    
    listConocidos = getConocidosPa(paciente)

    for i in listConocidos:
        w = 'MATCH (u:Paciente)-[r:FECHA]->(m:Doctor) WHERE u.Nombre="'+ i +'" RETURN u, type(r), m'
        doctores = driver.query(q, returns=(client.Node, str, client.Node))
        
        
    

#funcion para la recomendacion de doctores que conocen a cierto doctor, espero que este correcto vi dos sintaxis distintas 
def recomendacionDoc(especialidad, nombre):
    q = 'MATCH (u:Doctor)-[r:CONOCE]->(m:Doctor) WHERE u.Especialidad = " '+ especialidad +'" AND u.Nombre = "'+ nombre +'" RETURN u, type(r), m'
    resultados = driver.query(q, returns=(client.Node, str, client.Node))

    if(not resultados):
        print("El doctor no se encuentra en la base de datos o no hay relacion entre doctores o la especialidad que ingreso es incorrecta")
    else :
        print("\nLos doctores recomendados son:")
        nombres = ""        
        for r in resultados:
            print("%s, telefono: %s" % (r[0]["Nombre"],r[0]["Telefono"]))   #espero que funcione asi con el [0] porque me base en el link de marco pero no estoy muy segura que sea ese indice que le mete alli
            z = r[0]["Nombre"]

        #Esta segunda query es para los doctores conocidos de los conocidos
        s = 'MATCH (u:Doctor)-[r:CONOCED]->(m:Doctor) WHERE u.Especialidad = " '+ especialidad +'" AND u.Nombre = "'+ nombre +'" RETURN u, type(r), m'
        resultados2 = driver.query(s, returns=(client.Node, str, client.Node))

        for i in resultados2:
            if (z != i[0]["Nombre"]):
                print("%s, telefono: %s" % (i[0]["Nombre"], i[0]["Telefono"]))
