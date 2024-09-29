import tkinter as tk
import os

def rename_subdirectories_gui():
    """
    Crea una ventana para ingresar los datos antes de comenzar a renombrar los subdirectorios. 
    Se ingresan el directorio, el número de entrega y el CBR.
    
    :return: (str, str, str) Si se procesa, devuelve el directorio, número de entrega y CBR; de lo contrario, None.
    """

    root = tk.Tk()
    root.title("Renombrar Subdirectorios")

    process = False
    
    # Variables de entrada
    directory = tk.StringVar()
    submission_number = tk.StringVar()
    CBR = tk.StringVar()

    # Función para procesar las entradas y validar
    def process_action():
        nonlocal process
        if not os.path.isdir(directory.get()):
            error_label.config(text="La ruta ingresada no es un directorio válido.")
            return

        try:
            submission_number_value = int(submission_number.get())
        except ValueError:
            error_label.config(text="El número de entrega debe ser un número entero.")
            return
        
        if not CBR.get().strip():
            error_label.config(text="El CBR no puede estar vacío.")
            return

        root.destroy() 
        process = True

    # Configuración de la ventana principal
    window_width = 400
    window_height = 280

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    position_top = int((screen_height - window_height) / 2)
    position_left = int((screen_width - window_width) / 2)

    root.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")

    # Interfaz para ingresar datos
    frame_input = tk.Frame(root)
    frame_input.pack(pady=10, padx=20, fill='x')

    tk.Label(frame_input, text="Ingrese la ruta del directorio:", anchor='w').pack(pady=(0, 5))
    entry_directory = tk.Entry(frame_input, textvariable=directory, width=50)
    entry_directory.pack()
    
    tk.Label(frame_input, text="Ingrese el CBR:", anchor='w').pack(pady=(10, 5))
    entry_cbr = tk.Entry(frame_input, textvariable=CBR, width=50)
    entry_cbr.pack()

    tk.Label(frame_input, text="Ingrese el número de entrega:", anchor='w').pack(pady=(10, 5))
    entry_submission_number = tk.Entry(frame_input, textvariable=submission_number, width=50)
    entry_submission_number.pack()

    error_label = tk.Label(frame_input, text="", fg="red", anchor='w')
    error_label.pack(pady=(10, 0))

    # Botón para procesar
    btn_process = tk.Button(root, text="Comenzar", command=process_action)
    btn_process.pack(pady=20)

    # Vincular la tecla Enter en el último campo y en el botón
    entry_directory.bind('<Return>', lambda event: entry_cbr.focus_set())
    entry_cbr.bind('<Return>', lambda event: entry_submission_number.focus_set())
    entry_submission_number.bind('<Return>', lambda event: process_action())
    btn_process.bind('<Return>', lambda event: process_action())

    # Hacer que el botón pueda ser activado con Enter
    btn_process.focus_force()

    # Forzar el foco en el campo de entrada
    def force_focus():
        root.focus_force()
        entry_directory.focus_set()

    root.after(100, force_focus)

    # Ejecutar la aplicación
    root.mainloop()
    if process:
        return directory.get(), submission_number.get(), CBR.get()
    else:
        return None, None, None
