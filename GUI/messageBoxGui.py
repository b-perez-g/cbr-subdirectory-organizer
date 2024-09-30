import tkinter as tk
from utils.tools import log_message

def message_box_gui(title, message, button, show_continue_option=False):
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

    continue_result = tk.BooleanVar(value=False)
    
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

    # Frame para contener los botones horizontalmente
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)


    def on_continue_button():
        root.destroy()
        continue_result.set(True)
    
    if show_continue_option:
        btn_continue = tk.Button(button_frame, text="Continuar", command=on_continue_button)
        btn_continue.pack(side=tk.LEFT, padx=10)
        
    # Función y botón para cerrar la ventana
    def on_press_button():
        root.destroy()

    btn = tk.Button(button_frame, text=button, command=on_press_button)
    btn.pack(side=tk.LEFT, padx=10)
    

    # Asociar el evento Enter al botón actualmente enfocado
    def on_enter(event):
        focused_widget = root.focus_get()
        if focused_widget == btn:
            on_press_button()
        elif show_continue_option and focused_widget == btn_continue:
            on_continue_button()
    
    root.bind('<Return>', on_enter)

    # Foco inicial en el primer botón
    btn.focus_set()

    def force_focus():
        root.focus_force()
        if show_continue_option:
            btn_continue.focus_set()
        else:
            btn.focus_set()

    root.after(100, force_focus)

    # Iniciar la aplicación
    root.mainloop()

    return continue_result.get()
