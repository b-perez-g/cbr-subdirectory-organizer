import os
from utils.extractAndCreateFolders import extract_and_create_folders
from utils.tools import log_message, write_new_line
from GUI.manualInputGui import manual_input_gui
from GUI.mainMenuGui import main_menu_gui
from GUI.updatableMessageBox import updatable_message_box
from GUI.messageBoxGui import message_box_gui
import time 

def process_pdfs_in_directory(directory):
    """
    Recorre un directorio buscando archivos llamados 'sol.pdf', y por cada uno, intenta procesarlo con una interfaz de entrada manual.
    """
    
    try:
        log_message(f"Iniciando procesamiento de PDFs en el directorio {directory}.")
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower() == 'sol.pdf':
                    pdf_path = os.path.join(root, file)
                    try:
                        manual_input_gui(pdf_path, submission_number, CBR)
                    except Exception as e:
                        log_message(f"Error procesando el PDF {pdf_path}: {e}")
    except Exception as e:
        message_box_gui("Error", f"Error al procesar el directorio {directory}: {e}", "Cerrar")


if __name__ == "__main__":
    try:
        # Seleccionar un proceso y obtener entradas del usuario desde el menú principal
        inputs = main_menu_gui()
        print(inputs)
        option = inputs[0]

        
        if option:
            directory = inputs[1].strip()
            
            # Ejecutar script para mover pdfs sueltos a carpetas y extraer solicitud
            extract_and_create_folders(directory)
            
            # Crear archivo de control de cambios
            if not os.path.exists(f"{directory}/control de cambios.csv"):
                write_new_line(f"{directory}/control de cambios.csv", ["Nombre anterior", "Nombre nuevo", "Fecha"])
            
            # Proceso para solo añadir nombres de las carpetas al archivo de control de cambios
            if option=="only add names":
                loading_window, update_loading_message = updatable_message_box()
                
                subdirectories = []
                for root, dirs, _ in os.walk(directory):
                    subdirectories.extend(dirs)
                    
                for index, subdirectory in enumerate(subdirectories):
                    update_loading_message(
                        f"Procesando subdirectorio {index + 1} de {len(subdirectories)}..",
                        f'({index + 1}/{len(subdirectories)}) \n\n Añadiendo "{subdirectory}" \n al archivo "Control de cambios.csv"' 
                    )
                    
                    write_new_line(f"{directory}/control de cambios.csv", ["", subdirectory, ""])
                    loading_window.update()
                        
                time.sleep(0.2)
                loading_window.destroy()
                
                message_box_gui("Proceso finalizado", f"Se procesaron {len(subdirectories)} subdirectorios", "Salir")
                
            #Proceso para renombrar los  subdirectorios
            if option=="rename subdirectories":
                submission_number = inputs[2].strip()
                CBR = inputs[3].strip().upper()
                
                log_message("Comenzando el procesamiento de directorio.")
                process_pdfs_in_directory(directory)
                
                message_box_gui("Proceso finalizado", f"Terminaste de renombrar los subdirectorios", "Salir")
                
    except Exception as e:
        message_box_gui("Error", f"Ocurrio un error durante el proceso: {e}", "Cerrar")
            
            