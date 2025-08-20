import pandas as pd
import os

# Ruta del archivo
excel_file = "tasas/tasas.xlsx"

# Carpeta de salida para los CSV
output_folder = "tasas"
os.makedirs(output_folder, exist_ok=True)

# Lee todas las pestañas, saltando las primeras 11 filas
sheets = pd.read_excel(excel_file, sheet_name=None, skiprows=11)

for sheet_name, df in sheets.items():
    safe_name = sheet_name.replace(" ", "_").replace("/", "-")
    csv_file = os.path.join(output_folder, f"{safe_name}.csv")
    df.to_csv(csv_file, index=False, encoding="utf-8")
    print(f"Guardado: {csv_file}")

