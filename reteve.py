# Autores: Jose Mario / John Sebastián

""" MODULOS """
import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as MessageBox

""" FUNCIONES """

def boton_programar_citas():
    return

""" FUNCION PARA ABRIR LA VENTANA DE CONFIGURACION DEL SISTEMA
# ENTRADAS: Lee las opciones seleccionadas por el usuario.
# SALIDAS: Guarda los cambios en un archivo predefinido. """
def ventana_configuracion_sistema():

    def guardar_lineas_trabajo():
        return
    
    def guardar_fechas():
        return

    def guardar_general(dato, indice):
        if dato != "":
            dato = int(dato)
        archivo = open("configuración_reteve.dat", "r")
        datos_originales = archivo.read()
        datos_originales = eval(datos_originales)
        archivo.close()

        archivo = open("configuración_reteve.dat", "w")
        datos_originales[indice] = dato
        print(datos_originales)
        archivo.write(str(datos_originales))
        archivo.close()
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
    Button(segundo_frame_config, text= "Guardar", command= lambda: guardar_lineas_trabajo()).pack()
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
    Button(segundo_frame_config, text= "Guardar", command= lambda: guardar_fechas(combo_hora_inicial.get(), combo_hora_final.get())).pack()
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
    
    Label(segundo_frame_config, text="Vehículo:").pack()
    Label(segundo_frame_config, text="Automóvil particular y vehículo de carga liviana", font=("Franklin Gothic Demi", 9)).pack()
    Label(segundo_frame_config, text="Tarifa:").pack()
    entrada_tarifa_1 = Entry(segundo_frame_config, width= 5, border= 4)
    entrada_tarifa_1.pack()
    indicador_tarifa_1 = Label(segundo_frame_config, text="Actual: Ninguno")
    indicador_tarifa_1.pack()

    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()
    Label(segundo_frame_config, text="Vehículo:").pack()
    Label(segundo_frame_config, text="Automóvil particular y vehículo de carga liviana", font=("Franklin Gothic Demi", 9)).pack()
    Label(segundo_frame_config, text="Tarifa:").pack()
    entrada_tarifa_2 = Entry(segundo_frame_config, width= 5, border= 4)
    entrada_tarifa_2.pack()
    indicador_tarifa_2 = Label(segundo_frame_config, text="Actual: Ninguno")
    indicador_tarifa_2.pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()

    Label(segundo_frame_config, text="Vehículo:").pack()
    Label(segundo_frame_config, text="Automóvil particular y vehículo de carga liviana", font=("Franklin Gothic Demi", 9)).pack()
    Label(segundo_frame_config, text="Tarifa:").pack()
    entrada_tarifa_3 = Entry(segundo_frame_config, width= 5, border= 4)
    entrada_tarifa_3.pack()
    indicador_tarifa_3 = Label(segundo_frame_config, text="Actual: Ninguno")
    indicador_tarifa_3.pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()

    Label(segundo_frame_config, text="Vehículo:").pack()
    Label(segundo_frame_config, text="Automóvil particular y vehículo de carga liviana", font=("Franklin Gothic Demi", 9)).pack()
    Label(segundo_frame_config, text="Tarifa:").pack()
    entrada_tarifa_4 = Entry(segundo_frame_config, width= 5, border= 4)
    entrada_tarifa_4.pack()
    indicador_tarifa_4 = Label(segundo_frame_config, text="Actual: Ninguno")
    indicador_tarifa_4.pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()

    Label(segundo_frame_config, text="Vehículo:").pack()
    Label(segundo_frame_config, text="Automóvil particular y vehículo de carga liviana", font=("Franklin Gothic Demi", 9)).pack()
    Label(segundo_frame_config, text="Tarifa:").pack()
    entrada_tarifa_5 = Entry(segundo_frame_config, width= 5, border= 4)
    entrada_tarifa_5.pack()
    indicador_tarifa_5 = Label(segundo_frame_config, text="Actual: Ninguno")
    indicador_tarifa_5.pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()

    Label(segundo_frame_config, text="Vehículo:").pack()
    Label(segundo_frame_config, text="Automóvil particular y vehículo de carga liviana", font=("Franklin Gothic Demi", 9)).pack()
    Label(segundo_frame_config, text="Tarifa:").pack()
    entrada_tarifa_6 = Entry(segundo_frame_config, width= 5, border= 4)
    entrada_tarifa_6.pack()
    indicador_tarifa_6 = Label(segundo_frame_config, text="Actual: Ninguno")
    indicador_tarifa_6.pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()

    Label(segundo_frame_config, text="Vehículo:").pack()
    Label(segundo_frame_config, text="Automóvil particular y vehículo de carga liviana", font=("Franklin Gothic Demi", 9)).pack()
    Label(segundo_frame_config, text="Tarifa:").pack()
    entrada_tarifa_7 = Entry(segundo_frame_config, width= 5, border= 4)
    entrada_tarifa_7.pack()
    indicador_tarifa_7 = Label(segundo_frame_config, text="Actual: Ninguno")
    indicador_tarifa_7.pack()
    Label(segundo_frame_config, text="-------------------------------------------------------------------------------------------", font=("Arial", 12)).pack()

    Label(segundo_frame_config, text="Vehículo:").pack()
    Label(segundo_frame_config, text="Automóvil particular y vehículo de carga liviana", font=("Franklin Gothic Demi", 9)).pack()
    Label(segundo_frame_config, text="Tarifa:").pack()
    entrada_tarifa_8 = Entry(segundo_frame_config, width= 5, border= 4)
    entrada_tarifa_8.pack()
    indicador_tarifa_8 = Label(segundo_frame_config, text="Actual: Ninguno")
    indicador_tarifa_8.pack()
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
    texto_nuevo_1 = "Actual: " + str(datos_totales[5])
    indicador_fallas_graves.config(text= texto_nuevo_1)
    texto_nuevo_2 = "Actual: " + str(datos_totales[7])
    indicador_impuesto_iva.config(text= texto_nuevo_2)

    # Loop de la ventana.
    ventana_config.mainloop()

""" FUNCION PARA ABRIR EL MANUAL DE USUARIO
# ENTRADAS: Lee la respuesta del usuario en el messagebox.
# SALIDAS: Si el usuario responde 'sí', abre el manual de usuario. """
def ayuda_de_programa():
    if MessageBox.askyesno("CONFIRMAR", "¿Seguro de que desea abrir el manual?"):
        os.startfile("manual_de_usuario_reteve.docx") # Abrir el manual.
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
boton_a = Button(ventana_principal, text="Programar citas", font=("Arial", 12), command= lambda: boton_programar_citas())
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