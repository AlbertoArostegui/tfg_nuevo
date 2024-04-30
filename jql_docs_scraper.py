import requests
from bs4 import BeautifulSoup, NavigableString

with open('documents/JQL_docs.txt', 'w', encoding='utf-8') as file:
    def retrieve_documentation(url):
        res = requests.get(url)
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')

        tables = soup.find_all('div', {'class': 'pm-table-wrapper'}) # Todas las tablas que describen el uso de cada campo/funcion/operador JQL
        for table in tables:
            rows = table.tbody.find_all('tr')
            try:
                syntax = rows[0].td.find_all('code')[-1].text
            except:
                syntax = rows[0].td.text
            for row in rows[1:]:
                if 'Examples' in row.text:
                    examples = row.td.text
                    break
            
            file.write(f'{syntax}: {examples}\n\n')

    def retrieve_documentation_operators(url):
        res = requests.get(url)
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')

        operators = soup.find_all('h2')
        operators = [operator.text for operator in operators]
        operators.remove('Jira Service Management Support')
        operators.remove('Additional Help')
    
        examples = soup.find_all('p', string='Examples')
        examples_texts = []
        for example in examples:
            next_h2 = example.find_next('h2')
            examples_text = ''
            for sibling in example.find_all_next():
                if sibling == next_h2:
                    break
                elif sibling.name == 'code':
                    if sibling.text != '1\n':
                        examples_text += f'\n{sibling.text}'
            examples_texts.append(examples_text)
        
        for entry_idx in range(len(operators)):
            string = f'{operators[entry_idx]}: {examples_texts[entry_idx]}\n\n'
            file.write(string)
    retrieve_documentation('https://support.atlassian.com/jira-software-cloud/docs/advanced-search-reference-jql-fields/')
    retrieve_documentation('https://support.atlassian.com/jira-software-cloud/docs/advanced-search-reference-jql-functions/')
    retrieve_documentation_operators('https://support.atlassian.com/jira-service-management-cloud/docs/jql-operators/')
    file.close()