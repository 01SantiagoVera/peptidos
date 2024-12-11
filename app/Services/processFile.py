import os


def process_file(uploaded_file):
    """Procesar un archivo subido para extraer secuencias."""
    try:
        # Verificar si el archivo tiene contenido
        if not uploaded_file:
            raise ValueError("No se proporcionó un archivo válido.")

        # Leer las secuencias desde el archivo
        sequences = []
        for line in uploaded_file:
            line = line.decode("utf-8").strip()  # Decodificar línea a texto y quitar espacios
            if line:  # Ignorar líneas vacías
                sequences.append(line)

        if not sequences:
            raise ValueError("El archivo está vacío o no contiene secuencias válidas.")

        return sequences
    except Exception as e:
        raise ValueError(f"Error al procesar el archivo: {str(e)}")
