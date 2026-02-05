# Diccionario (traducciones) de toda la info de la página

traduccion_estudios = {
    "Less than a Bachelors": "Sin estudios universitarios",
    "Bachelor’s degree": "Grado Universitario (Carrera)",
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
    "Developer, back-end": "Desarrollador Back-end",
    "Developer, front-end": "Desarrollador Front-end",
    "Developer, full-stack": "Desarrollador Full-stack",
    "Developer, mobile": "Desarrollador Móvil (iOS/Android)",
    "Data scientist or machine learning specialist": "Data Scientist / IA Engineer",
    "Engineer, data": "Data Engineer",
    "DevOps specialist": "Ingeniero DevOps",
    "Engineering manager": "Engineering Manager",
    "Senior Executive (C-Suite, VP, etc.)": "Directivo (CTO, VP...)",
    "System administrator": "Administrador de Sistemas",
    "Project manager": "Project Manager",
    "Product manager": "Product Manager",
    "Academic researcher": "Investigador",
    "Educator": "Profesor / Educador"
}

def mostrar_nombre_pais(opcion_ingles):
    return traduccion_paises.get(opcion_ingles, opcion_ingles)

def mostrar_nombre_estudios(opcion_ingles):
    return traduccion_estudios.get(opcion_ingles, opcion_ingles)

def mostrar_nombre_rol(opcion_ingles):
    return traduccion_roles.get(opcion_ingles, opcion_ingles)