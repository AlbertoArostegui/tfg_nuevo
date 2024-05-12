from owlready2 import *

onto_path.append("documents/")
ontology = get_ontology("prueba.rdf")
ontology.load()

for x in ontology.search(label = "assignee"):
    print(x.label[0])
    print(x.comment[0])

assignee = ontology.search(label = "Assignee")[0].subclasses()
for x in assignee:
    print(x.label)

statuses = ontology.search(label = "Status")[0].subclasses()
for x in statuses:
    print(x.label[0])