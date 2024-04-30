import time
import csv
import json
import settings
from datetime import datetime
from tools.jira_json_ground_truth import get_keys_for_query
from colorama import Fore

#Langchain
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import SystemMessage
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder, PromptTemplate


inicio = time.time()
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

ruta_preguntas = 'benchmark/ES_preguntas_train_V2.csv'
ruta_resultados = f'benchmark/resultados/out_benchmark_{current_time}.csv'
ruta_ontologia = 'JIRA_JQL_ontologia.ttl'
ruta_json = 'json/json_recibido_de_jira.json'
local_model = "llama3:8b"

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

        template_json = json.load(open('es_en.json', encoding='utf-8'))

        chat = ChatOllama(model=local_model, base_url="http://127.0.0.1:11434")

        prompt = PromptTemplate(
            template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are a JQL assistant for question-answering tasks. 
            Use the following ontology to answer the questions, which contains information about JIRA issues and how to generate JQL queries. You only have to return the JQL query for it to run verbatim, do not return any additional comments. So, for example, for the question "Que incidencias estan abiertas?" you should return "status = Abierto".
            <|eot_id|><|start_header_id|>user<|end_header_id|>
            Context: {context} 
            Question: {question} 
            Answer: <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
            input_variables=["question", "document"],
        )

        doc = open(ruta_ontologia, 'r').read()
        question = texto_pregunta
        chain = prompt | chat | StrOutputParser()
        gen = chain.invoke({"context": doc, "question": question})
        print(gen)
        
        time.sleep(.2)
        incidencias_obtenidas = []
        with open(ruta_json, 'r', encoding='utf-8') as json_file:
            json_respuesta = json.load(json_file)

            acierto = False
            if 'errorMessages' not in json_respuesta:
                incidencias_obtenidas = [issue['key'] for issue in json_respuesta['issues']]
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

                json_file.close()

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
            writer.writerow([id_pregunta, acierto, texto_pregunta, incidencias_esperadas, incidencias_obtenidas, jql_esperado, settings.llm_query])
            file_resultados.close()
        
        cont_preguntas += 1

tiempo_total = time.time() - inicio

print(f"Numero de preguntas incorrectas: {cont_fallos}. Preguntas incorrectas: {fallos}")
# Se imprime la precision conseguida
if cont_preguntas != 0:
    print(f"Accuracy: {1 - (cont_fallos / cont_preguntas)}")
print("Tiempo total: ", tiempo_total)