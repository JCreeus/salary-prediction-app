# Diccionario de traduccion de paises
traduccion_paises = {
    "United States of America": "Estados Unidos",
    "United Kingdom of Great Britain and Northern Ireland": "Reino Unido",
    "Germany": "Alemania",
    "Canada": "Canadá",
    "Brazil": "Brasil",
    "Spain": "España",
    "France": "Francia",
    "India": "India",
    "Italy": "Italia",
    "Australia": "Australia",
    "Netherlands": "Países Bajos",
    "Poland": "Polonia",
    "Sweden": "Suecia",
    "Switzerland": "Suiza"
}

# Orden logico para la UI (importante para que no salga alfabetico)
orden_estudios_logico = [
    "Estudios menores (ej. bootcamps)",
    "Grado Universitario",
    "Máster",
    "Doctorado / Postgrado"
]

def limpiar_pais(pais):
    # Si esta en el diccionario devuelve la traduccion, si no, devuelve el original
    return traduccion_paises.get(pais, pais)

def normalizar_roles(rol):
    rol = str(rol).lower()
    
    # Datos e IA
    if 'machine learning' in rol or 'ai engineer' in rol: return 'Ingeniero de IA / Machine Learning'
    if 'data scientist' in rol: return 'Científico de Datos'
    if 'data engineer' in rol: return 'Ingeniero de Datos'
    if 'data analyst' in rol or 'business analyst' in rol: return 'Analista de Datos'
    
    # Web
    if 'back-end' in rol or 'backend' in rol: return 'Desarrollador Backend'
    if 'front-end' in rol or 'frontend' in rol: return 'Desarrollador Frontend'
    if 'full-stack' in rol or 'full stack' in rol: return 'Desarrollador Full Stack'
    
    # Infra
    if 'devops' in rol or 'sre' in rol or 'cloud' in rol: return 'DevOps / Cloud Engineer'
    if 'system admin' in rol or 'administrator' in rol: return 'SysAdmin / Sistemas'
    
    # Movil
    if 'mobile' in rol or 'android' in rol or 'ios' in rol: return 'Desarrollador Móvil'
    
    # Management
    if 'manager' in rol or 'lead' in rol or 'executive' in rol: return 'Engineering Manager / CTO'
    
    # Otros
    if 'game' in rol: return 'Desarrollador Videojuegos'
    if 'security' in rol: return 'Ciberseguridad'
    if 'qa' in rol or 'test' in rol: return 'QA / Tester'
    
    return 'Otro'

def parse_education(x):
    if 'Bachelor' in x: return 'Grado Universitario'
    if 'Master' in x: return 'Máster'
    if 'Professional' in x or 'doctoral' in x: return 'Doctorado / Postgrado'
    return 'Estudios menores (ej. bootcamps)'

def parse_experience(x):
    if x == 'More than 50 years': return 50
    if x == 'Less than 1 year': return 0.5
    try:
        return float(x)
    except:
        return 0