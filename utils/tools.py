from datetime import datetime
from PIL import Image
import csv

def log_message(message):
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}")

def write_new_line(filename, line):
    """
    Agrega una línea al archivo CSV especificado por 'filename'. Crea el archivo si no existe.
    """
    with open(filename, "a", newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';')
        csv_writer.writerow(line)