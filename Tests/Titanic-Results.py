import pandas as pd
import re

def clean_name(s):
    """Limpia los nombres para hacerlos comparables entre archivos."""
    if pd.isna(s):
        return s
    s = str(s)

    # Reemplazar comillas dobles y simples por espacio
    s = s.replace('"', ' ').replace("“", " ").replace("”", " ").replace("'", " ")

    # Quitar paréntesis, guiones, corchetes y otros signos no relevantes
    s = re.sub(r"[\(\)\[\]\-_/\\]", " ", s)

    # Quitar puntos y comas (como 'Miss. Johanna,' → 'Miss Johanna')
    s = re.sub(r"[.,;:]", " ", s)

    # Eliminar múltiples espacios y espacios en extremos
    s = re.sub(r"\s+", " ", s).strip()

    # Pasar todo a minúsculas
    s = s.lower()

    return s

# Cargar los datasets
total = pd.read_excel("total.xls")
test = pd.read_csv("test.csv")

# Normalizar nombres de columnas a minúsculas
total.columns = total.columns.str.lower()
test.columns = test.columns.str.lower()

# Crear columnas limpias
total["name"] = total["name"].apply(clean_name)
test["name"] = test["name"].apply(clean_name)

# Hacer el merge usando 'name' como clave
resultados = test.merge(total[["name", "survived"]], on="name", how="left")

# Mantener solo las columnas relevantes
columnas_finales = ["passengerid", "survived"]

resultados = resultados[columnas_finales]
resultados = resultados.rename(columns={"passengerid": "PassengerId", "survived": "Survived"})

# Eliminar filas con ID repetidos (Mismo nombre)
resultados = resultados.drop_duplicates(subset=["PassengerId"], keep='last')

# Guardar el nuevo CSV
resultados.to_csv("results.csv", index=False)

print("Archivo 'results.csv' creado con las columnas:", resultados.columns.tolist())