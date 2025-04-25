import os
import shutil
import csv
import time

# Ruta base del proyecto (directorio raíz)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Rutas absolutas a las carpetas
INPUT_DIR = os.path.join(BASE_DIR, "input-labs")
PROCESSED_DIR = os.path.join(BASE_DIR, "processed")
ERROR_DIR = os.path.join(BASE_DIR, "error")

# Asegurarse de que las carpetas existen (crear si no existen)
for carpeta in [INPUT_DIR, PROCESSED_DIR, ERROR_DIR]:
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

# Cabecera esperada del archivo CSV
CABECERA_ESPERADA = ["id", "laboratorio_id", "paciente_id", "tipo_examen", "resultado", "fecha_examen"]

# Procesar archivos .csv en la carpeta de entrada
for archivo in os.listdir(INPUT_DIR):
    if archivo.endswith(".csv"):
        ruta_archivo = os.path.join(INPUT_DIR, archivo)
        destino = None

        try:
            with open(ruta_archivo, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                encabezado = next(reader, [])

                # Mostrar el encabezado detectado
                print(f"🧐 Encabezado detectado en {archivo}: {encabezado}")

                # Limpiar y normalizar encabezados
                encabezado_limpio = [col.strip().lower() for col in encabezado]
                esperado_limpio = [col.lower() for col in CABECERA_ESPERADA]

                if encabezado_limpio != esperado_limpio:
                    print(f"❌ {archivo} tiene encabezado incorrecto.")
                    destino = os.path.join(ERROR_DIR, archivo)
                else:
                    print(f"✅ {archivo} es válido.")
                    destino = os.path.join(PROCESSED_DIR, archivo)

        except Exception as e:
            print(f"⚠️ Error al procesar {archivo}: {e}")
            destino = os.path.join(ERROR_DIR, archivo)

        # Mover el archivo a su destino
        if destino:
            try:
                time.sleep(0.5)  # pequeña pausa
                shutil.move(ruta_archivo, destino)
                print(f"📦 {archivo} movido a {os.path.basename(destino)}")
            except Exception as move_error:
                print(f"❌ No se pudo mover {archivo}: {move_error}")
