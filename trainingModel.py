import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
import pickle
import os
import utils

print("Iniciando pipeline de entrenamiento...")

def cargar_y_limpiar(ruta_csv, año):
    """Carga y estandariza los nombres de columnas entre diferentes años de encuestas."""
    try:
        df = pd.read_csv(ruta_csv)
        print(f" -> Dataset {año} cargado: {len(df)} registros")
    except FileNotFoundError:
        print(f"Error: Archivo no encontrado en {ruta_csv}")
        return None

    # Mapeo para unificar nomenclaturas de Stack Overflow (2023-2025)
    mapa_cols = {
        "ConvertedCompYearly": "Salary",
        "EdLevel": "EdLevel",
        "Country": "Country",
        "DevType": "DevType",
        "YearsCodePro": "Experience", 
        "LanguageHaveWorkedWith": "Languages"
    }
    
    cols_existentes = [c for c in mapa_cols.keys() if c in df.columns]
    df = df[cols_existentes].rename(columns=mapa_cols)
    
    # Lógica de respaldo para la columna Experience si YearsCodePro no existe
    # Jerarquía de selección basada en la correlación con el salario:
    # 1. YearsCodePro (Target ideal): Años programando profesionalmente. Máxima precisión.
    # 2. WorkExp (Fallback 1): Experiencia laboral general. Puede incluir roles no técnicos, menor precisión.
    # 3. YearsCode (Fallback 2): Tiempo total programando (incluye universidad y hobbies). 
    if "Experience" not in df.columns:
        if "WorkExp" in df.columns:
            df["Experience"] = df["WorkExp"]
        elif "YearsCode" in df.columns:
             df["Experience"] = df["YearsCode"]
    
    return df

# --- Carga de Datos ---
datasets = []
archivos = [
    ("data/survey_results_public_2023.csv", 2023),
    ("data/survey_results_public_2024.csv", 2024),
    ("data/survey_results_public_2025.csv", 2025)
]

for ruta, anio in archivos:
    df_temp = cargar_y_limpiar(ruta, anio)
    if df_temp is not None:
        datasets.append(df_temp)

if not datasets:
    print("No se han podido cargar los datos.")
    exit()

df = pd.concat(datasets, ignore_index=True)
print(f"Total registros brutos: {len(df)}")

# Eliminación de filas con valores nulos en features críticas
df = df.dropna(subset=["Salary", "DevType", "Country", "Experience"])

# --- Preprocesamiento y Limpieza ---
# Normalización de roles y filtrado de categorías no relevantes (ej. 'Otro', 'Estudiante')
df['DevType'] = df['DevType'].apply(utils.normalizar_roles)
df = df[df['DevType'] != 'Otro']

# Extracción de estadísticas de tecnologías (Top 5 por rol) para el sistema de recomendación
print("Generando estadísticas de stack tecnológico...")
tech_stats = {}
lista_roles = df['DevType'].unique()

for rol in lista_roles:
    df_rol = df[df['DevType'] == rol]
    # Tokenización y conteo de lenguajes
    all_langs = ";".join(df_rol['Languages'].dropna().astype(str))
    lista_langs = [x.strip() for x in all_langs.split(';')]
    from collections import Counter
    conteo = Counter(lista_langs)
    tech_stats[rol] = conteo.most_common(5)

# Filtro de representatividad: Eliminar países con muestra insuficiente (<650) para reducir varianza
counts = df['Country'].value_counts()
df = df[df['Country'].isin(counts[counts >= 650].index)]

# Traducción de países a Español antes del encoding
df['Country'] = df['Country'].apply(utils.limpiar_pais)

# Filtrado de outliers salariales y limpieza de datos geográficos
df = df[df["Salary"] <= 300000] 
df = df[df["Salary"] >= 10000] 
df = df[df["Country"] != "Other"]

# Parsing de variables numéricas y categóricas usando utilidades externas
df['Experience'] = df['Experience'].astype(str).apply(utils.parse_experience)
df['EdLevel'] = df['EdLevel'].apply(utils.parse_education)

# --- Feature Engineering ---
# Codificación de variables categóricas (Label Encoding)
le_country = LabelEncoder()
df['Country'] = le_country.fit_transform(df['Country'])

le_education = LabelEncoder()
df['EdLevel'] = le_education.fit_transform(df['EdLevel'])

le_devtype = LabelEncoder()
df['DevType'] = le_devtype.fit_transform(df['DevType'])

# Definición de matriz de características (X) y vector objetivo (y)
X = df[["Country", "EdLevel", "Experience", "DevType"]]
y = df["Salary"]

# --- Entrenamiento ---
print(f"Entrenando GradientBoostingRegressor con {len(df)} registros...")
# Hiperparámetros seleccionados para balancear bias/variance
regressor = GradientBoostingRegressor(n_estimators=300, max_depth=5, learning_rate=0.05, random_state=0)
regressor.fit(X, y)

# --- Serialización ---
output_path = 'models/predictorModel.pkl'
data = {
    "model": regressor,
    "le_country": le_country,
    "le_education": le_education,
    "le_devtype": le_devtype,
    "tech_stats": tech_stats
}

if not os.path.exists('models'):
    os.makedirs('models')

with open(output_path, 'wb') as file:
    pickle.dump(data, file)

print(f"Pipeline finalizado. Modelo exportado a: {output_path}")