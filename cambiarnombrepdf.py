# -*- coding: utf-8 -*-
"""cambiarnombrePDF.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1A6N2AsHXqwmRd1XVzYUNq7ZWg4BDyEzQ
"""

from google.colab import files
import zipfile
import os

# Permitir subir archivo ZIP
uploaded = files.upload()

# Extraer el nombre del archivo ZIP
zip_file_name = next(iter(uploaded))

# Crear una carpeta para los archivos extraídos
extracted_folder = '/content/extracted_pdfs'
os.makedirs(extracted_folder, exist_ok=True)

# Extraer el contenido del archivo ZIP
with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
    zip_ref.extractall(extracted_folder)

print(f"Archivos extraídos a {extracted_folder}")

!pip install PyMuPDF

import fitz  # PyMuPDF

# Función para extraer el DNI de un PDF
def extract_dni_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    dni = None

    # Leer cada página del PDF
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text = page.get_text()

        # Buscar el DNI (suponiendo que el DNI tiene un formato estándar como "DNI: 12345678")
        # Ajusta la búsqueda si el formato es diferente
        import re
        match = re.search(r'\bDNI[:\s]*([\d]+)\b', text)

        if match:
            dni = match.group(1)
            break  # Si encontramos el DNI, salimos del loop

    return dni

# Crear la carpeta RENOMBRADOS
renamed_folder = '/content/RENOMBRADOS'
os.makedirs(renamed_folder, exist_ok=True)

# Función para renombrar los PDFs con el DNI
def rename_pdfs_with_dni(extracted_folder, renamed_folder):
    for pdf_file in os.listdir(extracted_folder):
        pdf_path = os.path.join(extracted_folder, pdf_file)

        # Asegurarse de que es un archivo PDF
        if pdf_file.lower().endswith('.pdf'):
            dni = extract_dni_from_pdf(pdf_path)

            if dni:
                # Nuevo nombre del archivo (usamos el DNI)
                new_pdf_name = f"{dni}.pdf"
                new_pdf_path = os.path.join(renamed_folder, new_pdf_name)

                # Renombrar el archivo
                os.rename(pdf_path, new_pdf_path)
                print(f"Renombrado: {pdf_file} -> {new_pdf_name}")
            else:
                print(f"DNI no encontrado en el archivo: {pdf_file}")

# Llamar a la función para renombrar y mover los archivos
rename_pdfs_with_dni(extracted_folder, renamed_folder)

import shutil

# Comprimir la carpeta RENOMBRADOS en un archivo ZIP
shutil.make_archive('/content/RENOMBRADOS_compressed', 'zip', renamed_folder)

# Permitir la descarga del archivo comprimido
files.download('/content/RENOMBRADOS_compressed.zip')