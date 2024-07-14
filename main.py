import tkinter as tk
from tkinter import messagebox
import pyperclip

def format_ticket(title, prefijo='RPA --', subticket_prefix='OLT BACKHAUL ---'):
    try:
        # Verificar si el título contiene la estructura esperada
        if 'ALARMA ACTIVA:' not in title or 'Puertas' not in title:
            raise ValueError("El formato del título de alarma no es válido")

        # Extracción de datos relevantes del título original
        parts = title.split(':')
        if len(parts) < 3:
            raise ValueError("El formato del título de alarma no es válido")

        olt_info = parts[1].strip().replace('OLT-', '')  # Corregir la duplicación de 'OLT-'
        puertas_info = parts[2].split('[', 1)[0].strip()

        if '[' in parts[2]:
            onts_info = '[' + parts[2].split('[', 1)[1]
        else:
            onts_info = ''

        # Construcción del nuevo título
        formatted_title = f"{prefijo} OLT-{olt_info} - Puertas -- {puertas_info} -- DOWN {onts_info}"

        # Construcción del subticket
        subticket = f"{subticket_prefix} {formatted_title}"

        return formatted_title, subticket
    except (IndexError, ValueError) as e:
        return f"Error: {str(e)}", "Error"

def generate_new_ticket():
    new_alarm = title_entry.get()
    formatted_title, subticket = format_ticket(new_alarm)
    ticket_result.set(formatted_title)
    subticket_result.set(subticket)

def copy_ticket():
    formatted_title = ticket_result.get()
    root.clipboard_clear()
    root.clipboard_append(formatted_title)
    messagebox.showinfo("Copiar", "Título del ticket copiado al portapapeles")

def copy_subticket():
    subticket_title = subticket_result.get()
    root.clipboard_clear()
    root.clipboard_append(subticket_title)
    messagebox.showinfo("Copiar", "Título del subticket copiado al portapapeles")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Generador de Tickets")

# Variables para almacenar los resultados
ticket_result = tk.StringVar()
subticket_result = tk.StringVar()

# Etiquetas y campos de entrada
tk.Label(root, text="Ingrese el nuevo título de alarma:").pack()
title_entry = tk.Entry(root, width=100)
title_entry.pack()

# Botón para generar el ticket
generate_button = tk.Button(root, text="Generar Título", command=generate_new_ticket)
generate_button.pack()

# Mostrar resultados
tk.Label(root, text="Título del ticket:").pack()
ticket_entry = tk.Entry(root, textvariable=ticket_result, width=100)
ticket_entry.pack()
tk.Button(root, text="Copiar Título del Ticket", command=copy_ticket).pack()

tk.Label(root, text="Título del subticket:").pack()
subticket_entry = tk.Entry(root, textvariable=subticket_result, width=100)
subticket_entry.pack()
tk.Button(root, text="Copiar Título del Subticket", command=copy_subticket).pack()

# Iniciar la aplicación
root.mainloop()
