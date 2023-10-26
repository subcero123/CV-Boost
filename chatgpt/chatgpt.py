from flask import Flask, request, render_template, jsonify
import openai
from PyPDF2 import PdfReader
import config
import os
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate



app = Flask(__name__)

# Clave de la API de OpenAI
openai.api_key = "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"

def obtener_texto_cv(path):
    # Desglose del CV

    #Lectura del archivo pdf
    #reader = PdfReader("curriculumVitaeSistemas.pdf")
    reader = PdfReader(path)
    number_of_pages = len(reader.pages)

    # Inicializamos el texto acumulado como una cadena vacía
    text = ""

    for i in range(number_of_pages):
        #Acumulamos las paginas
        page = reader.pages[i]

        # Extraemos el texto de la página y lo agregamos al texto acumulado
        text += page.extract_text()


    os.environ['OPENAI_API_KEY'] = config.OPENAI_API_KEY
    print(os.environ['OPENAI_API_KEY'])


    template = '''
        Quiero que actues como un analista de datos experto en analizar curriculums sobre ``` {carrera} ```.
        El curriculum es el siguiente:
        ``` {curriculum} ```
        Ordena y clasifica la siguiente información en base a los siguientes rubros:
        Educación: Dado que eres estudiante o recién graduado, tu historial académico es fundamental. Enumera tu título actual o más reciente, la institución, las fechas de inicio y finalización, y cualquier distinción académica relevante.
        Experiencia Laboral en Tecnología: Incluye cualquier pasantía, empleo a tiempo parcial o proyectos relacionados con la informática. Es importante especificar las tecnologías utilizadas y las responsabilidades asumidas.
        Habilidades Técnicas: Destaca tus habilidades técnicas, como lenguajes de programación, sistemas operativos, bases de datos, herramientas de desarrollo y cualquier otra competencia relevante.
        Proyectos Personales o de Grupo: Menciona proyectos en los que hayas trabajado, ya sea de forma independiente o en equipo. Describe tu contribución, las tecnologías utilizadas y los resultados logrados.
        Hackathons y Competencias Técnicas: Si has participado en hackathons, competencias de programación o eventos similares, resalta tus logros y premios.
        Certificaciones Técnicas: Enumera cualquier certificación relacionada con la informática que hayas obtenido.
        Idiomas de Programación: Especifica los lenguajes de programación que dominas y tu nivel de experiencia en cada uno.
        Proyectos de Código Abierto: Si has contribuido a proyectos de código abierto, menciona tu participación y las contribuciones realizadas.
        Habilidades Comunicativas y de Trabajo en Equipo: En el campo de la tecnología, la capacidad para comunicar ideas técnicas y trabajar en equipo es valiosa. Destaca estas habilidades.
        Intereses y Publicaciones Técnicas: Si tienes interés en áreas específicas de la computación o has publicado trabajos técnicos, inclúyelos.
        Redes Sociales y Perfiles en Línea: Si tienes perfiles en LinkedIn, GitHub u otras plataformas relevantes, menciónalos para que los reclutadores puedan obtener más información sobre tu trabajo.
        Estructura con el siguiente formato: "Titulo del Rubro": "Contenido desglosado en puntos"
        Agrega comillas dobles a cada rubro y contenido.
        No omitas información.
        '''

    #Generamos un template para el chat
    prompt = PromptTemplate.from_template(template)

    #print(prompt.format(carrera='ingenieros en computación', curriculum=text))

    llms = ChatOpenAI( model='gpt-3.5-turbo', temperature=0.9, max_tokens=1000,)

    from langchain.chains import LLMChain

    chain = LLMChain(llm=llms, prompt=prompt, verbose=True)

    result = chain.run(carrera='ingenieros en computación', curriculum=text)

    #En result se encuentra el desglose del CV


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
    print(cv)
    for seccion, contenido in cv.items():
        print(seccion)
        if seccion in ["Educación", "Experiencia Laboral en Tecnología", "Habilidades Técnicas",
                    "Proyectos Personales o de Grupo", "Hackathons y Competencias Técnicas",
                    "Proyectos de Código Abierto"]:
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
    # try:
    # Verifica si se ha enviado un archivo llamado 'cv_file'
    """
    if 'cv_file' in request.files:
        cv_file = request.files['cv_file']
        cv = obtener_texto_cv(cv_file)
        response_data = obtener_sugerencias_para_secciones(cv)

        # Puedes acceder a los atributos del archivo, por ejemplo, su nombre y contenido
        cv_filename = cv_file.filename
        cv_content = cv_file.read()

        # Aquí puedes realizar las operaciones necesarias con el contenido del archivo
    """
    # Datos de ejemplo del CV
    cv = {
        "Educación": {
            "Título actual o más reciente": "Computer systems engineering",
            "Institución": "Benemérita Universidad Autónoma de Puebla",
            "Fecha de inicio": "August 2018",
            "Fecha de finalización": "January 2024"
        },
        "Experiencia Laboral en Tecnología": [
            {
                "Puesto": "Internship at EMFUTECH in Osaka, Japan",
                "Fechas": "April 2023 - July 2023",
                "Responsabilidades": [
                    "Implementation of teleoperation of vehicles at EMFUTECH",
                    "Designed a full WebApplication using tools like Flask, Python, React",
                    "Implemented steering mechanisms, enhancing control precision and maneuverability of an RC vehicle",
                    "Designed and implemented RTSP solutions for video surveillance systems"
                ],
                "Experiencia en Tecnologías": [
                    "Java: 4 years",
                    "GIT",
                    "Linux Operative Systems",
                    "C#: 1 year",
                    "MySQL: 4 years",
                    "PYTHON Machine Learning and Data Scientist",
                    "JavaScript/Typescript: 4 years",
                    "PHP: 2 years",
                    "HTML/CSS: 4 years"
                ]
            }
        ],
        "Habilidades Técnicas": [
            "Java",
            "GIT",
            "Linux Operative Systems",
            "C#",
            "MySQL",
            "PYTHON Machine Learning and Data Scientist",
            "JavaScript/Typescript",
            "PHP",
            "HTML/CSS"
        ],
        "Proyectos Personales o de Grupo": [
            {
                "Proyecto": "Implementation of teleoperation of vehicles at EMFUTECH (June 2023)",
                "Contribución": "Designed a full WebApplication using tools like Flask, Python, React",
                "Tecnologías utilizadas": "Flask, Python, React"
            },
            {
                "Proyecto": "Real-Time Vehicle Tracking Application (December 2020)",
                "Contribución": "Integrated Google Maps API to display accurate and interactive maps, allowing users to visualize vehicle locations and routes in real time."
            }
        ],
        "Hackathons y Competencias Técnicas": [
            "2018 Participation at the national robotics contest WER MEXICO 2018",
            "2023 Best Project for the Industry Award at EMFUTECH 2023"
        ],
        "Certificaciones Técnicas": [
            "English: TOEFL IBT 95 Points",
            "Japanese: JLPT N4 Level certification",
            "Spanish: Native"
        ],
        "Idiomas de Programación": [
            "Java: 4 years",
            "C#: 1 year",
            "MySQL: 4 years",
            "PYTHON Machine Learning and Data Scientist",
            "JavaScript/Typescript: 4 years",
            "PHP: 2 years",
            "HTML/CSS: 4 years"
        ],
        "Proyectos de Código Abierto": "No se menciona la participación en proyectos de código abierto.",
        "Habilidades Comunicativas y de Trabajo en Equipo": "No se mencionan habilidades comunicativas y de trabajo en equipo.",
        "Intereses y Publicaciones Técnicas": "No se mencionan intereses y publicaciones técnicas.",
        "Redes Sociales y Perfiles en Línea": {
            "LinkedIn": "No se menciona",
            "GitHub": "https://github.com/subcero123"
        }
    }
    sugerencias_por_seccion = obtener_sugerencias_para_secciones(cv)
    response_data = sugerencias_por_seccion
    print(sugerencias_por_seccion)
    return jsonify(response_data)
    # return jsonify({"error": "No se envió ningún archivo con el nombre 'cv_file' en la solicitud."})
if __name__ == "__main__":
    app.run(debug=True)

