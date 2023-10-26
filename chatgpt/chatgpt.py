#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
#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
import openai
import os

# Clave de la API de OpenAI
openai.api_key = "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"


# Función para obtener sugerencias de mejoras en una sección del CV
def obtener_sugerencias(texto):
    prompt = f"La siguiente sección proviene de mi CV, quiero que mejores la sección para que pueda aprovar un filtro ATS, adicionalmente enlista me de forma breve que mejoraste de este rubro:\n{texto}\n"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
          messages=[
        {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=256,
    )
    return response['choices'][0]['message']['content']

# Función para obtener sugerencias de mejora para secciones específicas del CV
def obtener_sugerencias_para_secciones(cv):
    sugerencias_por_seccion = {}
    
    for seccion, contenido in cv.items():
        if seccion in ["Educación", "Experiencia Laboral en Tecnología", "Habilidades Técnicas",
                      "Proyectos Personales o de Grupo", "Hackathons y Competencias Técnicas",
                      "Proyectos de Código Abierto"] and contenido.strip():
            sugerencias = obtener_sugerencias(contenido)
            sugerencias_por_seccion[seccion] = sugerencias
    
    return sugerencias_por_seccion

# Datos de ejemplo del CV
cv = {
    "Educación": "Soy estudiante de Ciencias de la Computación en la Universidad XYZ.",
    "Experiencia Laboral en Tecnología": "",
    "Habilidades Técnicas": "Tengo experiencia en Python, Java, Linux, bases de datos SQL y herramientas de desarrollo como Git.",
    "Proyectos Personales o de Grupo": "",
    "Hackathons y Competencias Técnicas": "Gané el primer lugar en el Hackathon ABC en 2022.",
    "Proyectos de Código Abierto": "",
}

# Llama a la función para obtener sugerencias para secciones específicas
sugerencias_por_seccion = obtener_sugerencias_para_secciones(cv)

# Imprime las sugerencias para cada sección no vacía
for seccion, sugerencias in sugerencias_por_seccion.items():
    print(f"Sugerencias para la sección '{seccion}':\n{sugerencias}\n")
