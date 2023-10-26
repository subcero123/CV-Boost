from flask import Flask, request, render_template, jsonify
import openai
from PyPDF2 import PdfReader
import config
import os
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate



app = Flask(__name__)

# Clave de la API de OpenAI
openai.api_key = ""

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
    curriculum  = obtener_texto_cv(cv)
    
    for seccion, contenido in curriculum.items():
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
        # Verifica si se ha enviado un archivo llamado 'cv_file'
        if 'cv_file' in request.files:
            cv_file = request.files['cv_file']
            cv = obtener_texto_cv(cv_file)
            response_data = obtener_sugerencias_para_secciones(cv)

            # Puedes acceder a los atributos del archivo, por ejemplo, su nombre y contenido
            cv_filename = cv_file.filename
            cv_content = cv_file.read()

            # Aquí puedes realizar las operaciones necesarias con el contenido del archivo

            return jsonify(response_data)
        else:
            return jsonify({"error": "No se envió ningún archivo con el nombre 'cv_file' en la solicitud."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
