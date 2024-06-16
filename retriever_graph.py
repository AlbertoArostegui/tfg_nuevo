import templates
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import rdflib
from SPARQLWrapper import SPARQLWrapper, JSON, RDF


def graph_retriever(texto_pregunta):

    local_model = "gpt-3.5-turbo"

    #chat = ChatOllama(model=local_model, base_url="http://127.0.0.1:11434")
    chat = ChatOpenAI(model=local_model)

    prompt = PromptTemplate(
        template = templates.template_retrieve_graph_nodes,
        input_variables = ["question"],
    )

    question = texto_pregunta
    chain = prompt | chat | StrOutputParser()
    relevant_fields = chain.invoke({"question": question})

    relevant_fields = relevant_fields.split(", ")
    print(relevant_fields)
    relevant_info = ""

    sparql_endpoint = "http://localhost:7200/repositories/JIRA"

    sparql = SPARQLWrapper(sparql_endpoint)

    for field in relevant_fields:
        sparql_query = """
        PREFIX jira: <http://vocab.lksnext.com/jira/>
        DESCRIBE jira:{0}
        """.format(field)
        
        # Set the query and the return format
        sparql.setQuery(sparql_query)
        sparql.setReturnFormat(RDF)

        try:
            # Execute the query and get the results
            results = sparql.query().convert()
            g2 = rdflib.Graph()
            g2.parse(data=results)

            relevant_info = ""
        # Process and print the results
            for subj, pred, obj in g2:
                relevant_info += "s: {0}, p: {1}, o: {2} \n".format(subj, pred, obj)
                print(relevant_info)
        except:
            print('exception')

    return relevant_info
