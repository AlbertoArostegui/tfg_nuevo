from owlready2 import *

onto_path.append("documents/")
ontology = get_ontology("prueba.rdf")
ontology.load()

for x in ontology.search(label = "supports"):
    print(x)