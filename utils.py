# Diccionario (traducciones) de toda la info de la página

traduccion_estudios = {
    "Less than a Bachelors": "Sin estudios universitarios",
    "Bachelor’s degree": "Grado Universitario",
    "Master’s degree": "Máster / Postgrado",
    "Post grad": "Doctorado"
}

traduccion_paises = {
    "Spain": "España",
    "United States of America": "Estados Unidos",
    "Germany": "Alemania",
    "United Kingdom of Great Britain and Northern Ireland": "Reino Unido",
    "Canada": "Canadá",
    "France": "Francia",
    "Brazil": "Brasil",
    "Italy": "Italia",
    "Netherlands": "Países Bajos",
    "Poland": "Polonia",
    "Sweden": "Suecia",
    "India": "India",
    "Australia": "Australia",
    "Other": "Otro país"
}

traduccion_roles = {
    "AI/ML engineer": "Ingeniero de IA / Machine Learning",
    "Academic researcher": "Investigador Académico",
    "Applied scientist": "Científico Aplicado",
    "Architect, software or solutions": "Arquitecto de Software / Soluciones",
    "Cloud infrastructure engineer": "Ingeniero Cloud / Infraestructura",
    "Cybersecurity or InfoSec professional": "Especialista en Ciberseguridad",
    "Data engineer": "Ingeniero de Datos",
    "Data or business analyst": "Analista de Datos / Negocio",
    "Data scientist": "Científico de Datos",
    "Database administrator or engineer": "Administrador de Bases de Datos",
    "DevOps engineer or professional": "Ingeniero DevOps",
    "Developer, AI apps or physical AI": "Desarrollador de Apps IA",
    "Developer, back-end": "Desarrollador Back-end",
    "Developer, desktop or enterprise applications": "Desarrollador de Escritorio / Empresarial",
    "Developer, embedded applications or devices": "Desarrollador de Sistemas Embebidos",
    "Developer, front-end": "Desarrollador Front-end",
    "Developer, full-stack": "Desarrollador Full-stack",
    "Developer, game or graphics": "Desarrollador de Videojuegos / Gráficos",
    "Developer, mobile": "Desarrollador Móvil (iOS/Android)",
    "Developer, QA or test": "QA / Tester / Control de Calidad",
    "Engineering manager": "Engineering Manager (Gerente de Ingeniería)",
    "Financial analyst or engineer": "Analista Financiero",
    "Founder, technology or otherwise": "Fundador / Emprendedor",
    "Investigador": "Investigador",
    "Other (please specify):": "Otro",
    "Product manager": "Product Manager",
    "Project manager": "Project Manager",
    "Retired": "Jubilado",
    "Senior executive (C-Suite, VP, etc.)": "Directivo Ejecutivo (CEO, CTO, VP...)",
    "Student": "Estudiante",
    "Support engineer or analyst": "Ingeniero de Soporte Técnico",
    "System administrator": "Administrador de Sistemas (SysAdmin)",
    "UX, Research Ops or UI design professional": "Diseñador UI/UX",
    
    # Estos estan repetidos pero pueden aparecer en el dataset con estas otras formas
    "Administrador de Sistemas": "Administrador de Sistemas (SysAdmin)",
    "Desarrollador Back-end": "Desarrollador Back-end",
    "Desarrollador Front-end": "Desarrollador Front-end",
    "Desarrollador Full-stack": "Desarrollador Full-stack",
    "Desarrollador Móvil (iOS/Android)": "Desarrollador Móvil (iOS/Android)",
    "Investigador": "Investigador"
}

def mostrar_nombre_pais(opcion_ingles):
    return traduccion_paises.get(opcion_ingles, opcion_ingles)

def mostrar_nombre_estudios(opcion_ingles):
    return traduccion_estudios.get(opcion_ingles, opcion_ingles)

def mostrar_nombre_rol(opcion_ingles):
    return traduccion_roles.get(opcion_ingles, opcion_ingles)