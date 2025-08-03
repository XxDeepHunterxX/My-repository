
import json
import os
import datetime
from tkinter import ttk
import tkinter as tk
# elementos de entrada y salida
root = tk.Tk()
root.title("Task")
root.geometry("400x500")

label_task = tk.Label(root, text="Ingrese tarea:")
label_task.pack(pady=10)
entry_task = tk.Entry(root, width=50)
entry_task.pack(pady=10)

#task_listbox = tk.Listbox(root, width=40, height=15)
#task_listbox.pack(pady=5)

lista = ttk.Treeview(root, columns=("Tarea", "Fecha"), show="headings", height=15)
lista.heading("Tarea", text="Tarea")
lista.heading("Fecha", text="Fecha")    
lista.column("Tarea", width=220)
lista.column("Fecha", width=150)    
lista.pack(pady=5)

# funciones y metodos

def agregar_tarea():
    tarea = entry_task.get()
    if tarea:
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lista.insert("", "end", values=(tarea, fecha))
        entry_task.delete(0, tk.END)
    else:
        print("Por favor, ingrese una tarea.")

def eliminar_tarea():
    selecionar = lista.selection()
    if selecionar:
        lista.delete(selecionar[0])
    else:
        print("Por favor, seleccione una tarea para eliminar.")

def marcar_completada(event):
    selecionar = lista.selection()
    if selecionar:
        index = selecionar[0]
        tarea, fecha = lista.item(index, "values")
        if tarea.startswith("[in_process] "):
            # Si ya está en proceso marcar como hecha
            nuevo_texto = "[Done] " + tarea[len("[in_process] "):] 
        elif tarea.startswith("[Done] "):
           nuevo_texto = tarea[7:]
        #Si no tiene ninguna marca, marcar como en proceso
        else:
            nuevo_texto = "[in_process] " + tarea
                 
        lista.item(index, values=(nuevo_texto, fecha))

def guardar_tareas():
    tarea = [lista.item(item, "values") for item in lista.get_children()]
    with open("task.json", "w") as f:
        json.dump(tarea, f)

def cargar_tareas():
    if os.path.exists("task.json"):
        with open("task.json", "r") as f:
            tareas = json.load(f)
            for tarea, fecha in tareas:
                lista.insert("", "end", values=(tarea, fecha))

def modificar_tarea():
    seleccionar = lista.selection()
    if seleccionar:
        item = seleccionar[0]
        tarea, fecha = lista.item(item, "values")

        # Ventana emergente para editar tareas

        ventana_editar = tk.Toplevel(root)
        ventana_editar.title("Editar Tarea")            
        ventana_editar.geometry("300x150") 

        entry_editar = tk.Entry(ventana_editar, width=50)
        entry_editar.insert(0, tarea)
        entry_editar.pack(pady=10)

        label_fecha = tk.Label(ventana_editar, text=f"Fecha: {fecha}")
        label_fecha.pack(pady=5)

        def guardar_cambios():
            nuevo_texto = entry_editar.get()
            if nuevo_texto:
                lista.item(item, values=(nuevo_texto, fecha))
                ventana_editar.destroy()

        btn_guardar = tk.Button(ventana_editar, text="Guardar tareas", command= guardar_cambios)
        btn_guardar.pack(padx=5)
    else:
        print("Por favor, seleccione una tarea para modificar.")

# Elementos que activan tareas
frame = tk.Frame(root)
frame.pack(pady=5)

btn_agregar = tk.Button(frame, text="Agregar tarea", command= agregar_tarea)
btn_agregar.pack(side="left", padx=5)

btn_eliminar = tk.Button(frame, text="Eliminar tarea", command= eliminar_tarea)
btn_eliminar.pack(side="left", padx=5)

btn_modificar = tk.Button(frame, text="Modificar tarea", command= modificar_tarea)
btn_modificar.pack(side="left", padx=5)

lista.bind('<Double-1>', marcar_completada)

root.protocol("WM_DELETE_WINDOW", lambda: (guardar_tareas(), root.destroy()))
cargar_tareas()
root.mainloop()