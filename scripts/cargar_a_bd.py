import os
import csv
import pyodbc

# Ruta a la carpeta de archivos procesados
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROCESSED_DIR = os.path.join(BASE_DIR, "processed")

# Conexión a SQL Server (Windows Authentication)
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=MATEO;'
    'DATABASE=BioNet;'
    'Trusted_Connection=yes;'
)

cursor = conn.cursor()

# Procesar archivos CSV
for archivo in os.listdir(PROCESSED_DIR):
    if archivo.endswith(".csv"):
        ruta = os.path.join(PROCESSED_DIR, archivo)
        with open(ruta, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    # Evitar duplicados
                    cursor.execute("""
                        IF NOT EXISTS (
                            SELECT 1 FROM resultados_examenes 
                            WHERE paciente_id = ? AND tipo_examen = ? AND fecha_examen = ?
                        )
                        INSERT INTO resultados_examenes 
                        (laboratorio_id, paciente_id, tipo_examen, resultado, fecha_examen)
                        VALUES (?, ?, ?, ?, ?)
                    """,
                        row["paciente_id"], row["tipo_examen"], row["fecha_examen"],
                        row["laboratorio_id"], row["paciente_id"], row["tipo_examen"], row["resultado"], row["fecha_examen"]
                    )
                except Exception as e:
                    print(f"❌ Error insertando fila: {e}")

# Confirmar y cerrar conexión
conn.commit()
cursor.close()
conn.close()
print("✅ Datos insertados correctamente en la base de datos.")
