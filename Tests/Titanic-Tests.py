import pandas as pd
import glob
import os

results = pd.read_csv("results.csv")

csv_files = glob.glob("submission_*.csv")

if not csv_files:
    print("No se encontraron archivos 'submission_*.csv' en la carpeta.")
    exit()

# Lista para guardar resultados
resultados = []

for file in csv_files:
    try:
        # Nombre del modelo = texto después de "submission_" y antes de ".csv"
        modelo = os.path.basename(file).replace("submission_", "").replace(".csv", "")

        pred = pd.read_csv(file)
        
        merged = pred[["PassengerId", "Survived"]].merge(results[["PassengerId", "Survived"]], on="PassengerId", suffixes=('_pred', '_res'))

        total = len(merged)
        aciertos = (merged[f"{"Survived"}_pred"] == merged[f"{"Survived"}_res"]).sum()
        porcentaje = aciertos / total

        resultados.append({"Modelo": modelo, "Aciertos": aciertos, "Total": total, "Accuracy": round(porcentaje, 5)})

    except Exception as e:
        print(f"Error procesando {file}: {e}")

df_resumen = pd.DataFrame(resultados).sort_values(by="Accuracy", ascending=False)
print(df_resumen.head())