import os
from datetime import datetime
from pdf2image import convert_from_path
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from utils.tools import log_message, write_new_line

def manual_input_gui(pdf_path, submission_number, CBR):
    """
    Abre una interfaz gráfica para permitir al usuario ingresar manualmente un número de proceso asociado con un archivo PDF.
    Basado en esta entrada, la carpeta que contiene el PDF se renombrará siguiendo un formato específico.

    :param pdf_path: Ruta al archivo PDF que se va a procesar.
    :param submission_number: Número de entrega para formar parte del nuevo nombre del directorio.
    :param CBR: Nombre del CBR para formar parte del nuevo nombre del directorio.
    """
    try:
        log_message(f"Mostrando GUI para ingresar número de proceso manualmente para {pdf_path}")

        root_dir = os.path.dirname(os.path.dirname(pdf_path))
        pdf_dir = os.path.dirname(pdf_path)
        old_dir_name = os.path.basename(pdf_dir)
        
        
        # Configuración de la ventana
        root = tk.Tk()
        root.title(f"Renombrar subdirectorio: {old_dir_name}")
        root.state('zoomed')
        root.attributes('-topmost', True)
        root.lift()
        root.focus_force()
        root.attributes('-topmost', False)

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Crear marcos para contenido e imagen
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=1)

        image_frame = tk.Frame(main_frame)
        image_frame.grid(row=0, column=0, pady=10, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        image_canvas = tk.Canvas(image_frame, width=int(screen_width * 0.75), height=int(screen_height * 0.9))
        image_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        image_scrollbar = ttk.Scrollbar(image_frame, orient=tk.VERTICAL, command=image_canvas.yview)
        image_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        image_canvas.configure(yscrollcommand=image_scrollbar.set)
        image_canvas.bind('<Configure>', lambda e: image_canvas.configure(scrollregion=image_canvas.bbox("all")))
        image_container = tk.Frame(image_canvas)
        image_canvas.create_window((0, 0), window=image_container, anchor="n")

        # Cargar y mostrar imágenes del PDF
        images = convert_from_path(pdf_path, dpi=72)
        for img in images:
            img_width = int(screen_width * 0.75)
            img_height = int(img_width * (img.height / img.width))
            img = img.resize((img_width, img_height), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            img_label = tk.Label(image_container, image=img_tk)
            img_label.image = img_tk
            img_label.pack()
            separator = ttk.Separator(image_container, orient='horizontal')
            separator.pack(fill='x', pady=5)
    
        # Crear frame para controles de entrada
        control_frame = tk.Frame(main_frame)
        control_frame.grid(row=0, column=1, padx=20, pady=20, sticky="n")

        # Configurar label para mensajes de error
        error_label = tk.Label(control_frame, text="", fg="red")
        error_label.grid(row=0, column=0, padx=10, pady=10)

        # Campo de entrada para número de proceso
        entry_label = tk.Label(control_frame, text="Ingrese el número de proceso:", anchor="w")
        entry_label.grid(row=1, column=0, padx=10, pady=10)
        entry_field = tk.Entry(control_frame, width=30)
        entry_field.grid(row=2, column=0, padx=10, pady=10)
        entry_field.focus_set()

        # Función para guardar el número de proceso
        def guardar_numero(event=None):
            process_number = entry_field.get().strip().replace(" ", "")
            if not process_number:
                error_label.config(text="El campo no puede estar vacío. Ingrese un valor.")
                return
            new_dir_name = f"{submission_number}_{CBR}_{process_number}"
            new_dir_path = os.path.join(os.path.dirname(pdf_dir), new_dir_name)

            suffix_counter = 1
            while os.path.exists(new_dir_path):
                new_dir_name = f"REP{suffix_counter}_{submission_number}_{CBR}_{process_number}"
                new_dir_path = os.path.join(os.path.dirname(pdf_dir), new_dir_name)
                suffix_counter += 1

            os.rename(pdf_dir, new_dir_path)
            write_new_line(f"{root_dir}/control de cambios.csv", [old_dir_name, new_dir_name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
            log_message(f"Carpeta renombrada a: {new_dir_name}")
            root.destroy()

        save_button = tk.Button(control_frame, text="Guardar", command=guardar_numero)
        save_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        # Función para renombrar sin número
        def guardar_sin_numero():
            new_dir_name = f"{submission_number}_{CBR}_SN1"
            new_dir_path = os.path.join(os.path.dirname(pdf_dir), new_dir_name)

            suffix_counter = 1
            while os.path.exists(new_dir_path):
                new_dir_name = f"{submission_number}_{CBR}_SN{suffix_counter}"
                new_dir_path = os.path.join(os.path.dirname(pdf_dir), new_dir_name)
                suffix_counter += 1

            os.rename(pdf_dir, new_dir_path)
            write_new_line(f"{root_dir}/control de cambios.csv", [old_dir_name, new_dir_name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
            log_message(f"Carpeta renombrada a: {new_dir_name}")
            root.destroy()

        na_button = tk.Button(control_frame, text="Sin Número", command=guardar_sin_numero)
        na_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        # Función para finalizar proceso
        def terminar_proceso():
            log_message("Finalizando el proceso por el usuario.")
            root.destroy()
            os._exit(0)

        terminate_button = tk.Button(control_frame, text="Terminar", command=terminar_proceso)
        terminate_button.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

        # Asociar tecla Enter al campo de entrada
        root.bind('<Return>', guardar_numero)

        # Añadir y vincular función de scroll con la rueda del mouse
        def _on_mouse_wheel(event):
            image_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        image_canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

        root.mainloop()

    except Exception as e:
        log_message(f"Error en la GUI para entrada manual: {e}")