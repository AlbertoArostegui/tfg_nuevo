import templates
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from owlready2 import *

def ontology_retriever(texto_pregunta):

    local_model = "gpt-3.5-turbo"

    #chat = ChatOllama(model=local_model, base_url="http://127.0.0.1:11434")
    chat = ChatOpenAI(model=local_model)

    prompt = PromptTemplate(
        template = templates.template_retrieve_ontology_fields,
        input_variables = ["question"],
    )

    question = texto_pregunta
    chain = prompt | chat | StrOutputParser()
    relevant_fields = chain.invoke({"question": question})

    relevant_fields = relevant_fields.strip(" ").split(',')    

    onto_path.append("documents/")
    ontology = get_ontology("prueba.rdf")
    ontology.load()
    relevant_info = ""
    print(relevant_fields)

    for field in relevant_fields:
        field = field.strip(" ")
        for x in ontology.search(label = field):
            relevant_info += "Label: " + x.label[0] + "\n"
            try:
                relevant_info += "Comment: " + x.comment[0] + "\n"
            except IndexError:
                relevant_info += "Comment: None\n"

            try:
                relevant_info += "Supports operators: " + ", ".join([y.label[0] for y in x.supports]) + "\n"
            except:
                print("supports peta")

            relevant_info += "Subclasses of the field: \n"

            for y in x.subclasses():
                try:
                    relevant_info += y.label[0] + "\n"
                except IndexError:
                    pass
        
        relevant_info += "\n\n"
    
    return relevant_info