import os
import time
import tkinter as tk

def updatable_message_box():
    """
    Crea una ventana de carga que permite actualizar el título y el mensaje.
    
    :return: (Tk, function) La ventana y una función para actualizar el mensaje.
    """
    # Configuración inicial de la ventana
    message = ""
    root = tk.Tk()
    root.title("Procesando")

    window_width = 500
    window_height = 150

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    position_top = int((screen_height - window_height) / 2)
    position_left = int((screen_width - window_width) / 2)

    root.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")
    root.configure(bg='white')

    # Crear un marco y una etiqueta para mostrar el mensaje
    frame = tk.Frame(root, bg='white')
    frame.pack(expand=True)

    lbl_loading = tk.Label(
        frame,
        text=message,
        bg='white',
        fg='black',
        font=('Arial', 10)
    )
    lbl_loading.pack(pady=20)

    #Actualiza el título y el mensaje de la ventana.
    def update_message(new_title, new_message):
        root.title(new_title)
        lbl_loading.config(text=new_message)

    return root, update_message
