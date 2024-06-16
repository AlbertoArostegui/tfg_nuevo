import time
import csv
import settings
import templates
import dotenv
from datetime import datetime
from tools.jira_json_retrieval import get_keys_for_query
from ontology_retriever import ontology_retriever
from colorama import Fore

#Langchain
#from langchain_community.chat_models import ChatOllama
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate


inicio = time.time()
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
dotenv.load_dotenv()

ruta_preguntas = 'benchmark/ES_preguntas_train_V2.csv'
ruta_resultados = f'benchmark/resultados/out_benchmark_ontology_{current_time}.csv'
ruta_ontologia = 'JIRA_JQL_ontologia.ttl'
ruta_json = 'json/ph.json'
local_model = "gpt-3.5-turbo"

cont_preguntas = 0
cont_fallos = 0
total_prompt_tokens = 0
total_completion_tokens = 0
tokens_total = 0
settings.init()

fallos = []

def sort_key(item):
    try:
        prefix, number = item.split('-')
        return (prefix, int(number))
    except:
        print("Error en sort_key")


with open(ruta_preguntas, 'r', encoding='utf-8') as file_preguntas:
    reader = csv.DictReader(file_preguntas)

    with open(ruta_resultados, 'w', newline='') as file_resultados:
        writer = csv.writer(file_resultados)

        columnas = ['id_pregunta', 'acierto', 'texto_pregunta', 'incidencias_esperadas', 'incidencias_obtenidas', 'jql_esperado', 'respuesta']
        writer.writerow(columnas)

        file_resultados.close()        
    
#####################################
##### Iteraciones del benchmark #####
#####################################

    for row in reader:

        id_pregunta = row['id_pregunta']
        texto_pregunta = row['texto_pregunta']
        incidencias_esperadas = row['incidencias_asignadas'].split(',')
        jql_esperado = row['jql_esperado']

        #chat = ChatOllama(model=local_model, base_url="http://127.0.0.1:11434")
        chat = ChatOpenAI(model=local_model)

        prompt = PromptTemplate(
            template = templates.template_ontology_fields,
            input_variables = ["question", "document"],
        )

        question = texto_pregunta
        doc = ontology_retriever(texto_pregunta)
        chain = prompt | chat | StrOutputParser()
        llm_generated = chain.invoke({"context": doc, "question": question})
        
        print(question)
        print(llm_generated)
        time.sleep(.2)
        incidencias_obtenidas = []


        acierto = False
        incidencias_obtenidas = get_keys_for_query(llm_generated)
        incidencias_esperadas = get_keys_for_query(jql_esperado)

        while None in incidencias_obtenidas:
            incidencias_obtenidas.remove(None)
        while '' in incidencias_obtenidas:
            incidencias_obtenidas.remove('')

        while '' in incidencias_esperadas:
            incidencias_esperadas.remove('')

        try:
            incidencias_obtenidas.sort(key=sort_key)
            incidencias_esperadas.sort(key=sort_key)
        except: 
            pass
            
        acierto = incidencias_esperadas == incidencias_obtenidas

        if not acierto:
            cont_fallos += 1
            fallos.append(id_pregunta)
        
        tokens_total += total_completion_tokens + total_prompt_tokens
        if acierto:
            progreso = f"\nPregunta {id_pregunta}: {texto_pregunta} ==> " + Fore.GREEN + str(acierto) + Fore.RESET 
        else:
            progreso = f"\nPregunta {id_pregunta}: {texto_pregunta} ==> " + Fore.RED + str(acierto) + Fore.RESET

        print(progreso)

        with open(ruta_resultados, 'a', newline='', encoding='utf-8') as file_resultados:
            writer = csv.writer(file_resultados)
            writer.writerow([id_pregunta, acierto, texto_pregunta, incidencias_esperadas, incidencias_obtenidas, jql_esperado, llm_generated])
            file_resultados.close()
        
        cont_preguntas += 1

tiempo_total = time.time() - inicio

print(f"Numero de preguntas incorrectas: {cont_fallos}. Preguntas incorrectas: {fallos}")
# Se imprime la precision conseguida
if cont_preguntas != 0:
    print(f"Accuracy: {1 - (cont_fallos / cont_preguntas)}")
print("Tiempo total: ", tiempo_total)