import json
import tkinter as tk
from tkinter import ttk

# Función para cargar la lista de contenido desde un archivo JSON
def cargar_lista():
    try:
        with open("lista_contenido.json", "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return {"Peliculas": {"Visto": [], "Pendiente": [], "Viendo": []},
                "Series": {"Visto": [], "Pendiente": [], "Viendo": []},
                "Anime": {"Visto": [], "Pendiente": [], "Viendo": []}}

# Función para guardar la lista de contenido en un archivo JSON
def guardar_lista(lista):
    with open("lista_contenido.json", "w") as archivo:
        json.dump(lista, archivo, indent=4)

# Función para agregar un elemento a la lista
def agregar_elemento():
    categoria = categoria_var.get()
    estado = estado_var.get()
    elemento = entrada_elemento.get()
    if categoria and estado and elemento:
        lista_contenido[categoria][estado].append(elemento)
        guardar_lista(lista_contenido)
        actualizar_lista()
        entrada_elemento.delete(0, "end")

# Función para borrar un elemento de la lista
def borrar_elemento():
    seleccionado = lista_box.curselection()
    if seleccionado:
        categoria = categoria_var.get()
        estado = estado_var.get()
        indice = seleccionado[0]
        elemento = lista_box.get(indice)
        elemento = elemento.split(".")[1].strip()
        lista_contenido[categoria][estado].remove(elemento)
        guardar_lista(lista_contenido)
        actualizar_lista()

# Función para mostrar la lista de elementos en una categoría y estado específicos
def mostrar_lista(categoria, estado):
    if categoria and estado:
        return lista_contenido[categoria][estado]
    return []

# Función para actualizar la lista mostrada en la interfaz
def actualizar_lista(event=None):
    categoria = categoria_var.get()
    estado = estado_var.get()
    lista = mostrar_lista(categoria, estado)
    lista_box.delete(0, "end")  # Borra el contenido anterior
    for idx, elemento in enumerate(lista, start=1):
        lista_box.insert("end", f"{idx}. {elemento}")

# Función para manejar el cambio de categoría
def cambiar_categoria(event):
    actualizar_lista()
    # Actualizar el menú desplegable de estado según la categoría seleccionada
    categoria = categoria_var.get()
    if categoria:
        estado_menu['values'] = list(lista_contenido[categoria].keys())
        estado_var.set(estado_menu['values'][0] if estado_menu['values'] else '')  # Establecer el primer estado como seleccionado si hay estados disponibles

# Crear una ventana principal
ventana = tk.Tk()
ventana.title("Organizador de Lista de Contenido")

# Aplicar un estilo moderno
style = ttk.Style()
style.theme_use("clam")

# Crear elementos de la interfaz
etiqueta_categoria = tk.Label(ventana, text="Categoría:")
categoria_var = tk.StringVar()
categoria_var.set("Peliculas")  # Valor predeterminado
categoria_menu = ttk.Combobox(ventana, textvariable=categoria_var, values=("Peliculas", "Series", "Anime"))
categoria_menu['state'] = 'readonly'  # Hacer el menú desplegable de categoría de solo lectura
etiqueta_estado = tk.Label(ventana, text="Estado:")
estado_var = tk.StringVar()
estado_menu = ttk.Combobox(ventana, textvariable=estado_var, values=[])
estado_menu['state'] = 'readonly'  # Hacer el menú desplegable de estado de solo lectura
etiqueta_elemento = tk.Label(ventana, text="Nombre del Elemento:")
entrada_elemento = tk.Entry(ventana)
boton_agregar = tk.Button(ventana, text="Agregar Elemento", command=agregar_elemento)
boton_borrar = tk.Button(ventana, text="Borrar Elemento", command=borrar_elemento)
lista_box = tk.Listbox(ventana, height=10, width=40)

# Colocar elementos en la ventana
etiqueta_categoria.grid(row=0, column=0, padx=10, pady=5)
categoria_menu.grid(row=0, column=1, padx=10, pady=5)
etiqueta_estado.grid(row=1, column=0, padx=10, pady=5)
estado_menu.grid(row=1, column=1, padx=10, pady=5)
etiqueta_elemento.grid(row=2, column=0, padx=10, pady=5)
entrada_elemento.grid(row=2, column=1, padx=10, pady=5)
boton_agregar.grid(row=3, column=0, padx=10, pady=10)
boton_borrar.grid(row=3, column=1, padx=10, pady=10)
lista_box.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Vincular el evento de cambio de categoría a la función
categoria_menu.bind("<<ComboboxSelected>>", cambiar_categoria)

# Vincular el evento de cambio de estado a la función de actualización
estado_menu.bind("<<ComboboxSelected>>", actualizar_lista)

# Cargar la lista de contenido
lista_contenido = cargar_lista()
actualizar_lista()

# Actualizar el menú desplegable de estado con los valores iniciales
estado_menu['values'] = list(lista_contenido[categoria_var.get()].keys())
estado_var.set(estado_menu['values'][0] if estado_menu['values'] else '')  # Establecer el primer estado como seleccionado si hay estados disponibles

# Iniciar el bucle principal
ventana.mainloop()






