import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import pickle
import os

print("⏳ Cargando datos y entrenando Random Forest (Mejorado)...")

# CARGAR DATOS
try:
    df = pd.read_csv("data/survey_results_public.csv")
except FileNotFoundError:
    print("❌ ERROR: No encuentro el CSV.")
    exit()

# LIMPIEZA
try:
    df = df[["ConvertedCompYearly", "Country", "EdLevel", "WorkExp", "DevType"]]
except KeyError:
    df = df[["ConvertedCompYearly", "Country", "EdLevel", "YearsCode", "DevType"]]
    df = df.rename(columns={"YearsCode": "WorkExp"})

df = df.rename(columns={"ConvertedCompYearly": "Salary", "WorkExp": "Experience"})
df = df[df["Salary"].notnull()]
df = df.dropna()

# --- FILTRO DE CALIDAD POR PAÍS ---
# Contamos cuántos datos hay de cada país
conteo_paises = df['Country'].value_counts()

# Ponemos el límite en 150 datos por país, para quedarnos solo con países que tengan una muestra decente
limite_respuestas = 150 

# Creamos la lista de países aprobados
paises_validos = conteo_paises[conteo_paises >= limite_respuestas].index

# Creamos el nuevo DataFrame filtrado
df = df[df['Country'].isin(paises_validos)]

print(f"🌍 Países que pasaron el filtro (> {limite_respuestas} datos): {len(paises_validos)}")

# --- Limitar datos ---
# Solo gente que cobra entre 10k y 250k.
df = df[df["Salary"] <= 250000] 
df = df[df["Salary"] >= 10000] 
df = df[df["Country"] != "Other"]

# Funciones de limpieza
def clean_experience(x):
    if x ==  'More than 20 years': return 20
    if x == 'Less than 1 year': return 0.5
    return float(x)

def clean_education(x):
    if 'Bachelor’s degree' in x: return 'Bachelor’s degree'
    if 'Master’s degree' in x: return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x: return 'Post grad'
    return 'Less than a Bachelors'

df['Experience'] = df['Experience'].astype(str).apply(clean_experience)
df['EdLevel'] = df['EdLevel'].apply(clean_education)

# CODIFICAR
le_country = LabelEncoder()
df['Country'] = le_country.fit_transform(df['Country'])
le_education = LabelEncoder()
df['EdLevel'] = le_education.fit_transform(df['EdLevel'])
le_devtype = LabelEncoder()
df['DevType'] = le_devtype.fit_transform(df['DevType'])

# ENTRENAR EL MODELO
X = df[["Country", "EdLevel", "Experience", "DevType"]]
y = df["Salary"]

# --- CONFIGURACIÓN DEL RANDOM FOREST ---
# n_estimators=200: Usamos 200 árboles.
# max_depth=10: Evita que el modelo se memorice casos raros.
regressor = RandomForestRegressor(n_estimators=200, max_depth=8, min_samples_leaf=5, random_state=0)
regressor.fit(X, y)

# GUARDAR
data = {"model": regressor, "le_country": le_country, "le_education": le_education, "le_devtype": le_devtype}

if not os.path.exists('models'):
    os.makedirs('models')

with open('models/predictorModel.pkl', 'wb') as file:
    pickle.dump(data, file)

print("✅ ¡ÉXITO! Modelo suavizado y guardado.")