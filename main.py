import os
import csv
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

# Definindo a variável de ambiente
os.environ['FLASK_DEBUG'] = 'True'

# Configurando o modo de depuração com base na variável de ambiente
app.debug = os.environ.get('FLASK_DEBUG') == 'True'

@app.route('/')
def ola():
    return render_template('index.html')


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


@app.route('/glossario')
def glossario():

    glossario_de_termos = []

    with open(
            'bd_glossario.csv',
            newline='', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo, delimiter=';')
        for l in reader:
            glossario_de_termos.append(l)

    return render_template('glossario.html',
                           glossario=glossario_de_termos)


@app.route('/novo_termo')
def novo_termo():
    return render_template('adicionar_termo.html')


@app.route('/criar_termo', methods=['POST', ])
def criar_termo():
    termo = request.form['termo']
    definicao = request.form['definicao']

    with open(
            'bd_glossario.csv', 'a',
            newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo, delimiter=';')
        writer.writerow([termo, definicao])

    return redirect(url_for('glossario'))


@app.route('/excluir_termo/<int:termo_id>', methods=['POST'])
def excluir_termo(termo_id):

    with open('bd_glossario.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        linhas = list(reader)

    # Encontrar e excluir o termo com base no ID
    for i, linha in enumerate(linhas):
        if i == termo_id:
            del linhas[i]
            break

    # Salvar as alterações de volta no arquivo
    with open('bd_glossario.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(linhas)

    return redirect(url_for('glossario'))

# @app.route('/pesquisar_termo/<int:termo_id>')
# def pesquisar_termo(termo_id):
#
#     with open('bd_glossario.csv', 'r', newline='') as file:
#         reader = csv.reader(file)
#         linhas = list(reader)
#
#     # Encontrar e excluir o termo com base no ID
#     for i, linha in enumerate(linhas):
#         if i == termo_id:
#             del linhas[i]
#             break

@app.route('/tarefa.html')
def form_cadastro_tarefa():
    return render_template('/tarefa.html')


@app.route('/processar_tarefa', methods=['POST'])
def processar_tarefa():
    if request.method == 'POST':
        # Obtém os dados do formulário
        titulo_tarefa = request.form.get('titulo_tarefa')
        palavras_tarefa= request.form.get('palavras_tarefa')

        # Caminho para o arquivo CSV
        cadastro_tarefa = 'bd_glossario.csv'

        # Verifica se o arquivo já existe
        arquivo_existe = os.path.exists(cadastro_tarefa)

        # Abre o arquivo CSV em modo de escrita
        with open(cadastro_tarefa, 'a', newline='') as csvfile:
            # Cria um objeto de gravação CSV
            csv_writer = csv.writer(csvfile)

            # Se o arquivo não existir, escreve o cabeçalho
            if not arquivo_existe:
                csv_writer.writerow(['titulo_tarefa', 'variaveis_tarefa'])

            # Escreve os dados no arquivo CSV
            csv_writer.writerow([titulo_receita, ingredientes_receita])

        return render_template('form_cadastro_tarefa.html', mensagem='Cadastro de tarefa realizado com sucesso!')


@app.route('/excluir_tarefa/<int:id>', methods=['POST'])
def excluir_tarefa(id):
    # Caminho para o arquivo CSV
    cadastro_tarefas_excluir = 'cadastro_tarefas.csv'

    # Lê todas as receitas do arquivo CSV tem que fazer
    with open(cadastro_tarefas_excluir, 'r', newline='') as csvfile_tarefas:
        csv_reader = csv.reader(csvfile_tarefas)
        receitas = list(csv_reader)

    # Remove a receita com o ID correspondente
    if 0 < id <= len(tarefas):
        del tarefas[id - 1]

    # Escreve as receitas de volta no arquivo CSV
    with open(cadastro_tarefas_excluir, 'w', newline='') as csvfile:
        csv_writer_excluir = csv.writer(csvfile)
        csv_writer_excluir.writerows(tarefas)

    return redirect(url_for('listar_tarefas'))



if __name__ == "__main__":
    app.run()