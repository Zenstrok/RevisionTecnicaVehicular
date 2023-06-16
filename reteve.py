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
"""def validar_fecha(fecha):
    global fecha_v
    try:
        # Intentamos crear un objeto de fecha a partir de la cadena proporcionada
        datetime.datetime.strptime(fecha, '%Y-%m-%d')
        fecha_v = True
    except ValueError:
        fecha_v = False
        MessageBox.showerror("Fecha","Fecha Invalida")"""
    
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

# FUNCION COMPARAR NODOS
# ENTRADAS: Recibe los dos datos a comparar.
# SALIDAS: Retorna True si va a la izquierda, False si va a la derecha.
def comparar_nodos(dato1, dato2):
    print(dato1, dato2)
    if int(dato2[0]) > int(dato1[0]):
        return False
    elif int(dato2[1]) > int(dato1[1]):
        return False
    elif int(dato2[2]) > int(dato1[2]):
        return False
    elif int(dato2[3]) > int(dato1[3]):
        return False
    else:
        return True

# FUNCION INSERTAR NODO
# ENTRADAS: Recibe el árbol y el valor a agregar.
# SALIDAS: Retorna el árbol con el nuevo nodo.
def insertar_nodo(arbol, valor):
    if arbol == None:
        return crear_nodo(valor)
    else:
        if comparar_nodos(arbol[0][10], valor[10]) == True:
            arbol[1] = insertar_nodo(arbol[1], valor)
        else:
            arbol[2] = insertar_nodo(arbol[2], valor)
        return arbol

# FUNCION QUE PROGRAMA UNA CITA Y LA GUARDA EN UN ÁRBOL DE BUSQUEDA BINARIA (ABB)
# ENTRADAS: Recibe los datos que se guardarán en el nodo.
# SALIDAS: Guarda los datos en un nodo del árbol (ABB).
def programar_cita_nueva(dato1, dato2, dato3, dato4, dato5, dato6, dato7, dato8, dato9, dato10):
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

    dato_nodo = [datos_originales["num_citas"], dato1, dato2, dato3, dato4, dato5, dato6, dato7, dato8, dato9, dato10, "PENDIENTE"]
    print(dato_nodo)

    # Leer archivos.
    archivo1 = open("arbol_citas.dat", "r")
    arbol = archivo1.read()
    arbol = eval(arbol)
    archivo1.close()

    archivo2 = open("registro_arbol.dat", "r")
    indices_nodo = archivo2.read()
    indices_nodo = eval(indices_nodo)
    archivo2.close()

    arbol = insertar_nodo(arbol, dato_nodo)

    indices_nodo[dato_nodo[0]] = [dato_nodo[2], dato_nodo[10]]

    # Escribir archivos.
    archivo = open("arbol_citas.dat", "w")
    archivo.write(str(arbol))
    archivo.close()

    archivo = open("registro_arbol.dat", "w")
    archivo.write(str(indices_nodo))
    archivo.close()

    # ENVÍO DE CORREO AQUÍ

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

# FUNCION DESCOMPONER H M
# ENTRADAS: Recibe la lista que contiene la fecha y hora.
# SALIDAS: Retorna la lista con la hora en segundos.
def descomponer_h_m(lista):
    horas = int(lista[-2])
    mins = int(lista[-1])
    suma = horas * 3600
    suma += mins * 60
    lista = lista[:-2]
    lista.append(str(suma))
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
                programar_cita_nueva(tipo_cita.get(), dato2, entry3.get(), dato4, dato5, dato6, dato7, dato8, dato9, descompuesto)
            else:
                MessageBox.showerror("ERROR", "Cita no disponible para programar.")
        else:
            fecha_hora_automatico(tipo_cita.get(), dato2, entry3.get(), dato4, dato5, dato6, dato7, dato8, dato9, valores_lista)
    
    # FUNCION PARA EL BOTÓN DE FECHA Y HORA AUTOMÁTICOS
    # ENTRADAS: Recibe los datos a guardar en la cita y la lista de citas posibles.
    # SALIDAS: Envía la solicitud de programar cita si el usuario lo indica.
    def fecha_hora_automatico(dato1, dato2, dato3, dato4, dato5, dato6, dato7, dato8, dato9, lista_automaticos):

        def cancelar_accion():
            res = MessageBox.askyesno("CONFIRMACIÓN", "¿Seguro de que desea cancelar la asignación?")
            if res:
                ventana_automatico.destroy()
                ventana_programar_citas.deiconify()

        # FUNCION PROGRAMAR AUTO
        # ENTRADAS: Recibe los datos de la cita a programar.
        # SALIDAS: Envía a programar la cita en el árbol de citas.
        def programar_auto(dato1, dato2, dato3, dato4, dato5, dato6, dato7, dato8, dato9, dato10):
            global manual
            print(dato10)
            ano_separado = dato10[:4]
            mes_separado = dato10[5:7]
            dia_separado = dato10[8:10]
            hora_separada = dato10[11:13]
            minutos_separados = dato10[14:16]
            descompuesto = descomponer_h_m([ano_separado, mes_separado, dia_separado, hora_separada, minutos_separados])
            programar_cita_nueva(dato1, dato2, dato3, dato4, dato5, dato6, dato7, dato8, dato9, descompuesto)
            ventana_automatico.destroy()
            ventana_programar_citas.destroy()
            manual = True
            programar_citas()
            return
        
        ventana_programar_citas.iconify()
        ventana_automatico = Toplevel()
        ventana_automatico.resizable(False, False)
        ancho_pantalla = ventana_automatico.winfo_screenwidth()
        alto_pantalla = ventana_automatico.winfo_screenheight()
        posicion_x = ancho_pantalla - 1000
        ventana_automatico.geometry(f"400x120+{posicion_x}+100")

        Label(ventana_automatico, text= "Seleccione una opción de fecha y hora:", font= ("Franklin Gothic Demi", 14)).pack()
        combo_auto = ttk.Combobox(ventana_automatico, values= lista_automaticos, state= "readonly", width= 40)
        combo_auto.pack()
        Label(ventana_automatico, text="").pack()
        Button(ventana_automatico, text= "Guardar", command= lambda: programar_auto(dato1, dato2, dato3, dato4, dato5, dato6, dato7, dato8, dato9, combo_auto.get()), bg= "#0277fa", fg= "White").place(x= 140, y= 70)
        Button(ventana_automatico, text= "Cancelar", command= lambda: cancelar_accion(), bg= "#f94141", fg= "White").place(x= 200, y= 70)

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
        respuesta = MessageBox.askyesno("SALIR", "¿Seguro de que desea cerrar la\nventana de programación de citas?")
        if respuesta:
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
    ventana_programar_citas.resizable(False, False)
    ventana_programar_citas.title("Programar Citas")
    ancho_pantalla = ventana_programar_citas.winfo_screenwidth()
    alto_pantalla = ventana_programar_citas.winfo_screenheight()
    posicion_x = ancho_pantalla - 1000
    ventana_programar_citas.geometry(f"600x700+{posicion_x}+100")

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

    #Button(ventana_programar_citas, text= "Guardar", command= lambda:  validar_fecha(fecha = (año.get() + "-" + mes.get() + "-" + dia.get())))

    tipo_programacion = StringVar()
    Label(ventana_programar_citas, text= "Fecha y hora de la cita: ", font= ("Franklin Gothic Demi", 12)).place(x= 10, y= 500)
    boton_manual = Radiobutton(ventana_programar_citas, text= "Manual", variable= tipo_programacion, value= "manual", command= lambda: activar_manual())
    boton_manual.place(x= 190, y= 502)
    boton_auto = Radiobutton(ventana_programar_citas, text= "Automático", variable= tipo_programacion, value= "auto", command= lambda: desactivar_manual())
    boton_auto.place(x= 270, y= 502)

    # Botones de interacción.
    Button(ventana_programar_citas, text= "Programar Cita", width= 20, height= 2, font= ("Franklin Gothic Demi", 10), bg= "#0277fa", fg= "White", command= lambda: validar_datos_cita()).place(x= 140, y= 600)
    Button(ventana_programar_citas, text= "Cerrar ventana", width= 20, height= 2, font= ("Franklin Gothic Demi", 10), bg= "#f94141", fg= "White", command= lambda: cerrar_citas()).place(x= 300, y= 600)

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
    
# FUNCIAN BUSCAR NODO Y CANCELAR
# ENTRADAS:
# SALIDAS: 
def buscar_nodo_cancelar(arbol, num, placa, fecha_hora):
    if arbol[0][0] == num:
        if arbol[0][11] == "PENDIENTE":
            arbol[0][11] = "CANCELADA"
            return arbol
        else:
            MessageBox.showerror("ERROR", "La cita debe estar pendiente para ser cancelada.")
            return arbol
    else:
        if comparar_nodos(arbol[0][10], fecha_hora) == True:
            arbol[1] = buscar_nodo_cancelar(arbol[1], num, placa, fecha_hora)
        else:
            arbol[2] = buscar_nodo_cancelar(arbol[2], num, placa, fecha_hora)
        return arbol

def cancelar_citas():

    def verificar_en_colas(dato):
        archivo = open("lista_colas.dat", "r")
        colas = archivo.read()
        colas = eval(colas)
        archivo.close()

        for lista in colas:
            # Colas de espera.
            if dato in lista[1]:
                lista[1].remove(dato)

                archivo = open("lista_colas.dat", "w")
                archivo.write(str(colas))
                archivo.close()
                return True
            
            # Colas de revisión.
            if dato in lista[2][0]:
                MessageBox.showerror("ERROR", "Vehículo se encuentra en una cola actualmente.")
                return False
            if dato in lista[2][1]:
                MessageBox.showerror("ERROR", "Vehículo se encuentra en una cola actualmente.")
                return False
            if dato in lista[2][2]:
                MessageBox.showerror("ERROR", "Vehículo se encuentra en una cola actualmente.")
                return False
            if dato in lista[2][3]:
                MessageBox.showerror("ERROR", "Vehículo se encuentra en una cola actualmente.")
                return False
            if dato in lista[2][4]:
                MessageBox.showerror("ERROR", "Vehículo se encuentra en una cola actualmente.")
                return False
        return

    def salir_cancelar():
        res = MessageBox.askyesno("CONFIRMACIÓN", "¿Seguro de que desea salir?")
        if res:
            ventana_cancelar_citas.destroy()
            ventana_principal.deiconify()
        return
    
    def cancelar_cita_deseada(cita, placa):
        if not cita.isdigit():
            MessageBox.showerror("ERROR", "Cita debe ser numérica")
            return
        cita = int(cita)

        archivo1 = open("arbol_citas.dat", "r")
        arbol = archivo1.read()
        arbol = eval(arbol)
        archivo1.close()

        archivo2 = open("registro_arbol.dat", "r")
        indices_nodo = archivo2.read()
        indices_nodo = eval(indices_nodo)
        archivo2.close()

        try:
            datos_cita = indices_nodo[cita]
        except:
            MessageBox.showerror("ERROR", "Cita no registrada")
            return
        
        if datos_cita[0] != placa:
            MessageBox.showerror("ERROR", "Cita no registrada")
            return
        
        if verificar_en_colas(placa) == False:
            return
        
        continuar = MessageBox.askyesno("CONTINUAR", "¿Seguro de que desea eliminar la cita número " + str(cita) + "?")
        if continuar:
            arbol = buscar_nodo_cancelar(arbol, cita, placa, datos_cita[1])
            print(arbol)

            archivo1 = open("arbol_citas.dat", "w")
            arbol = archivo1.write(str(arbol))
            archivo1.close()

            MessageBox.showinfo("ESTADO", "Se ha cancelado la cita número " + str(cita))
        return
    
    ventana_principal.iconify()
    ventana_cancelar_citas = Toplevel()
    ventana_cancelar_citas.resizable(False, False)
    ventana_cancelar_citas.title("Cancelar citas")
    ancho_pantalla = ventana_cancelar_citas.winfo_screenwidth()
    alto_pantalla = ventana_cancelar_citas.winfo_screenheight()
    posicion_x = ancho_pantalla - 1000
    ventana_cancelar_citas.geometry(f"400x300+{posicion_x}+100")

    Label(ventana_cancelar_citas, text= "Cancelar citas", width= 20, font= ("Franklin Gothic Demi", 16)).pack(pady= 10)
    Label(ventana_cancelar_citas, text= "Número de la cita:", font= ("Franklin Gothic Demi", 12)).pack(pady= 10)
    num_cita = Entry(ventana_cancelar_citas, width= 10, border= 6)
    num_cita.pack()
    Label(ventana_cancelar_citas, text= "Placa del vehículo:", font= ("Franklin Gothic Demi", 12)).pack(pady= 10)
    placa_vehiculo = Entry(ventana_cancelar_citas, width= 10, border= 6)
    placa_vehiculo.pack()

    Button(ventana_cancelar_citas, text= "Cancelar cita", command= lambda: cancelar_cita_deseada(num_cita.get(), placa_vehiculo.get()), bg= "#f94141", fg= "White").place(x= 110, y= 240)
    Button(ventana_cancelar_citas, text= "Cerrar ventana", command= lambda: salir_cancelar(), bg= "#0277fa", fg= "White").place(x= 200, y= 240)

    ventana_cancelar_citas.mainloop()

def guardar_dato_ingreso(dato):
    global datos_del_ingreso
    datos_del_ingreso = dato
    return

# FUNCIAN BUSCAR NODO Y CANCELAR
# ENTRADAS:
# SALIDAS: 
def buscar_nodo_info(arbol, num, placa, fecha_hora):
    if arbol[0][0] == num:
        if arbol[0][11] == "PENDIENTE":
            guardar_dato_ingreso(arbol[0])
            return arbol
        else:
            MessageBox.showerror("ERROR", "Cita debe ser pendiente.")
            return False
    else:
        if comparar_nodos(arbol[0][10], fecha_hora) == True:
            arbol[1] = buscar_nodo_info(arbol[1], num, placa, fecha_hora)
        else:
            arbol[2] = buscar_nodo_info(arbol[2], num, placa, fecha_hora)
        return arbol

def ingreso_a_estacion():

    def salir_ingreso():
        res = MessageBox.askyesno("CONFIRMACIÓN", "¿Seguro de que desea salir?")
        if res:
            ventana_ingreso_estacion.destroy()
            ventana_principal.deiconify()
        return
    
    def salir_ingresar():
        res = MessageBox.askyesno("CONFIRMACIÓN", "¿Seguro de que desea salir?")
        if res:
            ventana_ingresar.destroy()
            ventana_ingreso_estacion.deiconify()
        return
    
    def verificacion_cola(placa):
        archivo = open("lista_colas.dat", "r")
        colas = archivo.read()
        colas = eval(colas)
        archivo.close()

        for lista in colas:
            print(lista)
            if placa in lista[1]:
                MessageBox.showerror("ERROR", "Vehículo se encuentra en una cola actualmente.")
                ventana_ingresar.destroy()
                ventana_ingreso_estacion.deiconify()
                return
            if placa in lista[2][0]:
                MessageBox.showerror("ERROR", "Vehículo se encuentra en una cola actualmente.")
                ventana_ingresar.destroy()
                ventana_ingreso_estacion.deiconify()
                return
            if placa in lista[2][1]:
                MessageBox.showerror("ERROR", "Vehículo se encuentra en una cola actualmente.")
                ventana_ingresar.destroy()
                ventana_ingreso_estacion.deiconify()
                return
            if placa in lista[2][2]:
                MessageBox.showerror("ERROR", "Vehículo se encuentra en una cola actualmente.")
                ventana_ingresar.destroy()
                ventana_ingreso_estacion.deiconify()
                return
            if placa in lista[2][3]:
                MessageBox.showerror("ERROR", "Vehículo se encuentra en una cola actualmente.")
                ventana_ingresar.destroy()
                ventana_ingreso_estacion.deiconify()
                return
            if placa in lista[2][4]:
                MessageBox.showerror("ERROR", "Vehículo se encuentra en una cola actualmente.")
                ventana_ingresar.destroy()
                ventana_ingreso_estacion.deiconify()
                return
    
        valor_minimo = None
        indice = None
        contador = 0
        for lista in colas:
            if valor_minimo == None:
                valor_minimo = len(lista[1])
                indice = 0
            elif len(lista[1]) < valor_minimo:
                valor_minimo = len(lista[1])
                indice = contador
            contador += 1

        colas[indice][1].append(placa)

        print(colas)

        archivo = open("lista_colas.dat", "w")
        archivo.write(str(colas))
        archivo.close()
        MessageBox.showinfo("ESTADO", "Se ha ingresado a la estación correctamente.")
        ventana_ingresar.destroy()
        ventana_ingreso_estacion.deiconify()

    def ingresar(num_cita, placa):

        if not num_cita.isdigit():
            MessageBox.showerror("ERROR", "Valor de cita debe ser numérico.")
            return
        num_cita = int(num_cita)
        
        archivo = open("arbol_citas.dat", "r")
        arbol = archivo.read()
        arbol = eval(arbol)
        archivo.close()
        archivo = open("registro_arbol.dat", "r")
        registros = archivo.read()
        registros = eval(registros)
        archivo.close()
        
        try:
            datos_cita = registros[num_cita]
        except:
            MessageBox.showerror("ERROR", "Cita no registrada")
            return
        
        if datos_cita[0] != placa:
            MessageBox.showerror("ERROR", "Cita no registrada")
            return
        datos = registros[num_cita]

        buscar_nodo_info(arbol, num_cita, placa, datos[1])
        global datos_del_ingreso
        if datos_del_ingreso == False:
            return

        ventana_ingreso_estacion.iconify()

        global ventana_ingresar
        ventana_ingresar = Toplevel()
        ventana_ingresar.resizable(False, False)
        ventana_ingresar.title("Ingreso de vehículos")
        ancho_pantalla = ventana_ingresar.winfo_screenwidth()
        alto_pantalla = ventana_ingresar.winfo_screenheight()
        posicion_x = ancho_pantalla - 1000
        ventana_ingresar.geometry(f"440x260+{posicion_x}+100")

        Label(ventana_ingresar, text= "                    ").grid(row= 1, column= 2)
        Label(ventana_ingresar, text= "                    ").grid(row= 2, column= 2)
        Label(ventana_ingresar, text= "Ingresar un vehículo a la estación", width= 30, font= ("Franklin Gothic Demi", 16)).place(x= 50, y= 5)
        Label(ventana_ingresar, text= "Número de la cita:", font= ("Franklin Gothic Demi", 12)).grid(row= 3, column= 1)
        Label(ventana_ingresar, text= datos_del_ingreso[0], font= ("Arial", 10)).grid(row= 4, column= 1)
        Label(ventana_ingresar, text= "Placa del vehículo:", font= ("Franklin Gothic Demi", 12)).grid(row= 3, column= 3)
        Label(ventana_ingresar, text= datos_del_ingreso[2], font= ("Arial", 10)).grid(row= 4, column= 3)
        Label(ventana_ingresar, text= "Marca del vehículo:", font= ("Franklin Gothic Demi", 12)).grid(row= 5, column= 1)
        Label(ventana_ingresar, text= datos_del_ingreso[4], font= ("Arial", 10)).grid(row= 6, column= 1)
        Label(ventana_ingresar, text= "Modelo del vehículo:", font= ("Franklin Gothic Demi", 12)).grid(row= 5, column= 3)
        Label(ventana_ingresar, text= datos_del_ingreso[5], font= ("Arial", 10)).grid(row= 6, column= 3)
        Label(ventana_ingresar, text= "Propietario del vehículo:", font= ("Franklin Gothic Demi", 12)).grid(row= 7, column= 1)
        Label(ventana_ingresar, text= datos_del_ingreso[6], font= ("Arial", 10), wraplength= 130).grid(row= 8, column= 1)
        Label(ventana_ingresar, text= "Costo de revisión:", font= ("Franklin Gothic Demi", 12)).grid(row= 7, column= 3)
        Label(ventana_ingresar, text= datos_del_ingreso[7], font= ("Arial", 10)).grid(row= 8, column= 3)

        Label(ventana_ingresar, text= "                    ", font= ("Arial", 10)).grid(row= 9, column= 2)

        Button(ventana_ingresar, text= "Ingresar vehículo", bg= "#0277fa", fg= "White", command= lambda: verificacion_cola(datos_del_ingreso[2])).grid(row= 10, column= 1)
        Button(ventana_ingresar, text= "Cancelar ingreso", command= lambda: salir_ingresar(), bg= "#f94141", fg= "White").grid(row= 10, column= 3)
        
        ventana_ingresar.mainloop()

    ventana_principal.iconify()
    ventana_ingreso_estacion = Toplevel()
    ventana_ingreso_estacion.resizable(False, False)
    ventana_ingreso_estacion.title("Ingreso de vehículos")
    ancho_pantalla = ventana_ingreso_estacion.winfo_screenwidth()
    alto_pantalla = ventana_ingreso_estacion.winfo_screenheight()
    posicion_x = ancho_pantalla - 1000
    ventana_ingreso_estacion.geometry(f"400x300+{posicion_x}+100")

    Label(ventana_ingreso_estacion, text= "Ingreso de vehículos a la estación", width= 30, font= ("Franklin Gothic Demi", 16)).pack(pady= 10)
    Label(ventana_ingreso_estacion, text= "Número de la cita:", font= ("Franklin Gothic Demi", 12)).pack(pady= 10)
    num_cita = Entry(ventana_ingreso_estacion, width= 10, border= 6)
    num_cita.pack()
    Label(ventana_ingreso_estacion, text= "Placa del vehículo:", font= ("Franklin Gothic Demi", 12)).pack(pady= 10)
    placa_vehiculo = Entry(ventana_ingreso_estacion, width= 10, border= 6)
    placa_vehiculo.pack()

    Button(ventana_ingreso_estacion, text= "Validar datos", command= lambda: ingresar(num_cita.get(), placa_vehiculo.get()), bg= "#0277fa", fg= "White").place(x= 110, y= 240)
    Button(ventana_ingreso_estacion, text= "Cerrar ventana", command= lambda: salir_ingreso(), bg= "#f94141", fg= "White").place(x= 200, y= 240)

    ventana_ingreso_estacion.mainloop()

























def tablero():

    def cerrar_tablero():
        res = MessageBox.askyesno("CONFIRMAR", "¿Seguro de que desea cerrar la ventana?")
        if res:
            ventana_tablero_revision.destroy()
            ventana_principal.deiconify()
        return

    def comando_t(dato):
        return
    
    def comando_u(dato):
        archivo = open("lista_colas.dat", "r")
        lista_colas = archivo.read()
        lista_colas = eval(lista_colas)
        archivo.close()

        for lista in lista_colas:
            if len(lista[1]) == 0:
                pass
            else:
                if dato == lista[1][0]:
                    if lista[2][0] == []:
                        lista[1].remove(dato)
                        lista[2][0].append(dato)

                        archivo = open("lista_colas.dat", "w")
                        archivo.write(str(lista_colas))
                        archivo.close()

                        ventana_tablero_revision.destroy()
                        tablero()
                        return
                    else:
                        MessageBox.showerror("ERROR", "Hay un vehículo en el puesto 1.")
                        return
            
            for indice, elemento in enumerate(lista[2]):
                print(indice, elemento)
                print(lista[2])
                if indice == 4:
                    if elemento == []:
                        pass
                    elif dato == elemento[0]:
                        MessageBox.showerror("ERROR", "El vehículo está en el puesto 5.")
                        return
                    else:
                        pass
                else:
                    if len(elemento) == 0:
                        pass
                    elif dato == elemento[0]:
                        if lista[2][indice + 1] == []:
                            elemento.remove(dato)
                            lista[2][indice + 1].append(dato)

                            archivo = open("lista_colas.dat", "w")
                            archivo.write(str(lista_colas))
                            archivo.close()

                            ventana_tablero_revision.destroy()
                            tablero()
                            return
                        else:
                            MessageBox.showerror("ERROR", "Hay un vehículo delante.")
                            return
    
    def comando_e(dato):

        return
    
    def comando_f(dato):
        return

    def ejecutar_comando(comando):
        comando = comando.get()
        placa = comando[1:]
        if comando[0] == "T":
            comando_t(placa)
        elif comando[0] == "U":
            comando_u(placa)
        elif comando[0] == "E":
            comando_e(placa)
        elif comando[0] == "F":
            comando_f(placa)
        elif comando[0] == "R":
            cerrar_tablero()
        else:
            MessageBox.showerror("ERROR", "Comando Invalido")

    ventana_principal.iconify()

    ventana_tablero_revision = Toplevel()
    ventana_tablero_revision.title("Tablero de revision")
    ventana_tablero_revision.resizable(False, False)
    ancho_pantalla = ventana_tablero_revision.winfo_screenwidth()
    alto_pantalla = ventana_tablero_revision.winfo_screenheight()
    posicion_x = ancho_pantalla - 1000
    ventana_tablero_revision.geometry(f"760x700+{posicion_x}+100")
    
    frame_tablero = Frame(ventana_tablero_revision) 
    frame_tablero.pack(fill= BOTH, expand= 1, pady= 100)  
    
    # Crear un canvas.
    canvas_tablero = Canvas(frame_tablero) 
    canvas_tablero.pack(side= LEFT, fill= BOTH, expand= 1)  
    
    # Crear el scrollbar en el canvas.
    scrollbar_tablero = Scrollbar(frame_tablero, orient= VERTICAL, command= canvas_tablero.yview) 
    scrollbar_tablero.pack(side= RIGHT, fill= Y)  
    
    # Configurar el canvas.
    canvas_tablero.configure(yscrollcommand= scrollbar_tablero.set) 
    canvas_tablero.bind("<Configure>", lambda e: canvas_tablero.configure(scrollregion= canvas_tablero.bbox("all")))  
    
    # Crear otro frame dentro del canvas.
    segundo_frame_tablero = Frame(canvas_tablero)  
    
    # Agregar el nuevo frame a una ventana en el canvas.
    canvas_tablero.create_window((0, 0), window = segundo_frame_tablero, anchor= "nw")

    archivo = open("lista_colas.dat", "r")
    colas = archivo.read()
    colas = eval(colas)
    archivo.close()

    lineas = len(colas)
    canvas = Canvas(segundo_frame_tablero, width=1200, height=1200)
    canvas.place(x=0, y=20) # Ajusta la posición del canvas según tus necesidades
    # Dibujar línea vertical   # Ajusta la posición inicial de las líneas según tus necesidades

    n = 0
    puestos = 7
    crear_lineas = puestos
    #lineas = 25
    while crear_lineas > 0:
        print("hola")
        canvas.create_line( 60 + n, 0, 60 + n, lineas *70, fill="black")  # Ajusta el ancho y color de las líneas según tus necesidades
        crear_lineas -= 1
        n += 100

    linea = Label(ventana_tablero_revision,text="Linea",font=("", 12))
    linea.place(x=10,y=60)
    siguiente = Label(ventana_tablero_revision,text="Siguiente",font=("", 12))
    siguiente.place(x=77,y=60)
    puesto1 = Label(ventana_tablero_revision,text="Puesto 1",font=("", 12))
    puesto1.place(x=180,y=60)
    puesto2 = Label(ventana_tablero_revision,text="Puesto 2",font=("", 12))
    puesto2.place(x=280,y=60)
    puesto3 = Label(ventana_tablero_revision,text="Puesto 3",font=("", 12))
    puesto3.place(x=380,y=60)
    puesto4 = Label(ventana_tablero_revision,text="Puesto 4",font=("", 12))
    puesto4.place(x=480,y=60)
    puesto5 = Label(ventana_tablero_revision,text="Puesto 5",font=("", 12))
    puesto5.place(x=580,y=60)
    espacio = Label(segundo_frame_tablero,text="  ",font=("", 12))
    espacio.grid(row = 0,column= 2)

 
    num = 1
    n = 4
    for i in range(lineas):
        num_linea = Label(segundo_frame_tablero,text="     " + str(num),font=("", 12))
        num_linea.grid(row = n + num   ,column= 1)
        separador = Label(segundo_frame_tablero,text="───────────────────────────────────────────────────")
        separador.grid(row = n +1 + num   ,column= 5)
        num += 1
        n += 1

    archivo = open("lista_colas.dat","r")
    lista_de_colas = archivo.read()
    lista_de_colas = eval(lista_de_colas)
    archivo.close()

    print(lista_de_colas)
    #print(lineas,puestos)
    columna_largo = 20
    for i in range(1,lineas + 1):
        for j in range(1,puestos):
            print(i,j)
            print(lista_de_colas)
            if j-1 == 0:
                placa_casilla = lista_de_colas[i-1][1]
            else:
                placa_casilla = lista_de_colas[i-1][2][j-2]
            nombre_etiqueta = str(i) + str(j)
            num_linea = Label(segundo_frame_tablero, text=placa_casilla,fg = None, name=nombre_etiqueta, font=("", 10))
            num_linea.place(x = 95*j ,y = columna_largo) 
        columna_largo += 45
    
    
        


    comando = Label(ventana_tablero_revision,text="COMANDO:",font=("", 12))
    comando.place(x=100,y=8)
    comando = Entry(ventana_tablero_revision,width = 50)
    comando.place(x=200,y=10)
    btn_ejecutar = Button(ventana_tablero_revision, text="Ejecutar", bg= "#0277fa", fg= "White", font=("", 10), width= 7, height= 1, command= lambda: ejecutar_comando(comando))
    btn_ejecutar.place(x=530, y=6)
    btn_cerrar = Button(ventana_tablero_revision, text="Salir", bg= "#f94141", fg= "White", font=("", 10), width= 7, height= 1, command= lambda: cerrar_tablero())
    btn_cerrar.place(x=670, y=6)

    # Loop de la ventana.
    ventana_tablero_revision.mainloop()














""" FUNCION PARA ABRIR LA VENTANA DE LISTA DE FALLAS
# ENTRADAS: Lee las acciones del usuario.
# SALIDAS: Guarda los cambios en un archivo predefinido. """
def lista_de_fallas():

    def salir_fallas():
        res = MessageBox.askyesno("CONFIRMACIÓN", "¿Seguro de que desea salir?")
        if res:
            ventana_lista_de_fallas.destroy()
            ventana_principal.deiconify()
        return

    # FUNCION GUARDAR FALLA
    # ENTRADAS: 
    # SALIDAS: 
    def guardar_falla(lista, opcion, texto):
        if opcion == 1:
            if len(lista[1]) < 5:
                MessageBox.showerror("Error","Texto Invalido")
                return
        else:
            if lista[1] == "":
                lista[1] = texto

        if lista[0].isdigit() == False:
            MessageBox.showerror("Error","Falla debe ser un numero")
            return
        else:
            archivo = open("registros.dat", "r")
            numeros_usados = archivo.read()
            numeros_usados = eval(numeros_usados)
            archivo.close()
            
            numeros = numeros_usados["fallas_usadas"]
            if opcion == 1:
                for elemento in numeros:
                    if elemento == lista[0]:
                        MessageBox.showerror("Error","El numero " + lista[0] + " de falla ya se registro")
                        return

                numeros.append(lista[0])
                numeros_usados["fallas_usadas"] = numeros
                archivo = open("registros.dat", "w")
                archivo.write(str(numeros_usados))
                archivo.close()


            archivo = open("lista_fallas.dat", "r")
            fallas_generales = archivo.read()
            fallas_generales = eval(fallas_generales)
            archivo.close()


            fallas_generales[lista[0]] = tuple(lista[1:])
            archivo = open("lista_fallas.dat", "w")
            archivo.write(str(fallas_generales))
            archivo.close()

            if opcion == 1:
                ventana_crear_falla.destroy()
            if opcion == 2:
                ventana_modificar_falla.destroy()
            ventana_lista_de_fallas.destroy()
            lista_de_fallas()
    
    # FUNCION CREAR FALLA
    # ENTRADAS: 
    # SALIDAS: 
    def crear_falla():

        def salir_crear_falla():
            res = MessageBox.askyesno("CONFIRMACIÓN", "¿Seguro de que desea salir?")
            if res:
                ventana_crear_falla.destroy()
                ventana_lista_de_fallas.deiconify()
            return
    
        def validar_largo_texto1(*args):
             texto_f = d_falla.get("1.0", "end-1c")
             texto_n = n_falla.get("1.0", "end-1c")
             if len(texto_f) > 200:
                 nuevo_texto_f = texto_f[:200]
                 d_falla.delete("1.0", "end")
                 d_falla.insert("1.0", nuevo_texto_f)
             if len(texto_n) > 4:
                 nuevo_texto_n = texto_n[:4]
                 n_falla.delete("1.0", "end")
                 n_falla.insert("1.0", nuevo_texto_n)
        
        ventana_lista_de_fallas.iconify()    
        global ventana_crear_falla   
        ventana_crear_falla = Toplevel()
        ventana_crear_falla.resizable(False, False)
        ventana_crear_falla.title("Crear Falla")
        ancho_pantalla = ventana_crear_falla.winfo_screenwidth()
        alto_pantalla = ventana_crear_falla.winfo_screenheight()
        posicion_x = ancho_pantalla - 1000
        ventana_crear_falla.geometry(f"400x350+{posicion_x}+100")

        Label(ventana_crear_falla, text= "Crear Falla", width= 20, font= ("Franklin Gothic Demi", 15)).pack()
        Label(ventana_crear_falla, text= "Número de falla:", font= ("Franklin Gothic Demi", 12)).pack()
        n_falla = Text(ventana_crear_falla, height=1, width=4)
        n_falla.pack()
        n_falla.bind("<KeyRelease>", validar_largo_texto1)
        Label(ventana_crear_falla, text= "Descripcion de la falla:", font= ("Franklin Gothic Demi", 12)).pack()
        d_falla = Text(ventana_crear_falla, height=6, width=45)
        d_falla.pack()
        d_falla.bind("<KeyRelease>", validar_largo_texto1)
        tipo_de_falla = StringVar() 
        leve = Radiobutton(ventana_crear_falla, text="Leve", variable=tipo_de_falla, value="Leve").place(x= 145, y= 235)
        grave = Radiobutton(ventana_crear_falla, text="Grave", variable=tipo_de_falla, value="Grave").place(x= 205, y= 235)
        tipo_de_falla.set("Leve")
        Label(ventana_crear_falla, text= "Tipo de falla:", font= ("Franklin Gothic Demi", 12)).pack(pady= 6)
        Button(ventana_crear_falla, text= "Guardar", bg= "#0277fa", fg= "White", command= lambda: guardar_falla([n_falla.get("1.0", "end-1c"),d_falla.get("1.0", "end-1c"),tipo_de_falla.get()], 1, None)).place(x= 145, y= 290)
        Button(ventana_crear_falla, text= "Cancelar", bg= "#f94141", fg= "White", command= lambda: salir_crear_falla()).place(x= 205, y= 290)

        # Loop de la ventana.
        ventana_crear_falla.mainloop()

    # FUNCION MODIFICAR FALLA
    # ENTRADAS: 
    # SALIDAS:
    def modificar_falla(dato):

        def salir_modificar_falla():
            res = MessageBox.askyesno("CONFIRMACIÓN", "¿Seguro de que desea salir?")
            if res:
                ventana_modificar_falla.destroy()
                ventana_lista_de_fallas.deiconify()
            return

        def validar_largo_texto2(*args):
             texto_f = d_falla.get("1.0", "end-1c")
             if len(texto_f) > 200:
                 nuevo_texto_f = texto_f[:200]
                 d_falla.delete("1.0", "end")
                 d_falla.insert("1.0", nuevo_texto_f)

        ventana_lista_de_fallas.iconify()
        global ventana_modificar_falla
        ventana_modificar_falla = Toplevel()
        ventana_modificar_falla.resizable(False, False)
        ventana_modificar_falla.title("Modificar Falla")
        ancho_pantalla = ventana_modificar_falla.winfo_screenwidth()
        alto_pantalla = ventana_modificar_falla.winfo_screenheight()
        posicion_x = ancho_pantalla - 1000
        ventana_modificar_falla.geometry(f"400x460+{posicion_x}+100")

        archivo = open("lista_fallas.dat")
        datos_fallas = archivo.read()
        datos_fallas = eval(datos_fallas)
        archivo.close()

        Label(ventana_modificar_falla, text= "Modificar Falla", width= 20, font= ("Franklin Gothic Demi", 15)).pack()
        Label(ventana_modificar_falla, text= "Número de falla:", font= ("Franklin Gothic Demi", 12)).pack()
        Label(ventana_modificar_falla, text= dato[0], font= ("Arial", 9)).pack()
        Label(ventana_modificar_falla, text= "Descripción de la falla:", font= ("Franklin Gothic Demi", 12)).pack()
        Label(ventana_modificar_falla, text= dato[2], wraplength=300, font= ("Arial", 9)).pack()
        Label(ventana_modificar_falla, text= "Nueva descripción:", font= ("Franklin Gothic Demi", 12)).pack()
        d_falla = Text(ventana_modificar_falla, height=6, width=45)
        d_falla.pack()
        d_falla.bind("<KeyRelease>", validar_largo_texto2)
        tipo_de_falla = StringVar() 
        Label(ventana_modificar_falla, text= "Tipo de falla:", font= ("Franklin Gothic Demi", 12)).pack(pady= 6)
        leve = Radiobutton(ventana_modificar_falla, text="Leve", variable=tipo_de_falla, value="Leve").pack()
        grave = Radiobutton(ventana_modificar_falla, text="Grave", variable=tipo_de_falla, value="Grave").pack()
        tipo_de_falla.set("Leve")
        Button(ventana_modificar_falla, text= "Guardar", bg= "#0277fa", fg= "White", command= lambda: guardar_falla([dato[0], d_falla.get("1.0", "end-1c"),tipo_de_falla.get()], 2, dato[2])).place(x= 145, y= 400)
        Button(ventana_modificar_falla, text= "Cancelar", bg= "#f94141", fg= "White", command= lambda: salir_modificar_falla()).place(x= 205, y= 400)
        
        ventana_modificar_falla.mainloop()
        print("¡Hola! Has presionado el botón del label:", dato)
        return
    
    # FUNCION ELIMINAR FALLA
    # ENTRADAS: 
    # SALIDAS:
    def eliminar_falla(dato):
        respuesta = MessageBox.askyesno("CONFIRMACIÓN", "¿Seguro de que desea borrar la falla?")
        if respuesta:
            validar = 0
            if validar == 1:
                MessageBox.showerror("Error","Esta usandose")
                return
            else:
                numero_falla_borrar = dato[0]
                archivo = open("lista_fallas.dat", "r")
                fallas_generales = archivo.read()
                fallas_generales = eval(fallas_generales)
                archivo.close()

                del fallas_generales[numero_falla_borrar]

                archivo = open("lista_fallas.dat", "w")
                archivo.write(str(fallas_generales))
                archivo.close()

                archivo = open("registros.dat", "r")
                numeros_usados = archivo.read()
                numeros_usados = eval(numeros_usados)
                archivo.close()

                numeros_usados["fallas_usadas"].remove(numero_falla_borrar)
                archivo = open("registros.dat", "w")
                archivo.write(str(numeros_usados))
                archivo.close()
                
                ventana_lista_de_fallas.destroy()
                lista_de_fallas()

    # Esconder la ventana principal.
    ventana_principal.iconify()

    # Crear la ventana de lista de fallas.
    ventana_lista_de_fallas = Toplevel()
    ventana_lista_de_fallas.resizable(False, False)
    ventana_lista_de_fallas.title("Lista de fallas")
    ancho_pantalla = ventana_lista_de_fallas.winfo_screenwidth()
    alto_pantalla = ventana_lista_de_fallas.winfo_screenheight()
    posicion_x = ancho_pantalla - 1000
    ventana_lista_de_fallas.geometry(f"680x650+{posicion_x}+100")

    Label(ventana_lista_de_fallas, text= "Lista de fallas         ", width= 20, font= ("Franklin Gothic Demi", 16)).pack()
    Label(ventana_lista_de_fallas, text= "").pack(pady= 10)
    Button(ventana_lista_de_fallas, text= "Agregar Falla", width= 20, bg= "#0277fa", fg= "White", command= lambda: crear_falla()).place(x= 12, y= 75)
    Button(ventana_lista_de_fallas, text= "Salir", width= 10, bg= "#f94141", fg= "White", command= lambda: salir_fallas()).place(x= 585, y= 10)
    Label(ventana_lista_de_fallas, text= "", pady= 6).pack()
    Label(ventana_lista_de_fallas, text= "Número de Falla                                              ↓Descripcion↓                                       Tipo de Falla", font= ("Franklin Gothic Demi", 10)).place(x= 30, y= 120)

    # Crear un frame en la ventana.
    frame_fallas = Frame(ventana_lista_de_fallas)
    frame_fallas.pack(fill= BOTH, expand= 1, pady= 40)

    # Crear un canvas.
    canvas_fallas = Canvas(frame_fallas)
    canvas_fallas.pack(side= LEFT, fill= BOTH, expand= 1)

    # Crear el scrollbar en el canvas.
    scrollbar_fallas = Scrollbar(frame_fallas, orient= VERTICAL, command= canvas_fallas.yview)
    scrollbar_fallas.pack(side= RIGHT, fill= Y)

    # Configurar el canvas.
    canvas_fallas.configure(yscrollcommand= scrollbar_fallas.set)
    canvas_fallas.bind("<Configure>", lambda e: canvas_fallas.configure(scrollregion= canvas_fallas.bbox("all"))) 

    # Crear otro frame dentro del canvas.
    segundo_frame_fallas = Frame(canvas_fallas)

    # Agregar el nuevo frame a una ventana en el canvas.
    canvas_fallas.create_window((0, 0), window = segundo_frame_fallas, anchor= "nw")       

    Label(segundo_frame_fallas, text= "                                                                                                    ").grid(row= 3, column= 2)

    archivo = open("lista_fallas.dat", "r")
    fallas_generales = archivo.read()
    fallas_generales = eval(fallas_generales)
    archivo.close()

    labels_textos = list()
    for elemento in fallas_generales:
        labels_textos.append([elemento,fallas_generales[elemento][1],fallas_generales[elemento][0]])

    contador = 5
    for texto in labels_textos:
        print(texto)
        # Crear el label
        label_f = Label(segundo_frame_fallas, text=texto[0])
        label_f.grid(row= contador, column= 1)
        Label(segundo_frame_fallas, text="────────────").grid(row= contador + 1, column= 1)
        label_t = Label(segundo_frame_fallas, text=texto[1])
        label_t.grid(row= contador, column= 3)
        Label(segundo_frame_fallas, text="──────").grid(row= contador + 1, column= 3)
        label_d = Label(segundo_frame_fallas, text=texto[2], wraplength=300)
        label_d.grid(row= contador, column= 2)
        Label(segundo_frame_fallas, text="────────────────────────").grid(row= contador + 1, column= 2)

        # Crear el botón y vincularlo a la función modificar o borrar
        boton_up = Button(segundo_frame_fallas, text="Modificar", bg= "#0277fa", fg= "White", command=lambda text=texto: modificar_falla(text))
        boton_up.grid(row= contador, column= 4)
        Label(segundo_frame_fallas, text="────").grid(row= contador + 1, column= 4)
        boton_del = Button(segundo_frame_fallas, text="Borrar", bg= "#f94141", fg= "White", command=lambda text=texto: eliminar_falla(text))
        boton_del.grid(row= contador, column= 5)
        Label(segundo_frame_fallas, text="────").grid(row= contador + 1, column= 5)

        contador += 2

    # Loop de la ventana.
    ventana_lista_de_fallas.mainloop()






















""" FUNCION PARA ABRIR LA VENTANA DE CONFIGURACION DEL SISTEMA
# ENTRADAS: Lee las opciones seleccionadas por el usuario.
# SALIDAS: Guarda los cambios en un archivo predefinido. """
def ventana_configuracion_sistema():

    MessageBox.showinfo("ESTADO", "Si efectúa un cambio, presione el botón cerrar ventana. \n(Se encuentra al final de la ventana).")

    archivo = open("configuración_reteve.dat", "r")
    datos_originales = archivo.read()
    datos_originales = eval(datos_originales)
    archivo.close()

    def guardar_cerrar_config():
        res = MessageBox.askyesno("CONFIRMAR", "¿Está seguro de que desea guardar los cambios?")
        if res:
            MessageBox.showinfo("ESTADO", "Guardando datos. \n(Se cerrará el programa).")

            archivo = open("configuración_reteve.dat", "w")
            archivo.write(str(datos_originales))
            archivo.close()

            ventana_config.destroy()
            ventana_principal.destroy()
            return
        return
    
    def cerrar_config():
        res = MessageBox.askyesno("CONFIRMAR", "¿Está seguro de que desea cerrar la ventana? \n(No se guardarán los cambios)")
        if res:
            ventana_principal.deiconify()
            ventana_config.destroy()
        return
    
    # FUNCION QUE GUARDA LA OPCION DE LINEAS DE TRABAJO
    # ENTRADAS: Recibe el nuevo dato de lineas de trabajo.
    # SALIDAS: Si la opción es válida se guarda, de lo contrario envía el error respectivo.
    def guardar_lineas_trabajo(dato):

        archivo = open("lista_colas.dat", "r")
        colas = archivo.read()
        colas = eval(colas)
        archivo.close()

        if int(dato) < datos_originales[0]:
            for lista in colas:
                if len(lista[1]) > 0:
                    MessageBox.showerror("ERROR", "Hay colas ocupadas actualmente.")
                    return
                if len(lista[2][0]) > 0:
                    MessageBox.showerror("ERROR", "Hay colas ocupadas actualmente.")
                    return
                if len(lista[2][1]) > 0:
                    MessageBox.showerror("ERROR", "Hay colas ocupadas actualmente.")
                    return
                if len(lista[2][2]) > 0:
                    MessageBox.showerror("ERROR", "Hay colas ocupadas actualmente.")
                    return
                if len(lista[2][3]) > 0:
                    MessageBox.showerror("ERROR", "Hay colas ocupadas actualmente.")
                    return
                if len(lista[2][4]) > 0:
                    MessageBox.showerror("ERROR", "Hay colas ocupadas actualmente.")
                    return

        datos_originales[0] = int(dato)
        MessageBox.showinfo("ESTADO", "Los datos se han guardado correctamente.")
    
    # FUNCION QUE GUARDA LAS HORAS DE TRABAJO DE LA ESTACIÓN
    # ENTRADAS: Recibe la hora inicial y la hora final.
    # SALIDAS: Si la opción es válida se guarda, de lo contrario envía el error respectivo.
    def guardar_horas(dato1, dato2):
        inicial = int(dato1[0:2])
        final = int(dato2[0:2])

        if final >= inicial:
            
            datos_originales[1] = dato1
            datos_originales[2] = dato2
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

            datos_originales[indice] = dato
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

        datos_originales[8][indice] = dato
        MessageBox.showinfo("ESTADO", "Los datos se han guardado correctamente.")
        return
    
    ventana_principal.iconify()

    # Crear la ventana de configuración.
    ventana_config = Toplevel()
    ventana_config.resizable(False, False)
    ventana_config.title("Configuración del sistema")
    ancho_pantalla = ventana_config.winfo_screenwidth()
    alto_pantalla = ventana_config.winfo_screenheight()
    posicion_x = ancho_pantalla - 1000
    ventana_config.geometry(f"500x700+{posicion_x}+100")

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
    Button(segundo_frame_config, text= "Cambiar", bg= "#73B6E7", command= lambda: guardar_lineas_trabajo(combo_lineas.get())).pack()
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
    Button(segundo_frame_config, text= "Cambiar", bg= "#73B6E7", command= lambda: guardar_horas(combo_hora_inicial.get(), combo_hora_final.get())).pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()

    # Minutos por cada cita de revisión.
    opciones_minutos_cita = ["00:05", "00:10", "00:15", "00:20", "00:25", "00:30", "00:35", "00:40", "00:45"]
    Label(segundo_frame_config, text="Minutos por cada cita de revisión:", font=("Arial", 12)).pack()
    combo_minutos_cita = ttk.Combobox(segundo_frame_config, values= opciones_minutos_cita, state="readonly")
    combo_minutos_cita.pack()
    Label(segundo_frame_config, text="").pack()
    Button(segundo_frame_config, text= "Cambiar", bg= "#73B6E7", command= lambda: guardar_general(combo_minutos_cita.get(), 3)).pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()

    # Cantidad máxima de días naturales para reinspección.
    opciones_dias_reinspeccion = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60]
    Label(segundo_frame_config, text="Cantidad máxima de días naturales para reinspección:", font=("Arial", 12)).pack()
    combo_dias_reinspeccion = ttk.Combobox(segundo_frame_config, values= opciones_dias_reinspeccion, state= "readonly")
    combo_dias_reinspeccion.pack()
    Label(segundo_frame_config, text="").pack()
    Button(segundo_frame_config, text= "Cambiar", bg= "#73B6E7", command= lambda: guardar_general(combo_dias_reinspeccion.get(), 4)).pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()

    # Cantidad de fallas graves para sacar vehículo de circulación.
    Label(segundo_frame_config, text="Cantidad de fallas graves para sacar vehículo de circulación:", font=("Arial", 12)).pack()
    entrada_fallas_graves = Entry(segundo_frame_config, width= 5, border= 4)
    entrada_fallas_graves.pack()
    indicador_fallas_graves = Label(segundo_frame_config, text= "Actual: Ninguno")
    indicador_fallas_graves.pack()
    Label(segundo_frame_config, text="").pack()
    Button(segundo_frame_config, text= "Cambiar", bg= "#73B6E7", command= lambda: guardar_general(entrada_fallas_graves.get(), 5)).pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()

    # Cantidad de meses.
    opciones_meses = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    Label(segundo_frame_config, text="Cantidad de meses que se van a considerar para desplegar todas \nlas citas disponibles en la asignación automática de citas:", font=("Arial", 12)).pack()
    combo_meses = ttk.Combobox(segundo_frame_config, values= opciones_meses, state= "readonly")
    combo_meses.pack()
    Label(segundo_frame_config, text="").pack()
    Button(segundo_frame_config, text= "Cambiar", bg= "#73B6E7", command= lambda: guardar_general(combo_meses.get(), 6)).pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()

    # Porcentaje de Impuesto al Valor Agregado (IVA) sobre la tarifa.
    Label(segundo_frame_config, text="Porcentaje de Impuesto al Valor Agregado (IVA) sobre la tarifa:", font=("Arial", 12)).pack()
    entrada_impuesto_iva = Entry(segundo_frame_config, width= 5, border= 4)
    entrada_impuesto_iva.pack()
    indicador_impuesto_iva = Label(segundo_frame_config, text= "Actual: Ninguno")
    indicador_impuesto_iva.pack()
    Label(segundo_frame_config, text="").pack()
    Button(segundo_frame_config, text= "Cambiar", bg= "#73B6E7", command= lambda: guardar_general(entrada_impuesto_iva.get(), 7)).pack()
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
    Button(segundo_frame_config, text= "Cambiar", bg= "#73B6E7", command= lambda: guardar_tarifas(entrada_tarifa_1.get(), 0)).pack()
    indicador_tarifa_1 = Label(segundo_frame_config, text="Tarifa actual: Ninguno", font=("Franklin Gothic Demi", 10))
    indicador_tarifa_1.pack()

    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()
    Label(segundo_frame_config, text="Vehículo:", font=("Arial", 10)).pack()
    Label(segundo_frame_config, text="Automóvil particular y vehículo de carga liviana \n(mayor a 3500 kg pero menor a 8000 kg)", font=("Franklin Gothic Demi", 10)).pack()
    Label(segundo_frame_config, text="Tarifa nueva:", font=("Arial", 10)).pack()
    entrada_tarifa_2 = Entry(segundo_frame_config, width= 8, border= 4)
    entrada_tarifa_2.pack()
    Button(segundo_frame_config, text= "Cambiar", bg= "#73B6E7", command= lambda: guardar_tarifas(entrada_tarifa_2.get(), 1)).pack()
    indicador_tarifa_2 = Label(segundo_frame_config, text="Tarifa actual: Ninguno", font=("Franklin Gothic Demi", 10))
    indicador_tarifa_2.pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()

    Label(segundo_frame_config, text="Vehículo:", font=("Arial", 10)).pack()
    Label(segundo_frame_config, text="Vehículo de carga pesada y cabezales \n(mayor o igual a 8000 kg)", font=("Franklin Gothic Demi", 10)).pack()
    Label(segundo_frame_config, text="Tarifa:", font=("Arial", 10)).pack()
    entrada_tarifa_3 = Entry(segundo_frame_config, width= 8, border= 4)
    entrada_tarifa_3.pack()
    Button(segundo_frame_config, text= "Cambiar", bg= "#73B6E7", command= lambda: guardar_tarifas(entrada_tarifa_3.get(), 2)).pack()
    indicador_tarifa_3 = Label(segundo_frame_config, text="Tarifa actual: Ninguno", font=("Franklin Gothic Demi", 10))
    indicador_tarifa_3.pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()

    Label(segundo_frame_config, text="Vehículo:", font=("Arial", 10)).pack()
    Label(segundo_frame_config, text="Taxis", font=("Franklin Gothic Demi", 10)).pack()
    Label(segundo_frame_config, text="Tarifa:", font=("Arial", 10)).pack()
    entrada_tarifa_4 = Entry(segundo_frame_config, width= 8, border= 4)
    entrada_tarifa_4.pack()
    Button(segundo_frame_config, text= "Cambiar", bg= "#73B6E7", command= lambda: guardar_tarifas(entrada_tarifa_4.get(), 3)).pack()
    indicador_tarifa_4 = Label(segundo_frame_config, text="Tarifa actual: Ninguno", font=("Franklin Gothic Demi", 10))
    indicador_tarifa_4.pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()

    Label(segundo_frame_config, text="Vehículo:", font=("Arial", 10)).pack()
    Label(segundo_frame_config, text="Autobuses, buses y microbuses", font=("Franklin Gothic Demi", 10)).pack()
    Label(segundo_frame_config, text="Tarifa:", font=("Arial", 10)).pack()
    entrada_tarifa_5 = Entry(segundo_frame_config, width= 8, border= 4)
    entrada_tarifa_5.pack()
    Button(segundo_frame_config, text= "Cambiar", bg= "#73B6E7", command= lambda: guardar_tarifas(entrada_tarifa_5.get(), 4)).pack()
    indicador_tarifa_5 = Label(segundo_frame_config, text="Tarifa actual: Ninguno", font=("Franklin Gothic Demi", 10))
    indicador_tarifa_5.pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()

    Label(segundo_frame_config, text="Vehículo:", font=("Arial", 10)).pack()
    Label(segundo_frame_config, text="Motocicletas", font=("Franklin Gothic Demi", 10)).pack()
    Label(segundo_frame_config, text="Tarifa:", font=("Arial", 10)).pack()
    entrada_tarifa_6 = Entry(segundo_frame_config, width= 8, border= 4)
    entrada_tarifa_6.pack()
    Button(segundo_frame_config, text= "Cambiar", bg= "#73B6E7", command= lambda: guardar_tarifas(entrada_tarifa_6.get(), 5)).pack()
    indicador_tarifa_6 = Label(segundo_frame_config, text="Tarifa actual: Ninguno", font=("Franklin Gothic Demi", 10))
    indicador_tarifa_6.pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()

    Label(segundo_frame_config, text="Vehículo:", font=("Arial", 10)).pack()
    Label(segundo_frame_config, text="Equipo especial de obras", font=("Franklin Gothic Demi", 10)).pack()
    Label(segundo_frame_config, text="Tarifa:", font=("Arial", 10)).pack()
    entrada_tarifa_7 = Entry(segundo_frame_config, width= 8, border= 4)
    entrada_tarifa_7.pack()
    Button(segundo_frame_config, text= "Cambiar", bg= "#73B6E7", command= lambda: guardar_tarifas(entrada_tarifa_7.get(), 6)).pack()
    indicador_tarifa_7 = Label(segundo_frame_config, text="Tarifa actual: Ninguno", font=("Franklin Gothic Demi", 10))
    indicador_tarifa_7.pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()

    Label(segundo_frame_config, text="Vehículo:", font=("Arial", 10)).pack()
    Label(segundo_frame_config, text="Equipo especial agrícola \n(maquinaria agrícola)", font=("Franklin Gothic Demi", 10)).pack()
    Label(segundo_frame_config, text="Tarifa:", font=("Arial", 10)).pack()
    entrada_tarifa_8 = Entry(segundo_frame_config, width= 8, border= 4)
    entrada_tarifa_8.pack()
    Button(segundo_frame_config, text= "Cambiar", bg= "#73B6E7", command= lambda: guardar_tarifas(entrada_tarifa_8.get(), 7)).pack()
    indicador_tarifa_8 = Label(segundo_frame_config, text="Tarifa actual: Ninguno", font=("Franklin Gothic Demi", 10))
    indicador_tarifa_8.pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()
    Label(segundo_frame_config, text="").pack()
    Button(segundo_frame_config, text= "Guardar", bg= "#0277fa", fg= "White", command= lambda: guardar_cerrar_config()).place(x= 170, y= 2510)
    Button(segundo_frame_config, text= "Cancelar", bg= "#f94141", fg= "White", command= lambda: cerrar_config()).place(x= 240, y= 2510)
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
    def cerrar_acerca():
        ventana_principal.deiconify()
        ventana_de_informacion.destroy()
        return
    
    # Crear la ventana de información.
    ventana_principal.iconify()
    ventana_de_informacion = Toplevel()
    ventana_de_informacion.resizable(False, False)
    ventana_de_informacion.title("Acerca de")
    ventana_de_informacion.config(bg="White")
    ancho_pantalla = ventana_de_informacion.winfo_screenwidth()
    alto_pantalla = ventana_de_informacion.winfo_screenheight()
    posicion_x = ancho_pantalla - 1000
    ventana_de_informacion.geometry(f"310x390+{posicion_x}+100")

    # Mostrar la información del programa.
    Label(ventana_de_informacion, text= "\nAcerca del programa\n", fg="black", bg="white", font=("Franklin Gothic Demi", 16)).pack()
    Label(ventana_de_informacion, text="Nombre del programa: ReTeVe\n \nVersión del programa: 1.0.0\n \
          \nFecha de creación: 01 de Junio del 2023\n \nÚltima modificación: 01 de Junio del 2023\n \nAutores:\n \
          \nJose Mario Jiménez Vargas\n \nJohn Sebastián Ceciliano Piedra", fg="black", bg="white", font=("Arial", 10)).pack()

    # Botón para cerrar la ventana.
    boton_aceptar = Button(ventana_de_informacion, text="Aceptar", command= lambda: cerrar_acerca())
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
    inicio = datetime(año_hoy, mes_hoy, dia_hoy + 1)  # Fecha de inicio
    fecha_final = validar_fecha_fin(año_hoy, mes_hoy + datos_originales[6], dia_hoy + 1)
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

# FUNCION QUE VALIDA QUE LAS LINEAS DE TRABAJO ACTUALES SEAN IGUALES A LA CONFIGURACION
# ENTRADAS: Lee los archivos de config y de colas.
# SALIDAS: Corrige el archivo de cola si es necesario.
def validar_lineas():
    archivo = open("lista_colas.dat", "r")
    lineas_actuales = archivo.read()
    lineas_actuales = eval(lineas_actuales)
    archivo.close()

    archivo = open("configuración_reteve.dat", "r")
    config = archivo.read()
    config = eval(config)
    archivo.close()

    largo_inicial = len(lineas_actuales)

    if len(lineas_actuales) < config[0]:
        contador = 1
        while len(lineas_actuales) < config[0]:
            lineas_actuales.append([str(largo_inicial + contador), [], [[], [], [], [], []]])
            contador += 1

        archivo = open("lista_colas.dat", "w")
        lineas_actuales = archivo.write(str(lineas_actuales))
        archivo.close()
    return

""" FUNCION PRINCIPAL """
manual = True
fecha_hoy = str()
valores_lista = list()
datos_del_ingreso = list()

# Ventana principal.
ventana_principal = Tk()
ventana_principal.geometry("600x700")
ventana_principal.resizable(False, False)
ventana_principal.title("ReTeVe")
ancho_pantalla = ventana_principal.winfo_screenwidth()
alto_pantalla = ventana_principal.winfo_screenheight()
posicion_x = ancho_pantalla -1000
ventana_principal.geometry(f"600x700+{posicion_x}+100")

# Indicador de fecha y hora en la ventana.
label_fecha_hora = Label(ventana_principal, font=("Arial", 14))
label_fecha_hora.place(x=400,y=10)
actualizar_fecha_hora()
generar_lista_intervalo()
validar_lineas()

# Opciones de citas.
Label(ventana_principal, text="").pack()
Label(ventana_principal, text="Citas", font=("Comic Sans MS", 16)).pack()
boton_a = Button(ventana_principal, text="Programar citas", font=("Arial", 12), command= lambda: programar_citas())
boton_a.pack()
boton_b = Button(ventana_principal, text="Cancelar citas", font=("Arial", 12), command= lambda: cancelar_citas())
boton_b.pack()

# Opciones de vehículos.
Label(ventana_principal, text="").pack()
Label(ventana_principal, text="Vehículos", font=("Comic Sans MS", 16)).pack()
boton_c = Button(ventana_principal, text="Ingreso de vehículos a la estación", font=("Arial", 12), command= lambda: ingreso_a_estacion())
boton_c.pack()

# Opciones de revisiones.
Label(ventana_principal, text="").pack()
Label(ventana_principal, text="Revisiones", font=("Comic Sans MS", 16)).pack()
boton_d = Button(ventana_principal, text="Tablero de revisión", font=("Arial", 12), command= lambda: tablero())
boton_d.pack()
boton_e = Button(ventana_principal, text="Lista de fallas", font=("Arial", 12), command= lambda: lista_de_fallas())
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