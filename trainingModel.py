# Archivo: trainingModel.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import pickle
import os

print("⏳ Cargando datos y entrenando IA... espera.")

# 1. CARGAR DATOS
try:
    df = pd.read_csv("data/survey_results_public.csv")
except FileNotFoundError:
    print("❌ ERROR: No encuentro el CSV en 'data/survey_results_public.csv'.")
    exit()

# 2. LIMPIEZA
# --- CAMBIO IMPORTANTE AQUÍ ---
# Usamos 'WorkExp' en vez de 'YearsCodePro' porque es la que tiene tu archivo
try:
    df = df[["ConvertedCompYearly", "Country", "EdLevel", "WorkExp", "DevType"]]
except KeyError:
    # Si falla, intentamos buscar 'YearsCode' por si acaso
    print("⚠️ Aviso: No encontré 'WorkExp', probando con 'YearsCode'...")
    df = df[["ConvertedCompYearly", "Country", "EdLevel", "YearsCode", "DevType"]]
    df = df.rename(columns={"YearsCode": "WorkExp"})


# Renombramos para trabajar cómodo
df = df.rename(columns={"ConvertedCompYearly": "Salary", "WorkExp": "Experience"})

# Eliminamos nulos
df = df[df["Salary"].notnull()]
df = df.dropna()

def clean_experience(x):
    if x ==  'More than 30 years': return 30.0
    if x == 'Less than 1 year': return 0.5
    return float(x)

def clean_education(x):
    if 'Bachelor’s degree' in x: return 'Bachelor’s degree'
    if 'Master’s degree' in x: return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x: return 'Post grad'
    return 'Less than a Bachelors'

# Aplicamos limpieza
# Aseguramos que Experience sea string antes de limpiar por si acaso viene como numero mixto
df['Experience'] = df['Experience'].astype(str).apply(clean_experience)
df['EdLevel'] = df['EdLevel'].apply(clean_education)

# 3. CODIFICAR (TEXTO -> NÚMEROS)
le_country = LabelEncoder()
df['Country'] = le_country.fit_transform(df['Country'])

le_education = LabelEncoder()
df['EdLevel'] = le_education.fit_transform(df['EdLevel'])

le_devtype = LabelEncoder()
df['DevType'] = le_devtype.fit_transform(df['DevType'])

# 4. ENTRENAR EL MODELO
# Orden: [Country, EdLevel, Experience, DevType]
X = df[["Country", "EdLevel", "Experience", "DevType"]]
y = df["Salary"]

regressor = RandomForestRegressor(n_estimators=100, random_state=0)
regressor.fit(X, y)

# 5. GUARDAR EL CEREBRO (.pkl)
data = {
    "model": regressor,
    "le_country": le_country,
    "le_education": le_education,
    "le_devtype": le_devtype
}

if not os.path.exists('models'):
    os.makedirs('models')

with open('models/predictorModel.pkl', 'wb') as file:
    pickle.dump(data, file)

print("✅ ¡ÉXITO! Nuevo cerebro generado en 'models/predictorModel.pkl'")