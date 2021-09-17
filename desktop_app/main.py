from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pickle
import serial, time
import matplotlib.pyplot as plt
from drawnow import *
import atexit

lista = []

def cruz(tipo, nombreProyecto, conexion, db, user, password):
	cruz = ttk.Frame(notebook)
	notebook.add(cruz, text = "Crear Nueva Pestañar")

	Label(cruz, text = ("  Nombre del Proyecto: " + nombreProyecto), anchor="w", width="40").place(x=50, y=50)
	Label(cruz, text = ("  Comunicación: " + conexion), anchor="w", width="40").place(x=50, y=75)

	nomSensor = StringVar()
	Label(cruz, text = "  Nombre del Sensor: ", anchor="w", width="40", height="2").place(x=50, y=125)
	nombreSensor = Entry(cruz, textvariable = nomSensor,width="20", justify="center").place(x=200, y=134)

	def crear():
		nombreSensor = nomSensor.get()
		crearPestana(tipo, nombreProyecto, nombreSensor, conexion, db, user, password)
		cruz.destroy()

	crearBoton = Button(cruz, text="Crear", command = crear, width="20", justify="center")
	crearBoton.place(x=70, y=200)	

def crearPestana(tipo, nombreProyecto, nomSensor, conexion, db, user, password):

	mas = Button(root, text="+", command = lambda: cruz(tipo, nombreProyecto, conexion, db, user, password), justify="center")
	mas.place(x=976, y=0)
	mas.config(width="2", height="1")

	def Adris(datosTarea):
		values =[]
		plt.ion()
		cnt=0
		#serialArduino = serial.Serial("COM4", 9600)
		def plotValues():
			#plt.title('RPM')
			plt.grid(True)
			plt.ylabel('RPM')
			plt.plot(values, 'r', label='values')
			#plt.legend(loc='upper right')
		def doAtExit():
			#serialArduino.close()
			#print("Close serial")
			#print("serialArduino.isOpen() = " + str(serialArduino.isOpen()))
			exit()

		atexit.register(doAtExit)
		#print("serialArduino.isOpen() = " + str(serialArduino.isOpen()))

		#pre-load dummy data
		for i in range(0,26):
			values.append(0)  
		while True:
		 #   while (serialArduino.inWaiting()==0):
		  #      pass
		   # print("readline()")

			valueRead = datosTarea

		    #check if valid value can be casted
			try:
				valueInInt = int(valueRead)
				print(valueInInt)
				if valueInInt <= 6500:
					if valueInInt >= -1:
						values.append(valueInInt)
						values.pop(0)
						drawnow(plotValues)
					else:
						print("Invalid! negative number")
				else:
					print("Invalid! too large")
			except ValueError:
				print("Invalid! cannot cast")

		plt.subplot()
		plt.show()
	def mandar(datosTarea):

		arduino = serial.Serial("COM4", 9600)
		datoSet = str(datosTarea)
		mensajeSet = 'G' + datoSet
		time.sleep(2)
		arduino.write(mensajeSet.encode())
		time.sleep(2)
		out = arduino.readline(500)
		print(out.decode())
		arduino.close()
		Adris(datosTarea)      
	def tarea():
		nomArch = (nombreProyecto + "." + nomSensor + " - tareas")
		archivo = open(nomArch, "r")
		linea = archivo.readline()
		valores = linea.split("$")

		setPoint = valores[0]

		if unidadTiempo.get() == "s":
			tiempo = valores[1]
			tiempo = tiempo * 1000
		elif unidadTiempo.get() == "m":
			tiempo = valores[1] * 10000
		elif unidadTiempo.get() == "hs":
			tiempo = valores[1] * 100000
		elif unidadTiempo.get() == "d":
			tiempo = valores[1] * 1000000

		datos = (setPoint)
		mandar(datos)		
	def guardar():
		if setPoint.get() != "" and tiempo.get() != "":
			sp = setPoint.get()
			t = tiempo.get()
			lista.append(sp+"$"+t)
			escribirTarea()
			messagebox.showinfo("Agregado", "Se ha agregado una nueva tarea.")
			setPoint.set("")
			tiempo.set("")
			consultar()
			tarea()
	def eliminar():
		nomArch = (nombreProyecto + "." + nomSensor + " - tareas")
		archivo = open(nomArch, "r")
		linea = archivo.readline()
		valores = linea.split("$")
		valorActual = valores[0]

		#if conteliminar.get() != valorActual:
		eliminado = conteliminar.get()
		removido = False
		for elemento in lista:
			arreglo = elemento.split("$")
			if conteliminar.get() == arreglo[0]:
				lista.remove(elemento)
				removido = True
		escribirTarea()
		consultar()
		if removido:
			messagebox.showinfo("Eliminar", "Tarea eliminada: " + eliminado)
		#else:
		#	messagebox.showinfo("Esta tarea no se puede eliminar")			
	def consultar():
		r = Text(pest, width=18, height=16)
		valores = []
		r.insert(INSERT, " SetPoint  Tiempo\n")
		for elemento in lista:
			arreglo = elemento.split("$")
			valores.append(arreglo[0])
			r.insert(INSERT, "  "+arreglo[0]+unidadMedida.get()+"     "+arreglo[1]+unidadTiempo.get()+"\n")
		r.place(x=60, y=280)
		spinEliminar = Spinbox(pest,value=(valores), textvariable=conteliminar, width="13").place(x=285, y=300)
		if lista == []:
			spinEliminar = Spinbox(pest, value=(valores), width="13").place(x=285, y=300)
		r.config(state = DISABLED)	
	def iniciarArchivo():
		nomArch = (nombreProyecto + "." + nomSensor + " - tareas")
		archivo = open(nomArch, "a")
		archivo.close()
	def cargar():
		nomArch = (nombreProyecto + "." + nomSensor + " - tareas")
		archivo = open(nomArch, "r")
		linea = archivo.readline()
		if linea:
			while linea:
				if linea [-1] == 'n':
					linea = linea[:1]
					lista.append(linea)
					linea = archivo.readline()
		archivo.close()
	def escribirTarea():
		nomArch = (nombreProyecto + "." + nomSensor + " - tareas")
		archivo = open(nomArch, "w")
		for elemento in lista:
			archivo.write(elemento + "\n")
		archivo.close()
	def actualizar():
		if unidadMedida.get() == "°C":
			valSet = Spinbox(pest, from_ = 10, to = 20, width="5", textvariable = setPoint, justify="center")
			valSet.place(x=87, y=251)
		elif unidadMedida.get() == "rpm":
			valSet = Spinbox(pest, from_ = 300, to = 1600, width="5", textvariable = setPoint, justify="center")
			valSet.place(x=87, y=251)
		elif unidadMedida.get() == "Ph":
			valSet = Spinbox(pest, from_ = 30, to = 40, width="5", textvariable = setPoint, justify="center")
			valSet.place(x=87, y=251)
		elif unidadMedida.get() == "Od":
			valSet = Spinbox(pest, from_ = 40, to = 50, width="5", textvariable = setPoint, justify="center")
			valSet.place(x=87, y=251)
		else:
			pass
	
		if unidadTiempo.get() == "s":
			valTiempo = Spinbox(pest, from_ = 1, to = 240, width="6", textvariable = tiempo, justify="center")
			valTiempo.place(x=184, y=251)
		elif unidadTiempo.get() == "m":
			valTiempo = Spinbox(pest, from_ = 1, to = 3600, width="6", textvariable = tiempo, justify="center")
			valTiempo.place(x=184, y=251)
		elif unidadTiempo.get() == "hs":
			valTiempo = Spinbox(pest, from_ = 1, to = 72, width="6", textvariable = tiempo, justify="center")
			valTiempo.place(x=184, y=251)
		elif unidadTiempo.get() == "d":
			valTiempo = Spinbox(pest, from_ = 1, to = 5, width="6", textvariable = tiempo, justify="center")
			valTiempo.place(x=184, y=251)
		else:
			pass	
	def eliminarPestana():
		notebook.forget(CURRENT)

	
	pest = ttk.Frame(notebook)
	notebook.add(pest, text = nomSensor)

	iniciarArchivo()
	cargar()
	consultar()

	nomPest = Label(pest, text = ("  Nombre del Proyecto : " + nombreProyecto + "\n" + "  Nombre del sensor : " + nomSensor), width="50").place(x=40, y=20)

	pin = Label(pest, text = "Número del Pin", width="20").place(x=40, y=80)
	numeroPin = IntVar()
	numPin = Spinbox(pest, from_ = 1, to = 40, width="18", textvariable = numeroPin, justify="center").place(x=50, y=102)
	
	numeroSampleo = IntVar()
	etiqueta1 = Label(pest, text = "Sampleo", width="20").place(x=240, y=80)
	numSampleo = Spinbox(pest, from_ = 1, to = 5, width="18", textvariable = numeroSampleo, justify="center").place(x=250, y=102)

	Label(pest, text = "Medicion en", width="20").place(x=40, y=130)
	unidadMedida = 	StringVar()
	combo = ttk.Combobox(pest)
	combo.place(x=50, y=152)
	combo.config(textvariable = unidadMedida, width="18", justify="center")
	combo['values'] = ('°C', 'rpm', 'Ph', 'Od')

	Label(pest, text = "Tiempo en", width="20").place(x=240, y=130)
	unidadTiempo = StringVar()
	combo1 = ttk.Combobox(pest)
	combo1.place(x=250, y=152)
	combo1.config(textvariable = unidadTiempo, width="18", justify="center")
	combo1['values'] = ('s', 'm', 'hs', 'd')

	actuBoton = Button(pest, text="Actualizar", command = actualizar, width="20", justify="center")
	actuBoton.place(x=40, y=190)
	
	elimBoton = Button(pest, text="Eliminar Pestaña", command = eliminarPestana, width="20", justify="center")
	elimBoton.place(x=240, y=190)

	Label(pest, text = "SetPoint").place(x=37, y=250)
	valSet = Spinbox(pest, width="5", textvariable = setPoint, justify="center")
	valSet.place(x=87, y=251)

	Label(pest, text = "Tiempo").place(x=138, y=250)
	valTiempo = Spinbox(pest, width="6", textvariable = tiempo, justify="center")
	valTiempo.place(x=184, y=251)

	agrBoton = Button(pest, text="Agregar", command = guardar, width="15", justify="center")
	agrBoton.place(x=275, y=248)

	delBoton = Button(pest, text="Eliminar", command = eliminar, width="15", justify="center")
	delBoton.place(x=275, y=330)

	grafico1 = Text(pest, width="65", height="15").place(x=430, y=20)
	
	num = IntVar()
	escBoton1 = Radiobutton(pest, text="3Hs", value=1, variable=num, width="7").place(x=930, y=27)
	escBoton2 = Radiobutton(pest, text="12Hs", value=2, variable=num, width="8").place(x=930, y=55)
	escBoton3 = Radiobutton(pest, text="24Hs", value=3, variable=num, width="8").place(x=930, y=83)
	
	grafico2 = Text(pest, width="65", height="15").place(x=430, y=300)

def nuevoProyecto():
	cantPest = notebook.index("end")
	pest = 0
	while pest < cantPest:
		notebook.forget(0)
		pest = pest + 1
	
	nueProyecto = ttk.Frame(notebook)
	notebook.add(nueProyecto, text = "Configuración")

	nomProyecto = StringVar()
	Label(nueProyecto, text = "  Nombre del Proyecto:", anchor="w", width="45", height="2").place(x=50, y=50)
	nombreP = Entry(nueProyecto, textvariable = nomProyecto, width="20", justify="center").place(x=220, y=59)

	nomConexion = StringVar()
	Label(nueProyecto, text = "  Puerto comunicación COM:", anchor="w", width="45", height="2").place(x=50, y=90)
	combo2 = ttk.Combobox(nueProyecto)
	combo2.place(x=220, y=99)
	combo2.config(textvariable = nomConexion , justify="center",width="20")
	combo2['values'] = ('COM3', 'COM4', 'COM5', 'COM6', 'COM7')
	combo2.current(0)

	Label(nueProyecto, text = "  Velocidad de comunicación:", anchor="w", width="45", height="2").place(x=50, y=130)
	velComunicacion = Spinbox(nueProyecto, width="20", justify="center", values = (9600, 14400, 19200)).place(x=220, y=139)

	nomSensor = StringVar()
	Label(nueProyecto, text = "  Nombre Primer Sensor", anchor="w", width="45", height="2").place(x=50, y=170)
	nombreSensor = Entry(nueProyecto, textvariable = nomSensor,width="20", justify="center").place(x=220, y=179)
	
	def crear():
		nombreProyecto = nomProyecto.get()
		nombreConexion = nomConexion.get()
		nombreSensor = nomSensor.get()
		crearPestana("crear", nombreProyecto, nombreSensor, nombreConexion, "", "", "")
		notebook.forget(CURRENT)

	crearBoton = Button(nueProyecto, text="Crear", command = crear, width="20", justify="center")
	crearBoton.place(x=110, y=220)


def abrirProyecto():
	cantPest = notebook.index("end")
	pest = 0
	while pest < cantPest:
		notebook.forget(0)
		pest = pest + 1

	conectProyecto = ttk.Frame(notebook)
	notebook.add(conectProyecto, text = "Configuración")

	nomIp = StringVar()
	Label(conectProyecto, text = "  Dirección de IP:", anchor="w", width="40", height="2").place(x=50, y=50)
	ip = Entry(conectProyecto, textvariable=nomIp, width="20", justify="center").place(x=200, y=59)

	nomBBDD = StringVar()
	Label(conectProyecto, text = "  Nombre de BBDD:", anchor="w", width="40", height="2").place(x=50, y=90)
	nombreBBDD = Entry(conectProyecto, textvariable=nomBBDD, width="20", justify="center").place(x=200, y=99)

	nomUsuario = StringVar()
	Label(conectProyecto, text = "  Nombre de Usuario:", anchor="w", width="40", height="2").place(x=50, y=130)
	nombreUsuario = Entry(conectProyecto, textvariable=nomUsuario, width="20", justify="center").place(x=200, y=139)

	nomContrasena = StringVar()
	Label(conectProyecto, text = "  Contraseña de Usuario:", anchor="w", width="40", height="2").place(x=50, y=170)
	contrasenaUsuario = Entry(conectProyecto, textvariable=nomContrasena, width="20", justify="center").place(x=200, y=179)

	def conectar():
		nombreIp = nomIp.get()
		nombreBBDD = nomBBDD.get()
		nombreUsuario = nomUsuario.get()
		nombreContrasena = nomContrasena.get()
		crearPestana("conectar", "ProyectoOnline", "RPM", nombreIp, nombreBBDD, nombreUsuario, nombreContrasena)
		conectProyecto.destroy()

	conectBoton = Button(conectProyecto, text="Crear", command = conectar, width="20", justify="center")
	conectBoton.place(x=110, y=220)

root = Tk()
root.title("BioNanoReactor")
root.resizable(0, 0)
root.geometry("1000x600")
#root.iconbitmap("BNR1cc.bmp")
setPoint = StringVar()
tiempo = StringVar()
conteliminar = StringVar()
colorLetra ="#FFF"
colorFondo = "#ccc8db"
colorPest = "#ccc8db"
colorAct = "#4a59e0"
root.config(background=colorAct)

notebook = ttk.Notebook(root)
notebook.pack(fill = 'both', expand ='yes')

style = ttk.Style()
style.theme_create( 
					"colPestañas", parent="alt", settings={"TNotebook": {"configure": 
					{"tabmargins": [2, 5, 2, 0] } },"TNotebook.Tab": {"configure": 
					{"padding": [5, 1], "background": colorPest },"map": {"background": 
					[("selected", colorAct)],"expand": [("selected", [1, 1, 1, 0])] } } } )
style.theme_use("colPestañas")

barraMenu = Menu(root)

menuProyecto = Menu(barraMenu, tearoff = 0)
menuProyecto.add_command(label="Nuevo Proyecto", command = nuevoProyecto)
menuProyecto.add_command(label="Abrir Proyecto Online", command = abrirProyecto)
menuProyecto.add_command(label="Cargar Configuraciones")
menuProyecto.add_command(label="Guardar Configuraciones")
menuProyecto.add_command(label="Guardar Configuraciones Como")
menuProyecto.add_command(label="Salir")
barraMenu.add_cascade(label="Proyecto", menu=menuProyecto)

menuEdicion = Menu(barraMenu, tearoff = 0)
menuEdicion.add_command(label="Deshacer")
menuEdicion.add_command(label="Algo más")
menuEdicion.add_command(label="Otra cosa")
barraMenu.add_cascade(label="Edicion", menu=menuEdicion)

menuAyuda = Menu(barraMenu, tearoff = 0)
menuAyuda.add_command(label="Ayuda")
barraMenu.add_cascade(label="Ayuda", menu=menuAyuda)

menuPausa = Menu(barraMenu, tearoff = 0)
barraMenu.add_cascade(label="││", menu=menuPausa)
menuInicio = Menu(barraMenu, tearoff = 0)
barraMenu.add_cascade(label=">", menu=menuInicio)

root.config(menu=barraMenu)

root.mainloop()
