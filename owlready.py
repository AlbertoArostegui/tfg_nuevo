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

operators = []
JQLOperator = ontology.search(iri = "http://vocab.lksnext.com/vocab.lksnext.com/JQLOperator")[0].subclasses()
for x in JQLOperator:
    operators.append(x)

print(operators)
#print([op.label for op in operators])

JQLField = ontology.search(iri = "http://vocab.lksnext.com/vocab.lksnext.com/JQLField")[0].subclasses()
for x in JQLField:
    #print(x.label[0])
    #print(x.supports)
    pass

print('\n\n')
Assignee = ontology.search(iri = "http://vocab.lksnext.comAssignee")[0]
print([x.label[0] for x in Assignee.supports])

print('\n\n')
Assignee = ontology.search(label = "Assignee")[0]
print([x.label[0] for x in Assignee.supports])
