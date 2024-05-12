import templates
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from owlready2 import *

def ontology_retriever(texto_pregunta):

    local_model = "llama3:8b"
    embeddings = OpenAIEmbeddings()

    chat = ChatOllama(model=local_model, base_url="http://127.0.0.1:11434")

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

            relevant_info += "Subclasses of the field: \n"

            for y in x.subclasses():
                relevant_info += y.label[0] + "\n"
        
        relevant_info += "\n\n"

    return relevant_info