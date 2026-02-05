import streamlit as st
import pickle
import numpy as np
from utils import mostrar_nombre_pais, mostrar_nombre_estudios, mostrar_nombre_rol

def load_model():
    try:
        with open('models/predictorModel.pkl', 'rb') as file:
            data = pickle.load(file)
        return data
    except FileNotFoundError:
        st.error("⚠️ Error: Ejecuta primero 'python generar_modelo.py'")
        return None

data = load_model()

if data:
    regressor = data["model"]
    le_country = data["le_country"]
    le_education = data["le_education"]
    le_devtype = data["le_devtype"]

    st.title("Predicción de Salario (IT)")
    st.write("### ¿Cuánto deberías cobrar?")
    st.write("Selecciona tus datos y la IA estimará tu salario anual.")

    # --- PREPARAR OPCIONES ---
    paises_ingles = [str(x) for x in le_country.classes_]
    educacion_ingles = [str(x) for x in le_education.classes_]
    roles_ingles = [str(x) for x in le_devtype.classes_]

    # --- INPUTS ---
    country = st.selectbox("🌍 País", paises_ingles, format_func=mostrar_nombre_pais)
    
    # NUEVO SELECTOR
    dev_type = st.selectbox("💻 Rol / Puesto", roles_ingles, format_func=mostrar_nombre_rol)
    
    education = st.selectbox("🎓 Nivel de Estudios", educacion_ingles, format_func=mostrar_nombre_estudios)
    
    experience = st.slider("⏳ Años de Experiencia Profesional", 0, 30, 3)

    ok = st.button("Calcular Salario")

    if ok:
        # Convertimos todo a números
        X_country = le_country.transform([country])
        X_education = le_education.transform([education])
        X_devtype = le_devtype.transform([dev_type])
        
        # OJO AL ORDEN: Tiene que ser igual que en trainingModel.py
        # [Country, EdLevel, Experience, DevType]
        # (Mira tu trainingModel.py, si pusiste df[['Country', 'EdLevel', 'Experience', 'DevType']])
        # Entonces el array debe ser:
        X = np.array([[X_country[0], X_education[0], experience, X_devtype[0]]])
        
        salary = regressor.predict(X)
        st.success(f"El salario estimado es: ${salary[0]:,.2f}")