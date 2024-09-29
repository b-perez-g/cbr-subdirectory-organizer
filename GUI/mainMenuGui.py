import tkinter as tk
from GUI.onlyAddNamesGui import only_add_names_gui
from GUI.renameSubdirectoriesGui import rename_subdirectories_gui

def main_menu_gui():
    """
    Inicializa la GUI del menú principal y maneja las selecciones del usuario
    
    :return: tupla con la opción seleccionada, directorio, número de envío y CBR.
    """
    
    selected_option = None
    directory = None
    submission_number = None
    cbr = None
    
    root = tk.Tk()
    root.title("Menú")

    # Función para opcion de renombrar subdirectorios
    def rename_folders():
        nonlocal selected_option
        nonlocal directory
        nonlocal submission_number
        nonlocal cbr
        
        root.destroy()
        inputs = rename_subdirectories_gui()
        directory = inputs[0]
        submission_number = inputs[1]
        cbr = inputs[2]
        
        if directory:
            selected_option = "rename subdirectories"

    # Función para opcion de agregar directorios
    def add_directories():
        nonlocal selected_option
        nonlocal directory
        root.destroy()
        directory = only_add_names_gui()
        if directory:
            selected_option = "only add names"

    # Configuración de la ventana
    window_width = 400
    window_height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int((screen_height - window_height) / 2)
    position_left = int((screen_width - window_width) / 2)
    root.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")

    # Creación del marco y botones
    frame = tk.Frame(root)
    frame.pack(expand=True)

    rename_button = tk.Button(
        frame,
        text="Renombrar subdirectorios",
        command=rename_folders
    )
    rename_button.pack(pady=10)

    add_directories_button = tk.Button(
        frame,
        text='Solo crear "Control de Cambios.csv"',
        command=add_directories,
        wraplength=300
    )
    add_directories_button.pack(pady=10)

    # Configuracion del foco
    def force_focus():
        root.focus_force()
        rename_button.focus_set()

    root.after(100, force_focus)

    # Manejo del evento de la tecla Enter
    def on_enter_key(event):
        widget_with_focus = root.focus_get()
        if widget_with_focus == rename_button:
            rename_folders()
        elif widget_with_focus == add_directories_button:
            add_directories()

    root.bind('<Return>', on_enter_key)
    root.mainloop()
    
    return selected_option, directory, submission_number, cbr
