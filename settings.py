#Archivo para guardar variables globales entre módulos. Se usa para guardar la query que el LLM usa para llamar a la funcion de JIRA.
def init():
    global llm_query
    llm_query = "placeholder"