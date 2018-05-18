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

def relacionDP(paciente, doctor, fecha):
    paciente.relationships.create("FECHAV %s" %fecha, doctor)

def relacionPM(paciente, medicina):
    paciente.relationships.create("TOMA", medicina)

def relacionDM(doctor, medicina):
    doctor.relationships.create("PRESCRIBE", medicina)

def relacionPP(paciente, paciente1):
    paciente.relationships.create("CONOCEP", paciente1)

#Esta relacion va a servir para la segunda recomendacion
def relacionDD(doctor, doctor1):
    paciente.relationships.create("CONOCED", doctor1)

#funcion que retorna todos los doctores que tienen cierta especialidad
def queryEsp(especialidad):
    q = 'MATCH (u:Doctor) WHERE u.especialidad = "+ especialidad +" RETURN u'
    # q = 'MATCH (d:Doctor { Epecialidad: especialidad } RETURN d)'
    resultados = driver.query(q, returns=(client.Node))
    for r in resultados:
        print("%s" % (r[0]["Nombre"]))

#obtiene una lista con los conocidos de los conocidos del paciente
def getConocidosPa(nombrePa):
    q = 'MATCH (u:Paciente)-[r:CONOCEP]->(m:Paciente) WHERE u.Nombre=" '+ nombrePa +'" RETURN u, type(r), m'
    conocidos = driver.query(q, returns=(client.Node, str, client.Node))
    
    lista=[]
    conocidos2=[]    
    
    for r in conocidos:
        conocidos2.append(r[2]["Nombre"])    #probe con otros numero adentro del [] pero realmente no se si ese hay que cambiarlo o que
        lista.append(r[2]["Nombre"])
        

    for i in lista:
        q = 'MATCH (u:Paciente)-[r:Knows]->(m:Paciente) WHERE u.Nombre="'+i+'" RETURN u, type(r), m'
        conocidos = driver.query(q, returns=(client.Node, str, client.Node))

        for r in conocidos:
            conocidos2.append(r[2]["Nombre"])

    return conocidos2

#obtiene una lista con los doctores que tienen esta especialidad
def getDocsEsp(especialidad):
    q = 'MATCH (u:Doctores) WHERE u.Especialidad = "'+especialidad+'" RETURN u'
    especiales = driver.query(q, returns=(client.Node))

    cont = 0
    lista = []

    for r in especiales:
        cont += 1
        lista.append(r[0]["Nombre"])

    if(cont==0):
        print("\nNo hay doctores con esa especialidad")
    else:
        return lista

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
        w = 'MATCH (u:Paciente)-[r:FECHAV]->(m:Doctor) WHERE u.Nombre="'+i+'" RETURN u, type(r), m'
        doctores = driver.query(q, returns=(client.Node, str, client.Node))
        
        
    

#funcion para la recomendacion de doctores que conocen a cierto doctor, espero que este correcto vi dos sintaxis distintas 
def recomendacionDoc(especialidad, nombre):
    q = 'MATCH (u:Doctor)-[r:CONOCED]->(m:Doctor) WHERE u.Especialidad = " '+ especialidad +'" AND u.Nombre = "'+ nombre +'" RETURN u, type(r), m'
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
            print("%s, telefono: %s" % (i[0]["Nombre"], i[0]["Telefono"])  #igual aqui no se si ese indice deberia de cambiar o como 
                        
                          

#relacionDP(add_Paciente("Pedro", "8349201", "121212"), add_Doctor("Juan", "7439201", "895315", "Internista"))

