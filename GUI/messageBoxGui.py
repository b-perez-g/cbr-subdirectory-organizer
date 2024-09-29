import tkinter as tk
from utils.tools import log_message

def message_box_gui(title, message, button):
    """
    Crea una ventana de mensaje que muestra un título y un mensaje.

    :param title: Título de la ventana.
    :param message: Mensaje a mostrar en la ventana.
    :param button: Texto del botón para cerrar la ventana.
    """
    
    log_message(message)

    # Configuración de la ventana principal
    root = tk.Tk()
    root.title(title)

    window_width = 500
    window_height = 150
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int((screen_height - window_height) / 2)
    position_left = int((screen_width - window_width) / 2)
    root.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")

    # Creación de la etiqueta para mostrar el mensaje
    lbl_message = tk.Label(root, text=message, font=('Arial', 10))
    lbl_message.pack(pady=20)

    # Función y botón para cerrar la ventana
    def on_press_button():
        root.destroy()

    btn = tk.Button(root, text=button, command=on_press_button)
    btn.pack(pady=10)

    # Configuración de la interacción con el teclado
    root.bind('<Return>', lambda event: on_press_button())
    
    def force_focus():
        root.focus_force()
        btn.focus_set()

    root.after(100, force_focus)

    # Iniciar la aplicación
    root.mainloop()
