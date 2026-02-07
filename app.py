import streamlit as st
import pickle
import numpy as np
import matplotlib.pyplot as plt
import utils

st.set_page_config(page_title="Predicción Salarial IT", layout="centered")

def load_model():
    try:
        with open('models/predictorModel.pkl', 'rb') as file:
            data = pickle.load(file)
        return data
    except FileNotFoundError:
        st.error("Error: No se encuentra models/predictorModel.pkl")
        return None

data = load_model()

if not data:
    st.stop()

regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]
le_devtype = data["le_devtype"]
tech_stats = data["tech_stats"]

# Filtramos el orden logico de estudios definido en utils para que coincida con lo disponible en el modelo
estudios_disponibles = [e for e in utils.orden_estudios_logico if e in le_education.classes_]

# --- INTERFAZ ---
st.title("💸 Calculadora Salarial IT")
st.write("Estimación de valor de mercado y skills recomendadas.")
st.write("---")

st.subheader("Perfil")

c1, c2 = st.columns(2)

with c1:
    # Como entrenamos traduciendo, le_country.classes_ ya esta en español, asi que los mostramos tal cual
    paises = le_country.classes_
    pais_seleccionado = st.selectbox("🌍 País", paises)

    educacion_seleccionada = st.selectbox("🎓 Estudios", estudios_disponibles)

with c2:
    # Los roles tambien estan ya en español
    rol_seleccionado = st.selectbox("💻 Puesto / Rol", le_devtype.classes_)
    experiencia = st.slider("⏳ Años experiencia", 0, 20, 3)

st.write("")
calcular = st.button("Calcular Salario", type="primary", use_container_width=True)

if calcular:
    st.write("---")
    st.subheader("Análisis")
    
    # Vector base
    X_base = np.array([[
        le_country.transform([pais_seleccionado])[0],
        le_education.transform([educacion_seleccionada])[0],
        experiencia,
        le_devtype.transform([rol_seleccionado])[0]
    ]])

    # Proyección futura (correccion de picos)
    predicciones = []
    for i in range(10): 
        X_temp = X_base.copy()
        X_temp[0, 2] = experiencia + i
        pred = regressor.predict(X_temp)[0]
        predicciones.append(pred)

    salario_final = min(predicciones)
    
    salario_5_years = predicciones[5]
    if salario_5_years < salario_final: 
        salario_5_years = salario_final

    st.metric(label="Salario Anual Bruto Estimado", 
              value=f"${salario_final:,.0f}", 
              delta=f"Proyección 5 años: ${salario_5_years:,.0f}")
    
    st.info(f"Datos para **{rol_seleccionado}** en **{pais_seleccionado}**.")

    # --- GRÁFICOS ---
    # Tecnologías (Variables renombradas aquí)
    st.write("### 🛠️ Tecnologías más demandadas")
    top_techs = tech_stats.get(rol_seleccionado, [])
    
    if top_techs:
        tech_names, conteos = zip(*top_techs)
        fig_tech, ax_tech = plt.subplots(figsize=(8, 4))
        y_pos = np.arange(len(tech_names))
        
        ax_tech.barh(y_pos, conteos, align='center', color='#3498db')
        ax_tech.set_yticks(y_pos)
        ax_tech.set_yticklabels(tech_names)
        ax_tech.invert_yaxis()
        ax_tech.spines['top'].set_visible(False)
        ax_tech.spines['right'].set_visible(False)
        st.pyplot(fig_tech)
    else:
        st.warning("Sin datos suficientes de tecnologías.")

    st.write("---")
    
    # Comparativa Países
    st.write("### ✈️ Comparativa Internacional")
    
    # Lista manual de paises clave para comparar
    # Como ya estan traducidos en el modelo, aqui los ponemos en Español
    lista_paises = [pais_seleccionado, "Estados Unidos", "Alemania", "Reino Unido", "Canadá", "España"]
    # Filtramos solo los que existan en el modelo
    lista_paises = [p for p in list(set(lista_paises)) if p in le_country.classes_]

    nombres, salarios, colores = [], [], []

    for p in lista_paises:
        try:
            p_encoded = le_country.transform([p])[0]
            
            # Scan de estabilidad, variando la experiencia para evitar picos raros
            preds_pais = []
            for i in range(6):
                X_p = np.array([[p_encoded, le_education.transform([educacion_seleccionada])[0], experiencia + i, le_devtype.transform([rol_seleccionado])[0]]])
                preds_pais.append(regressor.predict(X_p)[0])
            
            val_pais = min(preds_pais)
            
            nombres.append(p)
            salarios.append(val_pais)
            colores.append('#2ecc71' if p == pais_seleccionado else '#95a5a6')
        except: continue
    
    fig_world, ax_world = plt.subplots(figsize=(8, 5))
    zipped = sorted(zip(salarios, nombres, colores), reverse=True)
    s_ord, n_ord, c_ord = zip(*zipped)
    
    barras = ax_world.bar(n_ord, s_ord, color=c_ord)
    ax_world.spines['top'].set_visible(False)
    ax_world.spines['right'].set_visible(False)
    ax_world.spines['left'].set_visible(False)
    ax_world.set_yticks([])
    
    for bar in barras:
        ax_world.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500, 
                      f"${bar.get_height()/1000:.0f}k", 
                      ha='center', va='bottom', fontweight='bold')
    
    st.pyplot(fig_world)