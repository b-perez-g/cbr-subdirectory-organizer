import tkinter as tk
import os

def only_add_names_gui():
    """
    Crea una ventana que permite al usuario ingresar la ruta de un directorio
    y confirma si se procesarán los nombres de los subdirectorios.
    """
    
    root = tk.Tk()
    root.title("Confirmación")

    process = False
    directory = tk.StringVar(root, value="")

    # Funciones de acción para el procesamiento y para volver al menú principal
    def process_action():
        nonlocal process
        if os.path.isdir(directory.get()):
            root.destroy()
            process = True
        else:
            error_label.config(text="La ruta ingresada no es un directorio válido. Por favor, ingrese una ruta válida.")

    def back_action():
        from GUI.mainMenuGui import main_menu_gui
        directory.set("")
        root.destroy()
        main_menu_gui()

    # Configuración de la ventana
    window_width = 400
    window_height = 280
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int((screen_height - window_height) / 2)
    position_left = int((screen_width - window_width) / 2)
    root.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")

    # Interfaz de usuario para ingresar la ruta del directorio
    frame_input = tk.Frame(root)
    frame_input.pack(pady=10, padx=20, fill='x')

    label_prompt_text = "Ingrese la ruta del directorio principal:"
    lbl_prompt = tk.Label(frame_input, text=label_prompt_text, wraplength=360, anchor='w')
    lbl_prompt.pack(pady=(0, 5))

    entry_directory = tk.Entry(frame_input, textvariable=directory, width=50)
    entry_directory.pack()

    label_text = "Se registrarán los nombres de los subdirectorios a 'control de cambios.csv' sin ser renombrados antes."
    lbl_description = tk.Label(frame_input, text=label_text, wraplength=360, anchor='w')
    lbl_description.pack(pady=(10, 0))

    error_label = tk.Label(frame_input, text="", fg="red", wraplength=360, anchor='w')
    error_label.pack(pady=(10, 0))

    # Botones para procesar o cancelar
    frame_buttons = tk.Frame(root)
    frame_buttons.pack(pady=10, padx=10, anchor='e')

    btn_process = tk.Button(frame_buttons, text="Procesar", command=process_action)
    btn_process.pack(side='left', padx=5)

    btn_back = tk.Button(frame_buttons, text="Cancelar", command=back_action)
    btn_back.pack(side='right', padx=5)

    # Enfoque en el campo de entrada
    def force_focus():
        root.focus_force()
        entry_directory.focus_set()

    root.after(100, force_focus)

    # Vinculación de la tecla Enter para acciones de procesamiento
    def on_enter_in_entry(event):
        process_action()

    entry_directory.bind('<Return>', on_enter_in_entry)
    btn_process.bind('<Return>', lambda event: process_action())
    btn_back.bind('<Return>', lambda event: back_action())

    # Ejecutar la aplicación
    root.mainloop()
    
    return directory.get() if process else None
