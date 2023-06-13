# Autores: Jose Mario / John Sebastián

""" MODULOS """
import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as MessageBox
from validate_email_address import validate_email #libreria para validar email
from fpdf import FPDF #libreria para crear pdf
import smtplib # librerias para el envio de archivos por correo
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
import base64 # libreria para codificar objetos
from datetime import datetime, timedelta
import time


""" FUNCIONES """

# FUNCION VALIDAR CORREOS
# ENTRADAS: Recibe un correo electronico.
# SALIDAS: Retorna True si es valido y existe, False si no es valido, None si no existe.
def validar_existencia_correo(correo):
     es_valido = validate_email(correo) # seccion que valida solo el formato
     if es_valido == True:
         existe = validate_email(correo,verify = True) # valida existencia gracias a verify
         return existe
     return False

# FUNCION VALIDAR FECHAS
# ENTRADAS: Recibe la fecha a validar.
# SALIDAS: True si es valido, False si no es valido.
def validar_fecha(fecha):
    global fecha_v
    try:
        # Intentamos crear un objeto de fecha a partir de la cadena proporcionada
        datetime.datetime.strptime(fecha, '%Y-%m-%d')
        fecha_v = True
    except ValueError:
        fecha_v = False
        MessageBox.showerror("Fecha","Fecha Invalida")
    
# FUNCION QUE GENERA LAS CITAS POSIBLES
# ENTRADAS: datos de la configuracion y del sistema.
# SALIDAS: lista de fechas.   
def generar_lista_fechas_intervalo(inicio, fin, hora_inicio, hora_fin, intervalo_minutos):
    lista_fechas = []
    fecha_actual = inicio
    hora_actual = datetime.strptime(hora_inicio, "%H:%M")

    while fecha_actual <= fin:
        fecha_con_hora = datetime.combine(fecha_actual, hora_actual.time())
        lista_fechas.append(fecha_con_hora)
        hora_actual += timedelta(minutes=intervalo_minutos)

        if hora_actual.time() > datetime.strptime(hora_fin, "%H:%M").time():
            fecha_actual += timedelta(days=1)
            hora_actual = datetime.strptime(hora_inicio, "%H:%M")

    return lista_fechas

# FUNCION QUE AGREGA UN AÑO SI EL MES ES MAYOR A 12
# ENTRADAS: Recibe la fecha separada.
# SALIDAS: Retorna la fecha arreglada.
def validar_fecha_fin(ano, mes_sumado, dia):
    if mes_sumado > 12:
        ano += 1
        mes_sumado -= 12
    return ano, mes_sumado, dia

# FUNCION CREAR NODO
# ENTRADAS: Recibe un valor para convertirlo en nodo con dos hijos.
# SALIDAS: Retorna el nodo creado.
def crear_nodo(valor):
        hijo_izquierdo = None
        hijo_derecho = None
        return [valor, hijo_izquierdo, hijo_derecho]

# FUNCION INSERTAR NODO !! ARREGLAR FECHAS
# ENTRADAS: Recibe el árbol y el valor a agregar.
# SALIDAS: Retorna el árbol con el nuevo nodo.
def insertar_nodo(arbol, valor):
    if arbol == None:
        return crear_nodo(valor)
    else:
        if valor[0] <= arbol[0][0]:
            arbol[1] = insertar_nodo(arbol[1], valor)
        else:
            arbol[2] = insertar_nodo(arbol[2], valor)
        return arbol

# FUNCION QUE PROGRAMA UNA CITA Y LA GUARDA EN UN ÁRBOL DE BUSQUEDA BINARIA (ABB)
# ENTRADAS: Recibe los datos que se guardarán en el nodo.
# SALIDAS: Guarda los datos en un nodo del árbol (ABB).
def programar_cita_nueva(dato1, dato2, dato3, dato4, dato5, dato6, dato7, dato8, dato9):
    if dato9 == "":
        MessageBox.showerror("ERROR", "No se ingresó ningún dato de fecha y hora.")
        return
    
    archivo = open("registros.dat", "r")
    datos_originales = archivo.read()
    datos_originales = eval(datos_originales)
    archivo.close()
    datos_originales["num_citas"] = datos_originales["num_citas"] + 1
    archivo = open("registros.dat", "w")
    archivo.write(str(datos_originales))
    archivo.close()

    dato_nodo = [datos_originales["num_citas"], dato1, dato2, dato3, dato4, dato5, dato6, dato7, dato8, dato9]
    print(dato_nodo)

    archivo = open("arbol_citas.dat", "r")
    arbol = archivo.read()
    arbol = eval(arbol)
    archivo.close()

    arbol = insertar_nodo(arbol, dato_nodo)

    archivo = open("arbol_citas.dat", "w")
    archivo.write(str(arbol))
    archivo.close()

    MessageBox.showinfo("ESTADO", "Se ha programado la nueva cita.")

def aprobar_fecha_hora(fechahora, lista_intervalos):
    if len(fechahora[1]) == 1:
        fechahora[1] = "0" + fechahora[1]
    if len(fechahora[2]) == 1:
        fechahora[2] = "0" + fechahora[2]
    if len(fechahora[3]) == 1:
        fechahora[3] = "0" + fechahora[3]
    if len(fechahora[4]) == 1:
        fechahora[4] = "0" + fechahora[4]

    nuevo_texto = fechahora[0] + "-" + fechahora[1] + "-" + fechahora[2] + " " + fechahora[3] + ":" + fechahora[4] + ":00"
    
    if nuevo_texto in lista_intervalos:
        return True
    else:
        return False
    
def descomponer_h_m(lista):
    horas = int(lista[-2])
    mins = int(lista[-1])
    suma = horas * 3600
    suma += mins * 60

    lista = lista[:-2]
    lista.append(suma)
    return lista

""" FUNCION COMPLETA DEL BOTÓN PROGRAMAR CITAS
# ENTRADAS: Lee los datos de la cita a agregar.
# SALIDAS: Dependiendo del usuario, guarda la cita o no hace nada. """
def programar_citas():

    # FUNCION QUE VALIDA LOS DATOS DE LA CITA ANTES DE PODER GUARDARLA
    # ENTRADAS: Lee los datos agregados.
    # SALIDAS: Llama a la función de agregar la cita o si no, retorna un error correspondiente.
    def validar_datos_cita():
        global manual, valores_lista

        # Validar el número de placa.
        dato2 = entry2.get()
        if dato2 == "":
            MessageBox.showerror("ERROR", "Dato de placa inválido.")
            return
        if len(dato2) > 8 or len(dato2) < 1:
            MessageBox.showerror("ERROR", "Dato de placa inválido.")
            return
        
        # Validar la marca del vehículo.
        dato4 = entry4.get()
        if dato4 == "":
            MessageBox.showerror("ERROR", "Marca de vehículo inválida.")
            return
        if len(dato4) > 15 or len(dato4) < 3:
            MessageBox.showerror("ERROR", "Marca de vehiculo inválida.")
            return

        # Validar modelo del vehículo.
        dato5 = entry5.get()
        if dato5 == "":
            MessageBox.showerror("ERROR", "Modelo del vehículo inválido.")
            return
        if len(dato5) > 15 or len(dato5) < 1:
            MessageBox.showerror("ERROR", "Modelo del vehiculo inválido.")
            return
        
        # Validar propietario del vehículo.
        dato6 = entry6.get()
        if dato6 == "":
            MessageBox.showerror("ERROR", "Propietario del vehículo inválido.")
            return
        if len(dato6) > 40 or len(dato6) < 6:
            MessageBox.showerror("ERROR", "Propietario del vehiculo inválido.")
            return
        
        # Validar teléfono.
        dato7 = entry7.get()
        if dato7 == "":
            MessageBox.showerror("ERROR", "Teléfono inválido.")
            return
        if len(dato7) > 20 or len(dato7) < 6:
            MessageBox.showerror("ERROR", "Teléfono inválido.")
            return
        
        # Validar correo electrónico.
        dato8 = entry8.get()
        if dato8 == "":
            MessageBox.showerror("ERROR", "Correo electrónico inválido o inexistente.")
            return
        else:
            """resultado = validar_existencia_correo(dato8)
            if resultado == None:
                MessageBox.showerror("ERROR", "Correo electrónico inválido o inexistente.")
                return
            if resultado == False:
                MessageBox.showerror("ERROR", "Correo electrónico inválido o inexistente.")
                return
            if resultado == True:"""
            pass    
            
        # Validar dirección física.
        dato9 = entry9.get()
        if dato9 == "":
            MessageBox.showerror("ERROR", "Dirección física inválida.")
            return
        if len(dato9) > 40 or len(dato9) < 10:
            MessageBox.showerror("ERROR", "Dirección física inválida.")
            return
        
        # Guardar cita.
        if manual == True:
            dia.get()
            mes.get()
            año.get()
            hora.get()
            minutos.get()
            if aprobar_fecha_hora([año.get(), mes.get(), dia.get(), hora.get(), minutos.get()], valores_lista):
                descompuesto = descomponer_h_m([año.get(), mes.get(), dia.get(), hora.get(), minutos.get()])
                programar_cita_nueva(dato2, entry3.get(), dato4, dato5, dato6, dato7, dato8, dato9, descompuesto)
            else:
                MessageBox.showerror("ERROR", "Cita no disponible para programar.")
        else:
            fecha_hora_automatico(dato2, entry3.get(), dato4, dato5, dato6, dato7, dato8, dato9, valores_lista)
    
    def fecha_hora_automatico(dato1, dato2, dato3, dato4, dato5, dato6, dato7, dato8, lista_automaticos):

        def programar_auto(dato1, dato2, dato3, dato4, dato5, dato6, dato7, dato8, dato9):
            print(dato9)
            ano_separado = dato9[:4]
            mes_separado = dato9[5:7]
            dia_separado = dato9[8:10]
            hora_separada = dato9[11:13]
            minutos_separados = dato9[14:16]
            descompuesto = [ano_separado, mes_separado, dia_separado, hora_separada, minutos_separados]
            programar_cita_nueva(dato1, dato2, dato3, dato4, dato5, dato6, dato7, dato8, descompuesto)
            ventana_automatico.destroy()
            return
        
        ventana_automatico = Toplevel()
        ventana_automatico.geometry("500x300")
        ventana_automatico.resizable(False, False)

        Label(ventana_automatico, text= "Seleccione una opción de fecha y hora:", font= ("Franklin Gothic Demi", 16)).pack()
        combo_auto = ttk.Combobox(ventana_automatico, values= lista_automaticos, state= "readonly", width= 50)
        combo_auto.pack()
        Button(ventana_automatico, text= "Guardar", command= lambda: programar_auto(dato1, dato2, dato3, dato4, dato5, dato6, dato7, dato8, combo_auto.get())).pack()

        combo_auto.set(lista_automaticos[0])
        ventana_automatico.mainloop()
        return

    def activar_manual():
        global manual
        manual = True

        dia.config(state= "readonly")
        mes.config(state= "readonly")
        año.config(state= "readonly")
        hora.config(state= "readonly")
        minutos.config(state= "readonly")
        return
    
    def desactivar_manual():
        global manual
        manual = False

        dia.config(state= "disabled")
        mes.config(state= "disabled")
        año.config(state= "disabled")
        hora.config(state= "disabled")
        minutos.config(state= "disabled")
        return
    
    def cerrar_citas():
        ventana_principal.deiconify()
        ventana_programar_citas.destroy()
        return
    
    # FUNCION QUE VALIDA LA LONGITUD DE UN TEXTO EN UN CAMPO DE ESCRITURA
    # ENTRADAS: Recibe el texto a validar.
    # SALIDAS: True si es correcto, False de lo contrario.
    def validar_texto(texto):
        return len(texto) <= 40
    
    # Definir los tipos de vehículos en una lista.
    tipos_de_vehículos = ["Automovil particular y vehiculo de carga liviana (<= 3500 kg)", \
                          "Automovil particular y vehiculo de carga liviana (3500 kg > 8000 kg)", \
                            "Vehiculo de carga pesada y cabezales (>= 8000 kg)", "Taxis", \
                                "Autobuses, buses y microbuses", "Motocicletas", "Equipo especial de obras", \
                                    "Equipo especial agricola (maquinaria agricola)"]

    # Esconder la ventana principal.
    ventana_principal.iconify()

    # Crear la ventana de programar citas.
    ventana_programar_citas = Toplevel()
    ventana_programar_citas.geometry("600x700")
    ventana_programar_citas.resizable(False, False)
    ventana_programar_citas.title("Programar Citas")
    
    # Validación de texto.
    texto = (ventana_programar_citas.register(validar_texto), "%P")

    # Título.
    Label(ventana_programar_citas, text= "Programar Citas", font= ("Arial", 16)).place(x= 220, y= 10)

    # Campos de información de las citas.
    Label(ventana_programar_citas, text= "Tipo de cita: ", font= ("Franklin Gothic Demi", 12)).place(x= 10, y= 50)
    tipo_cita = StringVar(value = 0) 
    primera = Radiobutton(ventana_programar_citas, text="Primera Vez", variable=tipo_cita, value="Primera Vez")
    primera.place(x= 110, y= 53)
    reinspeccion = Radiobutton(ventana_programar_citas, text="Reinspeccion", variable=tipo_cita, value="Reinspeccion")
    reinspeccion.place(x= 200, y= 53)

    Label(ventana_programar_citas, text= "Número de placa: ",font= ("Franklin Gothic Demi", 12)).place(x= 10, y= 100)
    entry2 = Entry(ventana_programar_citas, width=40,validate="key", validatecommand=texto)
    entry2.place(x= 145, y= 105)

    Label(ventana_programar_citas, text= "Tipo de vehículo: ", font= ("Franklin Gothic Demi", 12)).place(x= 10, y= 150)
    entry3 = ttk.Combobox(ventana_programar_citas, values= tipos_de_vehículos, width= 60, state= "readonly")
    entry3.place(x= 140, y= 155)

    Label(ventana_programar_citas, text= "Marca del vehículo: ",font= ("Franklin Gothic Demi", 12)).place(x= 10, y= 200)
    entry4 = Entry(ventana_programar_citas, width= 40,validate="key", validatecommand=texto)
    entry4.place(x= 160, y= 205)

    Label(ventana_programar_citas, text= "Modelo: ", font= ("Franklin Gothic Demi", 12)).place(x= 10, y= 250)
    entry5 = Entry(ventana_programar_citas, width= 40,validate="key", validatecommand=texto)
    entry5.place(x= 80, y= 255)

    Label(ventana_programar_citas, text= "Propietario: ", font= ("Franklin Gothic Demi", 12)).place(x= 10, y= 300)
    entry6 = Entry(ventana_programar_citas, width= 40,validate="key", validatecommand=texto)
    entry6.place(x= 110, y= 305)

    Label(ventana_programar_citas, text= "Teléfono: ", font= ("Franklin Gothic Demi", 12)).place(x= 10, y= 350)
    entry7 = Entry(ventana_programar_citas, width= 40,validate="key", validatecommand=texto)
    entry7.place(x= 90, y= 355)

    Label(ventana_programar_citas, text= "Correo electrónico: ", font= ("Franklin Gothic Demi", 12)).place(x= 10, y= 400)
    entry8 = Entry(ventana_programar_citas, width= 40,validate="key", validatecommand=texto)
    entry8.place(x= 160, y= 405)

    Label(ventana_programar_citas, text= "Dirección física: ", font= ("Franklin Gothic Demi", 12)).place(x= 10, y= 450)
    entry9 = Entry(ventana_programar_citas, width= 40,validate="key", validatecommand=texto)
    entry9.place(x= 140, y= 455)

    # Opciones de fechas y horas.
    opciones_dia = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
    opciones_mes = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    opciones_año = ["2023","2024","2025"]
    opciones_hora = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    opciones_minutos = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]

    Label(ventana_programar_citas, text= "DIA:", font= ("Arial", 12)).place(x= 10, y= 540)
    dia = ttk.Combobox(ventana_programar_citas, values= opciones_dia, state= "readonly", width= 5)
    dia.place(x= 50, y= 542)

    mes = ttk.Combobox(ventana_programar_citas, values= opciones_mes, state= "readonly", width= 5)
    mes.place(x= 160, y= 542)
    Label(ventana_programar_citas, text= "MES:", font= ("Arial", 12)).place(x= 110, y= 540)

    año = ttk.Combobox(ventana_programar_citas, values= opciones_año, state= "readonly", width= 5)
    año.place(x= 270, y= 542)
    Label(ventana_programar_citas, text= "AÑO:", font= ("Arial", 12)).place(x= 220, y= 540)

    hora = ttk.Combobox(ventana_programar_citas, values= opciones_hora, state= "readonly", width= 5)
    hora.place(x= 390, y= 542)
    Label(ventana_programar_citas, text= "HORA:", font= ("Arial", 12)).place(x= 330, y= 540)

    minutos = ttk.Combobox(ventana_programar_citas, values= opciones_minutos, state= "readonly", width= 5)
    minutos.place(x= 535, y= 542)
    Label(ventana_programar_citas, text= "MINUTOS:", font= ("Arial", 12)).place(x= 450, y= 540)

    Button(ventana_programar_citas, text= "Guardar", command= lambda:  validar_fecha(fecha = (año.get() + "-" + mes.get() + "-" + dia.get())))

    tipo_programacion = StringVar()
    Label(ventana_programar_citas, text= "Fecha y hora de la cita: ", font= ("Franklin Gothic Demi", 12)).place(x= 10, y= 500)
    boton_manual = Radiobutton(ventana_programar_citas, text= "Manual", variable= tipo_programacion, value= "manual", command= lambda: activar_manual())
    boton_manual.place(x= 190, y= 502)
    boton_auto = Radiobutton(ventana_programar_citas, text= "Automático", variable= tipo_programacion, value= "auto", command= lambda: desactivar_manual())
    boton_auto.place(x= 270, y= 502)

    # Botones de interacción.
    Button(ventana_programar_citas, text= "Programar Cita", width= 20, height= 2, font= ("Franklin Gothic Demi", 10), command= lambda: validar_datos_cita()).place(x= 140, y= 600)
    Button(ventana_programar_citas, text= "Cerrar ventana", width= 20, height= 2, font= ("Franklin Gothic Demi", 10), command= lambda: cerrar_citas()).place(x= 300, y= 600)

    # Asignar valores por defecto a las opciones.
    tipo_cita.set("Primera Vez")
    entry3.set("Automovil particular y vehiculo de carga liviana (<= 3500 kg)")
    tipo_programacion.set("manual")
    dia.set("01")
    mes.set("01")
    año.set("2023")
    hora.set(0)
    minutos.set(0)

    # Loop de la ventana.
    ventana_programar_citas.mainloop()
    return

""" FUNCION PARA ABRIR LA VENTANA DE CONFIGURACION DEL SISTEMA
# ENTRADAS: Lee las opciones seleccionadas por el usuario.
# SALIDAS: Guarda los cambios en un archivo predefinido. """
def ventana_configuracion_sistema():

    # FUNCION QUE GUARDA LA OPCION DE LINEAS DE TRABAJO
    # ENTRADAS: Recibe el nuevo dato de lineas de trabajo.
    # SALIDAS: Si la opción es válida se guarda, de lo contrario envía el error respectivo.
    def guardar_lineas_trabajo(dato):
        archivo = open("configuración_reteve.dat", "r")
        datos_originales = archivo.read()
        datos_originales = eval(datos_originales)
        dato_comparar = datos_originales[0]
        archivo.close()

        if int(dato) >= dato_comparar:
            archivo = open("configuración_reteve.dat", "w")
            datos_originales[0] = int(dato)
            archivo.write(str(datos_originales))
            archivo.close()
            MessageBox.showinfo("ESTADO", "Los datos se han guardado correctamente.")
        else:
            MessageBox.showerror("ERROR", "No se puede ejecutar la acción.")
            pass
    
    # FUNCION QUE GUARDA LAS HORAS DE TRABAJO DE LA ESTACIÓN
    # ENTRADAS: Recibe la hora inicial y la hora final.
    # SALIDAS: Si la opción es válida se guarda, de lo contrario envía el error respectivo.
    def guardar_horas(dato1, dato2):
        inicial = int(dato1[0:2])
        final = int(dato2[0:2])

        if final >= inicial:
            archivo = open("configuración_reteve.dat", "r")
            datos_originales = archivo.read()
            datos_originales = eval(datos_originales)
            archivo.close()

            archivo = open("configuración_reteve.dat", "w")
            datos_originales[1] = dato1
            datos_originales[2] = dato2
            archivo.write(str(datos_originales))
            archivo.close()

            MessageBox.showinfo("ESTADO", "Los datos se han guardado correctamente.")
        else:
            MessageBox.showerror("ERROR", "No se pudo guardar \n(hora inicial mayor que la final).")
        return

    # FUNCION QUE GUARDA OPCIONES DE LA CONFIGURACIÓN
    # ENTRADAS: Recibe el dato a guardar y el índice en el archivo que corresponde.
    # SALIDAS: Si la opción es válida se guarda, de lo contrario envía el error respectivo.
    def guardar_general(dato, indice):
        if dato != "":
            if indice == 7:
                try:
                    dato = float(dato)
                except:
                    MessageBox.showerror("ERROR", "No hay ningún dato registrado o es un dato incorrecto.")
                    return

                if dato < 0 or dato > 20:
                    MessageBox.showerror("ERROR", "El dato debe estar entre 0 y 20.")
                    return
            elif indice != 3:
                try:
                    dato = int(dato)
                except:
                    MessageBox.showerror("ERROR", "No hay ningún dato registrado o es un dato incorrecto.")
                    return

                if dato <= 0:
                    MessageBox.showerror("ERROR", "El dato debe ser mayor a 0.")
                    return
            else:
                pass

            archivo = open("configuración_reteve.dat", "r")
            datos_originales = archivo.read()
            datos_originales = eval(datos_originales)
            archivo.close()

            archivo = open("configuración_reteve.dat", "w")
            datos_originales[indice] = dato
            archivo.write(str(datos_originales))
            archivo.close()

            MessageBox.showinfo("ESTADO", "Los datos se han guardado correctamente.")
        else:
            MessageBox.showerror("ERROR", "No hay ningún dato registrado o es un dato incorrecto.")
        return
    
    # FUNCION QUE GUARDA CAMBIOS EN LAS TARIFAS DE VEHÍCULOS
    # ENTRADAS: Recibe el dato a guardar y el índice en el archivo que corresponde.
    # SALIDAS: Si la opción es válida se guarda, de lo contrario envía el error respectivo.
    def guardar_tarifas(dato, indice):
        if dato == "":
            MessageBox.showerror("ERROR", "No hay ningún dato registrado o es un dato incorrecto.")
            return
        try:
            dato = int(dato)
        except:
            MessageBox.showerror("ERROR", "No hay ningún dato registrado o es un dato incorrecto.")
            return
        
        if dato <= 0:
            MessageBox.showerror("ERROR", "El dato debe ser mayor a 0.")
            return
        
        archivo = open("configuración_reteve.dat", "r")
        datos_originales = archivo.read()
        datos_originales = eval(datos_originales)
        archivo.close()

        archivo = open("configuración_reteve.dat", "w")
        datos_originales[8][indice] = dato
        print(datos_originales)
        archivo.write(str(datos_originales))
        archivo.close()

        MessageBox.showinfo("ESTADO", "Los datos se han guardado correctamente.")
        return
    
    # Crear la ventana de configuración.
    ventana_config = Toplevel()
    ventana_config.geometry("500x700")
    ventana_config.resizable(False, False)
    ventana_config.title("Configuración del sistema")

    # Crear un frame principal.
    frame_config = Frame(ventana_config)
    frame_config.pack(fill= BOTH, expand= 1)

    # Crear un canvas.
    canvas_config = Canvas(frame_config)
    canvas_config.pack(side= LEFT, fill= BOTH, expand= 1)

    # Crear el scrollbar en el canvas.
    scrollbar_config = Scrollbar(frame_config, orient= VERTICAL, command= canvas_config.yview)
    scrollbar_config.pack(side= RIGHT, fill= Y)

    # Configurar el canvas.
    canvas_config.configure(yscrollcommand= scrollbar_config.set)
    canvas_config.bind("<Configure>", lambda e: canvas_config.configure(scrollregion= canvas_config.bbox("all")))

    # Crear otro frame dentro del canvas.
    segundo_frame_config = Frame(canvas_config)

    # Agregar el nuevo frame a una ventana en el canvas.
    canvas_config.create_window((0, 0), window= segundo_frame_config, anchor= "nw")

    """ Opciones de configuración. """
    # Título.
    Label(segundo_frame_config, text="").pack()
    Label(segundo_frame_config, text="Configuración del sistema", font=("Franklin Gothic Demi", 14)).pack()

    # Líneas de trabajo en la estación.
    opciones_lineas_trabajo = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()
    Label(segundo_frame_config, text="Cantidad de líneas de trabajo en la estación:", font=("Arial", 12)).pack()
    combo_lineas = ttk.Combobox(segundo_frame_config, values= opciones_lineas_trabajo, state="readonly")
    combo_lineas.pack()
    Label(segundo_frame_config, text="").pack()
    Button(segundo_frame_config, text= "Guardar", command= lambda: guardar_lineas_trabajo(combo_lineas.get())).pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()

    # Horario de la estación.
    opciones_horario = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]
    Label(segundo_frame_config, text="Horario de la estación:", font=("Arial", 12)).pack()
    Label(segundo_frame_config, text="Hora inicial:", font=("Arial", 8)).pack()
    combo_hora_inicial = ttk.Combobox(segundo_frame_config, values= opciones_horario, state="readonly")
    combo_hora_inicial.pack()
    Label(segundo_frame_config, text="Hora final:", font=("Arial", 8)).pack()
    combo_hora_final = ttk.Combobox(segundo_frame_config, values= opciones_horario, state="readonly")
    combo_hora_final.pack()
    Label(segundo_frame_config, text="").pack()
    Button(segundo_frame_config, text= "Guardar", command= lambda: guardar_horas(combo_hora_inicial.get(), combo_hora_final.get())).pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()

    # Minutos por cada cita de revisión.
    opciones_minutos_cita = ["00:05", "00:10", "00:15", "00:20", "00:25", "00:30", "00:35", "00:40", "00:45"]
    Label(segundo_frame_config, text="Minutos por cada cita de revisión:", font=("Arial", 12)).pack()
    combo_minutos_cita = ttk.Combobox(segundo_frame_config, values= opciones_minutos_cita, state="readonly")
    combo_minutos_cita.pack()
    Label(segundo_frame_config, text="").pack()
    Button(segundo_frame_config, text= "Guardar", command= lambda: guardar_general(combo_minutos_cita.get(), 3)).pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()

    # Cantidad máxima de días naturales para reinspección.
    opciones_dias_reinspeccion = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60]
    Label(segundo_frame_config, text="Cantidad máxima de días naturales para reinspección:", font=("Arial", 12)).pack()
    combo_dias_reinspeccion = ttk.Combobox(segundo_frame_config, values= opciones_dias_reinspeccion, state= "readonly")
    combo_dias_reinspeccion.pack()
    Label(segundo_frame_config, text="").pack()
    Button(segundo_frame_config, text= "Guardar", command= lambda: guardar_general(combo_dias_reinspeccion.get(), 4)).pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()

    # Cantidad de fallas graves para sacar vehículo de circulación.
    Label(segundo_frame_config, text="Cantidad de fallas graves para sacar vehículo de circulación:", font=("Arial", 12)).pack()
    entrada_fallas_graves = Entry(segundo_frame_config, width= 5, border= 4)
    entrada_fallas_graves.pack()
    indicador_fallas_graves = Label(segundo_frame_config, text= "Actual: Ninguno")
    indicador_fallas_graves.pack()
    Label(segundo_frame_config, text="").pack()
    Button(segundo_frame_config, text= "Guardar", command= lambda: guardar_general(entrada_fallas_graves.get(), 5)).pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()

    # Cantidad de meses.
    opciones_meses = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    Label(segundo_frame_config, text="Cantidad de meses que se van a considerar para desplegar todas \nlas citas disponibles en la asignación automática de citas:", font=("Arial", 12)).pack()
    combo_meses = ttk.Combobox(segundo_frame_config, values= opciones_meses, state= "readonly")
    combo_meses.pack()
    Label(segundo_frame_config, text="").pack()
    Button(segundo_frame_config, text= "Guardar", command= lambda: guardar_general(combo_meses.get(), 6)).pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()

    # Porcentaje de Impuesto al Valor Agregado (IVA) sobre la tarifa.
    Label(segundo_frame_config, text="Porcentaje de Impuesto al Valor Agregado (IVA) sobre la tarifa:", font=("Arial", 12)).pack()
    entrada_impuesto_iva = Entry(segundo_frame_config, width= 5, border= 4)
    entrada_impuesto_iva.pack()
    indicador_impuesto_iva = Label(segundo_frame_config, text= "Actual: Ninguno")
    indicador_impuesto_iva.pack()
    Label(segundo_frame_config, text="").pack()
    Button(segundo_frame_config, text= "Guardar", command= lambda: guardar_general(entrada_impuesto_iva.get(), 7)).pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()

    # Tabla de Tarifas.
    Label(segundo_frame_config, text="").pack()
    Label(segundo_frame_config, text="Tabla de Tarifas:", font=("Franklin Gothic Demi", 14)).pack()
    Label(segundo_frame_config, text="").pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()
    
    Label(segundo_frame_config, text="Vehículo:", font=("Arial", 10)).pack()
    Label(segundo_frame_config, text="Automóvil particular y vehículo de carga liviana \n(menor o igual a 3500 kg)", font=("Franklin Gothic Demi", 10)).pack()
    Label(segundo_frame_config, text="Tarifa nueva:", font=("Arial", 10)).pack()
    entrada_tarifa_1 = Entry(segundo_frame_config, width= 8, border= 4)
    entrada_tarifa_1.pack()
    Button(segundo_frame_config, text= "Guardar", command= lambda: guardar_tarifas(entrada_tarifa_1.get(), 0)).pack()
    indicador_tarifa_1 = Label(segundo_frame_config, text="Tarifa actual: Ninguno", font=("Franklin Gothic Demi", 10))
    indicador_tarifa_1.pack()

    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()
    Label(segundo_frame_config, text="Vehículo:", font=("Arial", 10)).pack()
    Label(segundo_frame_config, text="Automóvil particular y vehículo de carga liviana \n(mayor a 3500 kg pero menor a 8000 kg)", font=("Franklin Gothic Demi", 10)).pack()
    Label(segundo_frame_config, text="Tarifa nueva:", font=("Arial", 10)).pack()
    entrada_tarifa_2 = Entry(segundo_frame_config, width= 8, border= 4)
    entrada_tarifa_2.pack()
    Button(segundo_frame_config, text= "Guardar", command= lambda: guardar_tarifas(entrada_tarifa_2.get(), 1)).pack()
    indicador_tarifa_2 = Label(segundo_frame_config, text="Tarifa actual: Ninguno", font=("Franklin Gothic Demi", 10))
    indicador_tarifa_2.pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()

    Label(segundo_frame_config, text="Vehículo:", font=("Arial", 10)).pack()
    Label(segundo_frame_config, text="Vehículo de carga pesada y cabezales \n(mayor o igual a 8000 kg)", font=("Franklin Gothic Demi", 10)).pack()
    Label(segundo_frame_config, text="Tarifa:", font=("Arial", 10)).pack()
    entrada_tarifa_3 = Entry(segundo_frame_config, width= 8, border= 4)
    entrada_tarifa_3.pack()
    Button(segundo_frame_config, text= "Guardar", command= lambda: guardar_tarifas(entrada_tarifa_3.get(), 2)).pack()
    indicador_tarifa_3 = Label(segundo_frame_config, text="Tarifa actual: Ninguno", font=("Franklin Gothic Demi", 10))
    indicador_tarifa_3.pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()

    Label(segundo_frame_config, text="Vehículo:", font=("Arial", 10)).pack()
    Label(segundo_frame_config, text="Taxis", font=("Franklin Gothic Demi", 10)).pack()
    Label(segundo_frame_config, text="Tarifa:", font=("Arial", 10)).pack()
    entrada_tarifa_4 = Entry(segundo_frame_config, width= 8, border= 4)
    entrada_tarifa_4.pack()
    Button(segundo_frame_config, text= "Guardar", command= lambda: guardar_tarifas(entrada_tarifa_4.get(), 3)).pack()
    indicador_tarifa_4 = Label(segundo_frame_config, text="Tarifa actual: Ninguno", font=("Franklin Gothic Demi", 10))
    indicador_tarifa_4.pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()

    Label(segundo_frame_config, text="Vehículo:", font=("Arial", 10)).pack()
    Label(segundo_frame_config, text="Autobuses, buses y microbuses", font=("Franklin Gothic Demi", 10)).pack()
    Label(segundo_frame_config, text="Tarifa:", font=("Arial", 10)).pack()
    entrada_tarifa_5 = Entry(segundo_frame_config, width= 8, border= 4)
    entrada_tarifa_5.pack()
    Button(segundo_frame_config, text= "Guardar", command= lambda: guardar_tarifas(entrada_tarifa_5.get(), 4)).pack()
    indicador_tarifa_5 = Label(segundo_frame_config, text="Tarifa actual: Ninguno", font=("Franklin Gothic Demi", 10))
    indicador_tarifa_5.pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()

    Label(segundo_frame_config, text="Vehículo:", font=("Arial", 10)).pack()
    Label(segundo_frame_config, text="Motocicletas", font=("Franklin Gothic Demi", 10)).pack()
    Label(segundo_frame_config, text="Tarifa:", font=("Arial", 10)).pack()
    entrada_tarifa_6 = Entry(segundo_frame_config, width= 8, border= 4)
    entrada_tarifa_6.pack()
    Button(segundo_frame_config, text= "Guardar", command= lambda: guardar_tarifas(entrada_tarifa_6.get(), 5)).pack()
    indicador_tarifa_6 = Label(segundo_frame_config, text="Tarifa actual: Ninguno", font=("Franklin Gothic Demi", 10))
    indicador_tarifa_6.pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()

    Label(segundo_frame_config, text="Vehículo:", font=("Arial", 10)).pack()
    Label(segundo_frame_config, text="Equipo especial de obras", font=("Franklin Gothic Demi", 10)).pack()
    Label(segundo_frame_config, text="Tarifa:", font=("Arial", 10)).pack()
    entrada_tarifa_7 = Entry(segundo_frame_config, width= 8, border= 4)
    entrada_tarifa_7.pack()
    Button(segundo_frame_config, text= "Guardar", command= lambda: guardar_tarifas(entrada_tarifa_7.get(), 6)).pack()
    indicador_tarifa_7 = Label(segundo_frame_config, text="Tarifa actual: Ninguno", font=("Franklin Gothic Demi", 10))
    indicador_tarifa_7.pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()

    Label(segundo_frame_config, text="Vehículo:", font=("Arial", 10)).pack()
    Label(segundo_frame_config, text="Equipo especial agrícola \n(maquinaria agrícola)", font=("Franklin Gothic Demi", 10)).pack()
    Label(segundo_frame_config, text="Tarifa:", font=("Arial", 10)).pack()
    entrada_tarifa_8 = Entry(segundo_frame_config, width= 8, border= 4)
    entrada_tarifa_8.pack()
    Button(segundo_frame_config, text= "Guardar", command= lambda: guardar_tarifas(entrada_tarifa_8.get(), 7)).pack()
    indicador_tarifa_8 = Label(segundo_frame_config, text="Tarifa actual: Ninguno", font=("Franklin Gothic Demi", 10))
    indicador_tarifa_8.pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()
    Label(segundo_frame_config, text="").pack()
    Button(segundo_frame_config, text= "CERRAR VENTANA", command= lambda: ventana_config.destroy()).pack()
    Label(segundo_frame_config, text="").pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()

    # Abrir el archivo de configuración.
    archivo = open("configuración_reteve.dat", "r")
    datos_totales = archivo.read()
    datos_totales = eval(datos_totales)
    archivo.close()

    # Asignar los valores actuales de configuración a las opciones.
    combo_lineas.set(datos_totales[0])
    combo_hora_inicial.set(datos_totales[1])
    combo_hora_final.set(datos_totales[2])
    combo_minutos_cita.set(datos_totales[3])
    combo_dias_reinspeccion.set(datos_totales[4])
    combo_meses.set(datos_totales[6])
    texto_nuevo = "Actual: " + str(datos_totales[5])
    indicador_fallas_graves.config(text= texto_nuevo)
    texto_nuevo = "Actual: " + str(datos_totales[7])
    indicador_impuesto_iva.config(text= texto_nuevo)

    # Asignar los valores actuales a la tabla de tarifas.
    texto_nuevo = "Tarifa actual: " + str(datos_totales[8][0])
    indicador_tarifa_1.config(text= texto_nuevo)
    texto_nuevo = "Tarifa actual: " + str(datos_totales[8][1])
    indicador_tarifa_2.config(text= texto_nuevo)
    texto_nuevo = "Tarifa actual: " + str(datos_totales[8][2])
    indicador_tarifa_3.config(text= texto_nuevo)
    texto_nuevo = "Tarifa actual: " + str(datos_totales[8][3])
    indicador_tarifa_4.config(text= texto_nuevo)
    texto_nuevo = "Tarifa actual: " + str(datos_totales[8][4])
    indicador_tarifa_5.config(text= texto_nuevo)
    texto_nuevo = "Tarifa actual: " + str(datos_totales[8][5])
    indicador_tarifa_6.config(text= texto_nuevo)
    texto_nuevo = "Tarifa actual: " + str(datos_totales[8][6])
    indicador_tarifa_7.config(text= texto_nuevo)
    texto_nuevo = "Tarifa actual: " + str(datos_totales[8][7])
    indicador_tarifa_8.config(text= texto_nuevo)

    # Loop de la ventana.
    ventana_config.mainloop()

""" FUNCION PARA ABRIR EL MANUAL DE USUARIO
# ENTRADAS: Lee la respuesta del usuario en el messagebox.
# SALIDAS: Si el usuario responde 'sí', abre el manual de usuario. """
def ayuda_de_programa():
    if MessageBox.askyesno("CONFIRMAR", "¿Seguro de que desea abrir el manual?"):
        os.startfile("manual_de_usuario_reteve.pdf") # Abrir el manual.
    return

""" FUNCION PARA MOSTRAR LA INFORMACION DEL PROGRAMA EN UNA VENTANA
# ENTRADAS: No recibe ningún tipo de dato.
# SALIDAS: Despliega una ventana con la información del programa. """
def acerca_de():
    # Crear la ventana de información.
    ventana_de_informacion = Toplevel()
    ventana_de_informacion.geometry("310x390")
    ventana_de_informacion.resizable(False, False)
    ventana_de_informacion.title("Acerca de")
    ventana_de_informacion.config(bg="White")

    # Mostrar la información del programa.
    Label(ventana_de_informacion, text= "\nAcerca del programa\n", fg="black", bg="white", font=("Franklin Gothic Demi", 16)).pack()
    Label(ventana_de_informacion, text="Nombre del programa: ReTeVe\n \nVersión del programa: 1.0.0\n \
          \nFecha de creación: 01 de Junio del 2023\n \nÚltima modificación: 01 de Junio del 2023\n \nAutores:\n \
          \nJose Mario Jiménez Vargas\n \nJohn Sebastián Ceciliano Piedra", fg="black", bg="white", font=("Arial", 10)).pack()

    # Botón para cerrar la ventana.
    boton_aceptar = Button(ventana_de_informacion, text="Aceptar", command= ventana_de_informacion.destroy)
    boton_aceptar.place(x=125, y=320)

    # Loop de la ventana.
    ventana_de_informacion.mainloop()

""" FUNCION PARA CERRAR EL PROGRAMA
# ENTRADAS: Lee la respuesta del usuario en el messagebox.
# SALIDAS: Si el usuario responde 'sí', cierra el programa. """
def salir_del_programa():
    if MessageBox.askyesno("CONFIRMAR", "¿Seguro de que desea salir del programa?"):
        ventana_principal.destroy() # Cerrar la ventana.
    return

# FUNCION QUE GENERA LA LISTA DE INTERVALOS DISPONIBLES
# ENTRADAS: Lee la fecha actual y la configuración.
# SALIDAS: Lleva a crear la lista de citas.
def generar_lista_intervalo():
    global fecha_hoy, valores_lista
    fecha = fecha_hoy.split("/")
    año_hoy = int(fecha[0])
    mes_hoy = int(fecha[1])
    dia_hoy = int(fecha[2])

    archivo = open("configuración_reteve.dat", "r")
    datos_originales = archivo.read()
    datos_originales = eval(datos_originales)
    archivo.close()
    inicio = datetime(año_hoy, mes_hoy, dia_hoy)  # Fecha de inicio
    fecha_final = validar_fecha_fin(año_hoy, mes_hoy + datos_originales[6], dia_hoy)
    num1 = fecha_final[0]
    num2 = fecha_final[1]
    num3 = fecha_final[2]
    fin = datetime(num1, num2, num3)  # Fecha de fin
    hora_inicio = datos_originales[1]  # Hora de inicio
    hora_fin = datos_originales[2]   # Hora de fin
    minutos = int(datos_originales[3][3:])
    intervalo_minutos = minutos  # Intervalo de tiempo en minutos
    lista_fechas_intervalo = generar_lista_fechas_intervalo(inicio.date(), fin.date(), hora_inicio, hora_fin, intervalo_minutos)

    valores_lista = list()
    for fecha_hora in lista_fechas_intervalo:
        valores_lista.append(str(fecha_hora))

# FUNCION QUE ACTUALIZA LA FECHA Y HORA ACTUAL
# ENTRADAS: Recibe la fecha y hora en tiempo real del sistema.
# SALIDAS: Actualiza el label de fecha y hora por tics y guarda una variable con la fecha y hora actual.
def actualizar_fecha_hora():
    global fecha_hoy
    fecha_actual = datetime.now()
    fecha_formateada = fecha_actual.strftime("%Y/%m/%d %H:%M:%S")
    label_fecha_hora.config(text=fecha_formateada)
    ventana_principal.after(1000, actualizar_fecha_hora)
    fecha_hoy = fecha_formateada[:10]

""" FUNCION PRINCIPAL """
manual = True
fecha_hoy = str()
valores_lista = list()

# Ventana principal.
ventana_principal = Tk()
ventana_principal.geometry("600x700")
ventana_principal.resizable(False, False)
ventana_principal.title("ReTeVe")

# Indicador de fecha y hora en la ventana.
label_fecha_hora = Label(ventana_principal, font=("Arial", 14))
label_fecha_hora.place(x=400,y=10)
actualizar_fecha_hora()
generar_lista_intervalo()

# Opciones de citas.
Label(ventana_principal, text="").pack()
Label(ventana_principal, text="Citas", font=("Comic Sans MS", 16)).pack()
boton_a = Button(ventana_principal, text="Programar citas", font=("Arial", 12), command= lambda: programar_citas())
boton_a.pack()
boton_b = Button(ventana_principal, text="Cancelar citas", font=("Arial", 12), command= None)
boton_b.pack()

# Opciones de vehículos.
Label(ventana_principal, text="").pack()
Label(ventana_principal, text="Vehículos", font=("Comic Sans MS", 16)).pack()
boton_c = Button(ventana_principal, text="Ingreso de vehículos a la estación", font=("Arial", 12), command= None)
boton_c.pack()

# Opciones de revisiones.
Label(ventana_principal, text="").pack()
Label(ventana_principal, text="Revisiones", font=("Comic Sans MS", 16)).pack()
boton_d = Button(ventana_principal, text="Tablero de revisión", font=("Arial", 12), command= None)
boton_d.pack()
boton_e = Button(ventana_principal, text="Lista de fallas", font=("Arial", 12), command= None)
boton_e.pack()

# Barra de menú.
menubar = Menu(ventana_principal)
menubar.add_command(label="Configuración del sistema", command= lambda: ventana_configuracion_sistema())
menubar.add_command(label="Ayuda", command= lambda: ayuda_de_programa())
menubar.add_command(label="Acerca de", command= lambda: acerca_de())
menubar.add_command(label="Salir", command= lambda: salir_del_programa())
ventana_principal.config(menu=menubar)

# Loop de la ventana.
ventana_principal.mainloop()