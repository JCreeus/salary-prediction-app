import streamlit as st
import pickle
import numpy as np
import matplotlib.pyplot as plt
from utils import mostrar_nombre_pais, mostrar_nombre_estudios, mostrar_nombre_rol

# --- CARGAR MODELO ---
def load_model():
    try:
        with open('models/predictorModel.pkl', 'rb') as file:
            data = pickle.load(file)
        return data
    except FileNotFoundError:
        st.error("⚠️ Error: No encuentro el archivo .pkl")
        return None

data = load_model()

if data:
    regressor = data["model"]
    le_country = data["le_country"]
    le_education = data["le_education"]
    le_devtype = data["le_devtype"]

    # --- INTERFAZ ---
    st.title("Predicción de Salario IT")
    st.write("Calcula cuánto deberías cobrar y compáralo con otros países.")

    paises = [str(x) for x in le_country.classes_]
    # Definimos el orden lógico manualmente, ya que el modelo ordena alfabéticamente
    educacion = [
        "Less than a Bachelors",
        "Bachelor’s degree",
        "Master’s degree",
        "Post grad"
    ]
    roles = [str(x) for x in le_devtype.classes_]

    col1, col2 = st.columns(2)

    with col1:
        # País y estudios
        country = st.selectbox("🌍 Tu País", paises, format_func=mostrar_nombre_pais)
        education = st.selectbox("🎓 Estudios", educacion, format_func=mostrar_nombre_estudios)

    with col2:
        # Puesto y experiencia
        dev_type = st.selectbox("💻 Puesto", roles, format_func=mostrar_nombre_rol)
        experience = st.slider("⏳ Años de Experiencia", 0, 20, 3)

    ok = st.button("Calcular Salario", type="primary")

    if ok:
        # 1. Calculamos TU salario
        X_user = np.array([[
            le_country.transform([country])[0],
            le_education.transform([education])[0],
            experience,
            le_devtype.transform([dev_type])[0]
        ]])
        salary_user = regressor.predict(X_user)[0]

        st.subheader(f"💵 Tu Salario Estimado: ${salary_user:,.0f}")

        # 2. COMPARATIVA INTERNACIONAL
        st.write("---")
        st.write("### ✈️ ¿Cuánto ganarías en otros países con tu perfil?")

        # Países para comparar
        paises_comparar = [
            country,
            "United States of America",
            "Germany", 
            "United Kingdom of Great Britain and Northern Ireland"
        ]
        
        # Filtramos para no repetir si el usuario ya eligió uno de estos
        paises_comparar = list(set(paises_comparar)) 

        nombres_grafico = []
        salarios_grafico = []
        colores = []

        for p in paises_comparar:
            # Preparamos los datos cambiando SOLO el país
            try:
                # Transformamos el nombre del país al número que entiende el modelo
                pais_encoded = le_country.transform([p])[0]
                
                # Creamos la fila de datos
                X_temp = np.array([[
                    pais_encoded,
                    le_education.transform([education])[0],
                    experience,
                    le_devtype.transform([dev_type])[0]
                ]])
                
                pred = regressor.predict(X_temp)[0]
                
                # Guardamos datos para el gráfico
                nombre_bonito = mostrar_nombre_pais(p)
                if p == "United Kingdom of Great Britain and Northern Ireland":
                    nombre_bonito = "Reino Unido"
                
                nombres_grafico.append(nombre_bonito)
                salarios_grafico.append(pred)
                
                # Si es el país del usuario, lo pintamos verde. Si no, gris.
                if p == country:
                    colores.append('#2ecc71') # Verde
                else:
                    colores.append('#95a5a6') # Gris
            except:
                continue

        # 3. PINTAR EL GRÁFICO
        fig, ax = plt.subplots(figsize=(8, 5))
        
        # Ordenamos de mayor a menor salario
        listas_unidas = sorted(zip(salarios_grafico, nombres_grafico, colores), reverse=True)
        salarios_ordenados, nombres_ordenados, colores_ordenados = zip(*listas_unidas)

        barras = ax.bar(nombres_ordenados, salarios_ordenados, color=colores_ordenados)
        
        ax.set_ylabel('Salario Anual ($)')
        ax.set_title('Comparativa Internacional (Mismo Puesto y Experiencia)')
        
        # Poner los números encima de las barras
        for bar in barras:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval + 1000, f"${yval:,.0f}", ha='center', va='bottom', fontsize=10)

        st.pyplot(fig)