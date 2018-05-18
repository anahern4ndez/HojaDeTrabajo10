#Universidad del valle de Guatemala
#Algoritmos y estructura de datos, seccion:10
#main.py
#Hoja de trabajo 10 - utilizando neo4J y creando recomendaciones
#Maria Fernanda Lopez - 17160
#Ana Lucia Hernandez  - 17138
#Andrea Carolina Arguello - 17801
#18/05/2018

from hdt10 import *

ciclo = 0
while(ciclo==0):
    
    print ('Que desea hacer? \n>>1. Ingresar un doctor \n>>2. Ingresar un paciente \n>>3. Ingresar visita de un paciente a un doctor \n>>4. Consultar doctores por especialidad \n>>5. Ingresar relacion entre personas \n>>6. Salir')

    entrada= raw_input()
    print "\nUsted ingreso: ", entrada,"\n"



    if(entrada=="1"):
        name = raw_input("Ingrese el nombre del doctor: ")
        tel = raw_input("Ingrese el numero de contacto: ")
        col = raw_input("Ingrese el numero de colegiado: ")
        esp = raw_input("Ingrese la especialidad: ")
        add_Doctor(name,tel,col,esp)
        print '**Doctor ingresado**\n'
        ciclo = 0
    elif(entrada=="2"):
        name = raw_input("Ingrese el nombre del paciente: ")
        tel = raw_input("Ingrese el numero de contacto: ")
        add_Paciente(name,tel)
        print '**Paciente ingresado**\n'
        ciclo = 0
    elif(entrada=="3"):
        doctor = raw_input("Ingrese el nombre del doctor visitado: ")
        paciente = raw_input("Ingrese el nombre del paciente: ")
        fecha = raw_input("Ingrese la fecha de la visita: ")
        medicina = raw_input("Ingrese la medicina recetada: ")
        desde = raw_input("La tomara desde: ")
        hasta = raw_input("La tomara hasta: ")
        dosis = raw_input("Ingrese la dosis a tomar: ")
        add_Medicina(medicina,desde,hasta,dosis)
        #hacer query para devolver paciente y guardar en variable pac
        #hacer query para devolver doctor y guardar en variable doc
        #hacer query para la medicina recien ingresada y guardarla en med
           
        ciclo = 0
    elif(entrada=="4"):
        esp = raw_input("Ingrese la especialidad que desea buscar: ")
        queryEsp(esp)
        ciclo = 0
    elif(entrada=="5"):
        persona1 = raw_input("Ingrese la primera persona a relacionar: ")
        persona2 = raw_input("Ingrese la segunda persona a relacionar: ")
        #hacer queries con ambos y crear la relacion
        #relacionPP(p1,p2)
        ciclo = 0
    elif(entrada=="6"):
        print "Feliz dia"
        ciclo = 1
    else:
        print "Ingrese una opcion valida\n"
        ciclo = 0
        
        
        

