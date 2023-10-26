from flask import Flask, request, render_template
import openai

app = Flask(__name__)

# Clave de la API de OpenAI
openai.api_key = "TU_CLAVE_DE_API_DE_OPENAI"

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



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/obtener_sugerencias', methods=['POST'])
def obtener_sugerencias_endpoint():
    try:
        # Datos de ejemplo del CV
        cv = {
            "Educación": "Soy estudiante de Ciencias de la Computación en la Universidad XYZ.",
            "Experiencia Laboral en Tecnología": "",
            "Habilidades Técnicas": "Tengo experiencia en Python, Java, Linux, bases de datos SQL y herramientas de desarrollo como Git.",
            "Proyectos Personales o de Grupo": "",
            "Hackathons y Competencias Técnicas": "Gané el primer lugar en el Hackathon ABC en 2022.",
            "Proyectos de Código Abierto": "",
        }
        sugerencias_por_seccion = obtener_sugerencias_para_secciones({"Educación": cv})
        return render_template('index.html', cv_sugerencias=sugerencias_por_seccion)
    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)