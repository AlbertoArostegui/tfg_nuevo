import csv

r = csv.DictReader(open('benchmark/ES_preguntas_train_V2.csv', 'r', encoding='utf-8'))
for row in r:
    id = row['id_pregunta']
    texto_pregunta = row['texto_pregunta']
    jql_esperado = row['jql_esperado']

    print(f'{id} & {texto_pregunta} & {jql_esperado} \\\\')
    print('\hline')
    