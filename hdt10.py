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
    relacionPM(paciente,medicina)
    relacionDM(doctor,medicina)

# ------------ CREACION RELACIONES ---------------
def visitaDP(paciente, doctor, fecha):
    q = 'MATCH (u:Paciente), (s:Doctor) WHERE u.Nombre=\"'+ paciente +'\" AND s.Nombre=\"'+ doctor +'\" RETURN u,s'
    resultados = driver.query(q, returns=(client.Node, client.Node))
    for i in resultados:
        p1 = i[0]
        d1 = i[1]
        p1.relationships.create("VISITA", d1)
    

def relacionPM(paciente, medicina):
    
    q='MATCH (u:Paciente), (s:Medicinas) WHERE u.Nombre=\"'+ paciente +'\" AND s.Nombre= \"'+ medicina +'\"RETURN u,s'
    pacientes = driver.query(q,returns=(client.Node, client.Node))
    for i in pacientes:
        p1 = i[0]
        d1 = i[1]
        p1.relationships.create("TOMA", d1)


def relacionDM(doctor, medii):
    q='MATCH (u:Doctor) WHERE u.Nombre=\"'+ doctor +'\" RETURN u'
    doctores = driver.query(q,returns=(client.Node))
    for i in doctores:
        p1=i[0]

    r='MATCH (u:Medicinas) WHERE u.Nombre=\"'+ medii +'\" RETURN u'
    medicinas = driver.query(r,returns=(client.Node))

    for i in medicinas:
        med=i[0]
        p1.relationships.create("PRESCRIBE", med)

def relacionPP(paciente, paciente1):
    q='MATCH (u:Paciente) WHERE u.Nombre=\"'+ paciente +'\" RETURN u'
    pacientes = driver.query(q,returns=(client.Node))

    for i in pacientes:
        p1=i[0]

    r='MATCH (u:Paciente) WHERE u.Nombre=\"'+ paciente1 +'\" RETURN u'
    pacientes2 = driver.query(r,returns=(client.Node))

    for i in pacientes2:
        p2=i[0]
        p1.relationships.create("CONOCE", p2)
  

def relacionDP(doctor, paciente):
    q='MATCH (u:Paciente) WHERE u.Nombre= \"'+ paciente +'\" RETURN u'
    pacientes = driver.query(q,returns=(client.Node))
    
    for i in pacientes:
        p1=i[0]

    r='MATCH (u:Doctor) WHERE u.Nombre=\"'+ doctor +'\" RETURN u'
    doctores = driver.query(r,returns=(client.Node))
    for i in doctores:
        d1=i[0]
        d1.relationships.create("CONOCE", p1)
  

#Esta relacion va a servir para la segunda recomendacion
def relacionDD(doctor, doctor1):
    q='MATCH (u:Doctor) WHERE u.Nombre=\"'+ doctor1 +'\" RETURN u'
    doctores1 = driver.query(q,returns=(client.Node,str,client.Node))
    for p in doctores1:
        print("(%s)" % (p[0]["Nombre"]))
    p1=p[0]

    r='MATCH (u:Doctor) WHERE u.Nombre=\"'+ doctor +'\" RETURN u'
    doctores = driver.query(r,returns=(client.Node,str,client.Node))
    for r in doctores:
        print("(%s)" % (r[0]["Nombre"]))
    d1=r[0]
    d1.relationships.create("CONOCE", p1)
    

# ------------ QUERYS ---------------

#funcion que retorna todos los doctores que tienen cierta especialidad
def queryEsp(especialidad):
    doctores = [] #nombres de los doctores
    q = 'MATCH (u:Doctor) WHERE u.Especialidad = \"'+ especialidad +'\" RETURN u'
    resultados = driver.query(q, returns=(client.Node))
    if len(resultados) ==0:
        print("\nNo hay doctores con esa especialidad")
    else:
        for r in resultados:
            print("--> %s" % (r[0]["Nombre"]))
            doctores.append(r[0]["Nombre"])
        return doctores

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
        return conocidosL
    

#paciente es el nombre del paciente del cual se va a empezar a buscar
#en esta si no estoy mal hace falta comparar que esos doctores que son el resultado
#sean iguales a los doctores que tenien la especialidad que se busca
#lo que hice fue buscar al paciente que se pide y de alli jalar sus conocidos para despues
#buscar las relaciones de visitas a doctores por cada uno de estos conocidos


# ---------------- RECOMENDACIONES ----------------------
def recomendacionConocidosPaciente(nombrePa, especialidad):   
    z = ""
    nodoPaciente = None
    conocidos = [] #conocidos del doctor ingresado, guarda strings
    doctores =[] #doctores que coinciden con una especialidad, guarda strings
    conocidosDeConocidos =[] #personas que son conocidos de conocidos del doctor, guarda strings
    recomendados =[] #doctores recomendados, guarda strings
    q = 'MATCH (u:Paciente) WHERE u.Nombre = \"'+nombrePa+'\" RETURN u'
    pacientes = driver.query(q, returns=(client.Node))
    for p in pacientes:
        nodoPaciente = p
    
    listConocidos = getConocidosPa(nombrePa)
    doctores = queryEsp(especialidad) 

    if (listConocidos != None): #Si el paciente ingresado conoce a mas de alguien
        for i in listConocidos:
            w = 'MATCH (u:Paciente)-[r:CONOCE]->(m:Paciente) WHERE u.Nombre=\"'+ i +'\" RETURN m'
            conocidos2 = driver.query(q, returns=(client.Node))
            for cc in conocidos2:
                conocidosDeConocidos.append(cc[0]["Nombre"])
        #Primero se hara el query de si a cada doctor de una especialidad, lo ha visitado alguno de los conocidos del paciente
        for j in range(len(doctores)):
            for i in range(len(conocidos)):
                t = 'MATCH (u:Paciente)-[r:VISITA]->(m:Doctor) WHERE u.Nombre=\"'+ conocidos[i] +'\" AND m.Nombre=\"'+ doctores[j] +'\" RETURN u,m'
                recomendados1 = driver.query(t, returns=(client.Node, client.Node))
                for found in recomendados1:
                    recomendados.append(found[1]["Nombre"])

        #Luego se hara el query de si a cada doctor de una especialidad, lo ha visitado alguno de los conocidos de algun conocido del paciente
        for j in range(len(doctores)):
            for i in range(len(conocidosDeConocidos)):
                t = 'MATCH (u:Paciente)-[r:VISITA]->(m:Doctor) WHERE u.Nombre=\"'+ conocidosDeConocidos[i] +'\" AND m.Nombre=\"'+ doctores[j] +'\" RETURN u,m'
                recomendados1 = driver.query(t, returns=(client.Node, client.Node))
                for found in recomendados1:
                    recomendados.append(found[1]["Nombre"])
        #Impresion de los doctores encontrados (aunque se repitan)
        for s in recomendados:
            print("Nombre del Doctor: %s" %(s))            
            
        
#funcion para la recomendacion de doctores que conocen a cierto doctor
def recomendacionConocidosDoctor(especialidad, nombre):
    z = ""
    q = 'MATCH (u:Doctor)-[r:CONOCE]->(m:Doctor) WHERE u.Especialidad = \"'+ especialidad +'\" AND u.Nombre = \"'+ nombre +'\" RETURN u, type(r), m'
    resultados = driver.query(q, returns=(client.Node, str, client.Node))

    if(len(resultados) == 0):
        print("El doctor no se encuentra en la base de datos o no hay relacion entre doctores o la especialidad que ingreso es incorrecta")
    else :
        print("\nLos doctores recomendados son:")
        nombres = ""        
        for r in resultados:
            print("%s, telefono: %s" % (r[0]["Nombre"],r[0]["Telefono"]))   #espero que funcione asi con el [0] porque me base en el link de marco pero no estoy muy segura que sea ese indice que le mete alli
            z = r[0]["Nombre"]

        #Esta segunda query es para los doctores conocidos de los conocidos
        s = 'MATCH (u:Doctor)-[r:CONOCE]->(m:Doctor) WHERE u.Especialidad = \"'+ especialidad +'\" AND u.Nombre = \"'+ nombre +'\" RETURN u, type(r), m'
        resultados2 = driver.query(s, returns=(client.Node, str, client.Node))

        for i in resultados2:
            if (z != i[0]["Nombre"]):
                print("%s, telefono: %s" % (i[0]["Nombre"], i[0]["Telefono"]))
