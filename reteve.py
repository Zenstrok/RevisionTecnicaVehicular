# Autores: Jose Mario / John Sebastián

""" MODULOS """
import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as MessageBox

""" FUNCIONES """

def programar_citas():

    def programar_cita_nueva():
        print("Hola")
        return

    def validar_datos_cita():
        # Validar el número de placa.
        dato = entry2.get()
        if dato == "":
            MessageBox.showerror("ERROR", "Dato de placa inválido.")
            return
        if len(dato) > 8 or len(dato) < 1:
            MessageBox.showerror("ERROR", "Dato de placa inválido.")
            return
        
        # Validar la marca del vehículo.
        dato = entry4.get()
        if dato == "":
            MessageBox.showerror("ERROR", "Marca de vehículo inválida.")
            return
        if len(dato) > 15 or len(dato) < 3:
            MessageBox.showerror("ERROR", "Marca de vehiculo inválida.")
            return

        # Validar modelo del vehículo.
        dato = entry5.get()
        if dato == "":
            MessageBox.showerror("ERROR", "Modelo del vehículo inválido.")
            return
        if len(dato) > 15 or len(dato) < 1:
            MessageBox.showerror("ERROR", "Modelo del vehiculo inválido.")
            return
        
        # Validar propietario del vehículo.
        dato = entry6.get()
        if dato == "":
            MessageBox.showerror("ERROR", "Propietario del vehículo inválido.")
            return
        if len(dato) > 40 or len(dato) < 6:
            MessageBox.showerror("ERROR", "Propietario del vehiculo inválido.")
            return
        
        # Validar teléfono.
        dato = entry7.get()
        if dato == "":
            MessageBox.showerror("ERROR", "Teléfono inválido.")
            return
        if len(dato) > 20 or len(dato) < 6:
            MessageBox.showerror("ERROR", "Teléfono inválido.")
            return
        
        # Validar correo electrónico.
        dato = entry8.get()
        if dato == "":
            MessageBox.showerror("ERROR", "Correo electrónico inválido o inexistente.")
            return
        #FALTA

        # Validar dirección física.
        dato = entry9.get()
        if dato == "":
            MessageBox.showerror("ERROR", "Dirección física inválida.")
            return
        if len(dato) > 40 or len(dato) < 10:
            MessageBox.showerror("ERROR", "Dirección física inválida.")
            return
        
        programar_cita_nueva()
    
    def fecha_hora_manual():

        return
    
    def fecha_hora_automatico():

        return
    
    tipos_de_vehículos = ["Automóvil particular y vehículo de carga liviana (<= 3500 kg)", \
                          "Automóvil particular y vehículo de carga liviana (3500 kg > 8000 kg)", \
                            "Vehículo de carga pesada y cabezales (>= 8000 kg)", "Taxis", \
                                "Autobuses, buses y microbuses", "Motocicletas", "Equipo especial de obras", \
                                    "Equipo especial agrícola (maquinaria agrícola)"]

    ventana_programar_citas = Toplevel()
    ventana_programar_citas.geometry("600x700")
    ventana_programar_citas.resizable(False, False)
    ventana_programar_citas.title("Programar Citas")

    Label(ventana_programar_citas, text= "Programar Citas", font= ("Arial", 16)).place(x= 220, y= 10)
    Label(ventana_programar_citas, text= "Tipo de cita: ", font= ("Franklin Gothic Demi", 12)).place(x= 10, y= 50)


    tipo_c = StringVar(value = 0) 
    p_v = Radiobutton(ventana_programar_citas, text="Primera Vez", variable=tipo_c, value="Primera Vez").place(x= 110, y= 53)
    r_i = Radiobutton(ventana_programar_citas, text="Reinspeccion", variable=tipo_c, value="Reinspeccion").place(x= 200, y= 53)
    



    
    Label(ventana_programar_citas, text= "Número de placa: ", font= ("Franklin Gothic Demi", 12)).place(x= 10, y= 100)
    entry2 = Entry(ventana_programar_citas, width=40)
    entry2.place(x= 145, y= 105)

    Label(ventana_programar_citas, text= "Tipo de vehículo: ", font= ("Franklin Gothic Demi", 12)).place(x= 10, y= 150)
    entry3 = ttk.Combobox(ventana_programar_citas, values= tipos_de_vehículos, width= 60, state= "readonly")
    entry3.place(x= 140, y= 155)

    Label(ventana_programar_citas, text= "Marca del vehículo: ", font= ("Franklin Gothic Demi", 12)).place(x= 10, y= 200)
    entry4 = Entry(ventana_programar_citas, width= 40)
    entry4.place(x= 160, y= 205)

    Label(ventana_programar_citas, text= "Modelo: ", font= ("Franklin Gothic Demi", 12)).place(x= 10, y= 250)
    entry5 = Entry(ventana_programar_citas, width= 40)
    entry5.place(x= 80, y= 255)

    Label(ventana_programar_citas, text= "Propietario: ", font= ("Franklin Gothic Demi", 12)).place(x= 10, y= 300)
    entry6 = Entry(ventana_programar_citas, width= 40)
    entry6.place(x= 110, y= 305)

    Label(ventana_programar_citas, text= "Teléfono: ", font= ("Franklin Gothic Demi", 12)).place(x= 10, y= 350)
    entry7 = Entry(ventana_programar_citas, width= 40)
    entry7.place(x= 90, y= 355)

    Label(ventana_programar_citas, text= "Correo electrónico: ", font= ("Franklin Gothic Demi", 12)).place(x= 10, y= 400)
    entry8 = Entry(ventana_programar_citas, width= 40)
    entry8.place(x= 160, y= 405)

    Label(ventana_programar_citas, text= "Dirección física: ", font= ("Franklin Gothic Demi", 12)).place(x= 10, y= 450)
    entry9 = Entry(ventana_programar_citas, width= 40)
    entry9.place(x= 140, y= 455)

    Label(ventana_programar_citas, text= "Fecha y hora de la cita: ", font= ("Franklin Gothic Demi", 12)).place(x= 10, y= 500)
    boton_manual = Button(ventana_programar_citas, text= "Manual", command= None)
    boton_manual.place(x= 190, y= 500)
    boton_auto = Button(ventana_programar_citas, text= "Automático", command= None)
    boton_auto.place(x= 250, y= 500)

    Button(ventana_programar_citas, text= "Programar Cita", width= 20, height= 2, font= ("Franklin Gothic Demi", 10), command= lambda: validar_datos_cita()).place(x= 140, y= 555)
    Button(ventana_programar_citas, text= "Cerrar ventana", width= 20, height= 2, font= ("Franklin Gothic Demi", 10), command= lambda: ventana_programar_citas.destroy()).place(x= 300, y= 555)

    tipo_c.set("Primera Vez")
    entry3.set("Automóvil particular y vehículo de carga liviana (<= 3500 kg)")

    ventana_programar_citas.mainloop()
    return

""" FUNCION PARA ABRIR LA VENTANA DE CONFIGURACION DEL SISTEMA
# ENTRADAS: Lee las opciones seleccionadas por el usuario.
# SALIDAS: Guarda los cambios en un archivo predefinido. """
def ventana_configuracion_sistema():

    def guardar_lineas_trabajo(dato):
        archivo = open("configuración_reteve.dat", "r")
        datos_originales = archivo.read()
        datos_originales = eval(datos_originales)
        dato_comparar = datos_originales[0]
        archivo.close()

        if int(dato) >= dato_comparar:
            archivo = open("configuración_reteve.dat", "w")
            datos_originales[0] = int(dato)
            print(datos_originales)
            archivo.write(str(datos_originales))
            archivo.close()
            MessageBox.showinfo("ESTADO", "Los datos se han guardado correctamente.")
        else:
            MessageBox.showerror("ERROR", "No se puede ejecutar la acción.")
            pass
    
    def guardar_horas(inicial, final):
        inicial = int(inicial)
        final = int(final)

        if final >= inicial:
            archivo = open("configuración_reteve.dat", "r")
            datos_originales = archivo.read()
            datos_originales = eval(datos_originales)
            archivo.close()

            archivo = open("configuración_reteve.dat", "w")
            datos_originales[1] = inicial
            datos_originales[2] = final
            archivo.write(str(datos_originales))
            archivo.close()

            MessageBox.showinfo("ESTADO", "Los datos se han guardado correctamente.")
        else:
            MessageBox.showerror("ERROR", "No se pudo guardar \n(hora inicial mayor que la final).")
        return

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
            else:
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
            datos_originales[indice] = dato
            print(datos_originales)
            archivo.write(str(datos_originales))
            archivo.close()

            MessageBox.showinfo("ESTADO", "Los datos se han guardado correctamente.")
        else:
            MessageBox.showerror("ERROR", "No hay ningún dato registrado o es un dato incorrecto.")
        return
    
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
    opciones_horario = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
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
    opciones_minutos_cita = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45]
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


""" FUNCION PRINCIPAL """

# Ventana principal.
ventana_principal = Tk()
ventana_principal.geometry("600x700")
ventana_principal.resizable(False, False)
ventana_principal.title("ReTeVe")

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