import os
import shutil
from PyPDF2 import PdfReader, PdfWriter
from utils.tools import log_message
from GUI.messageBoxGui import message_box_gui

def extract_and_create_folders(directory):
    """
    Extrae las primeras dos páginas de todos los archivos PDF en el directorio especificado, 
    crea una carpeta para cada archivo PDF, y guarda un nuevo PDF llamado 'SOL.pdf' con 
    las páginas extraídas en la respectiva carpeta. Además, mueve el archivo PDF original 
    a su nueva carpeta.
    """
    # Verificar si el directorio existe
    if not os.path.isdir(directory):
        log_message(f"Error: El directorio '{directory}' no existe.")
        return

    # Filtrar solo archivos PDF en el directorio
    pdf_files = [f for f in os.listdir(directory) if f.lower().endswith('.pdf')]

    if not pdf_files:
        log_message("No se encontraron archivos PDF en el directorio proporcionado.")
        return
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(directory, pdf_file)
        folder_name = os.path.splitext(pdf_file)[0]
        folder_path = os.path.join(directory, folder_name)

        try:
            # Crear la carpeta si no existe
            os.makedirs(folder_path, exist_ok=True)
            
            # Leer el archivo PDF y preparar para extraer las primeras 2 páginas
            reader = PdfReader(pdf_path)
            writer = PdfWriter()

            # Extraer y agregar las primeras 2 páginas al nuevo PDF
            writer.add_page(reader.pages[0])
            if len(reader.pages) > 1:
                writer.add_page(reader.pages[1])

            # Guardar el nuevo PDF con el nombre 'SOL.pdf'
            new_pdf_path = os.path.join(folder_path, 'SOL.pdf')
            with open(new_pdf_path, 'wb') as new_pdf_file:
                writer.write(new_pdf_file)
            
            log_message(f"Se extrajeron las 2 primeras páginas de '{pdf_file}' y se guardaron en '{new_pdf_path}'.")

            # Mover el archivo PDF original a la nueva carpeta
            shutil.move(pdf_path, os.path.join(folder_path, pdf_file))
            log_message(f"El archivo original '{pdf_file}' se movió a '{folder_path}'.")
        
        except Exception as e:
            message_box_gui("Error", "Error al crear carpeta y extraer solicitud en '{pdf_file}': {e}", "Cerrar")
    
    log_message(f"Se crearon {len(pdf_files)} carpetas.")
