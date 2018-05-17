

from neo4jrestclient.client import GraphDatabase
from neo4jrestclient import client
import sys


driver = GraphDatabase("http://localhost:7474", username="neo4j", password="mypassword")


pacientes = driver.labels.create("Paciente")
doctores = driver.labels.create("Doctor")
medicinas = driver.labels.create("Medicinas")

def add_Paciente(nombre, telefono, fecha):
    p1 = driver.nodes.create(Nombre=nombre, Telefono=telefono, Fecha=fecha)
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

def relacionDP(paciente, doctor):
    paciente.relationships.create("VISITA", doctor)

def relacionPM(paciente, medicina):
    paciente.relationships.create("TOMA", medicina)

def relacionDM(doctor, medicina):
    doctor.relationships.create("PRESCRIBE", medicina)

relacionDP(add_Paciente("Pedro", "8349201", "121212"), add_Doctor("Juan", "7439201", "895315", "Internista"))

