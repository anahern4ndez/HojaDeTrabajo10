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
    
def add_Doctor(nombre, telefono, colegiado, especialidad):
    d = driver.nodes.create(Nombre=nombre, Telefono=telefono, Colegiado=colegiado, Especialidad=especialidad)
    doctores.add(d)
    return d

def add_Medicina(nombre, desdeFecha, hastaFecha, dosis):
    m = driver.nodes.create(Nombre=nombre, desdeFecha=desdeFecha, hastaFecha=desdeFecha, Dosis=dosis)
    medicinas.add(m)
    return m

def relacionDP(paciente, doctor, fecha):
    paciente.relationships.create("VISITA EN %s" %fecha, doctor)

def relacionPM(paciente, medicina):
    paciente.relationships.create("TOMA", medicina)

def relacionDM(doctor, medicina):
    doctor.relationships.create("PRESCRIBE", medicina)

def relacionPP(paciente, paciente1):
    paciente.relationships.create("CONOCEP", paciente1)

#Esta relacion va a servir para la segunda recomendacion
def relacionDD(doctor, doctor1):
    paciente.relationships.create("CONOCE AL DOCTOR", doctor1)

#funcion que retorna todos los doctores que tienen cierta especialidad
def queryEsp(especialidad):
    q = 'MATCH (d:Doctor) WHERE d.especialidad = "+ especialidad +" RETURN d'
    # q = 'MATCH (d:Doctor { Epecialidad: especialidad } RETURN d)'
    resultados = driver.query(q, returns=(client.Node, str, client.Node))
    for r in resultados:
        print("(%s)" % (d[0]["nombre"]))

#funcion para la recomendacion de doctores que conocen a cierto doctor, espero que este correcto vi dos sintaxis distintas 
def recomendacionDoc(especialidad, nombre):
    q = 'MATCH (d:Doctor) WHERE d.especialidad = " + especialidad +" and d.nombre = "+ nombre +" and Doctor-[:CONOCE]->(d) RETURN d, d'
    resultados = db.query(q, returns=(client.Node, str, client.Node))
    for r in resultados:
        print("(%s)" % (d[0]["nombre"]))

