# Gerenciador de Atividades

Trabalho da disciplina de **Fundamentos de Sistemas de Informação** do curso de **Sistemas de Informação da UEA**. O objetivo é desenvolver um gerenciador de atividades com Python, Flask e SQLite, permitindo organizar tarefas e acompanhar seus responsáveis e prazos.

## Equipe

- Guilherme Amaral
- Erick Coutinho
- Katriny Monteiro

As responsabilidades de cada integrante serão registradas no [cronograma do projeto](https://docs.google.com/spreadsheets/d/1ogO2FRa288dpRAqjsJit0C6fy4Ri6QZU0cL5cyOwxBU/edit?gid=2003380003#gid=2003380003). A entrega está prevista para **12/10/2026**.

## Funcionalidades previstas

- Cadastro e visualização de contatos.
- Cadastro de tarefas com título, descrição, prazo, prioridade e contato responsável.
- Visualização das tarefas com seus respectivos responsáveis.
- Status **a fazer**, **fazendo**, **concluída** e **atrasada**, com cores diferentes.
- Exclusão de tarefas.

## Tecnologias

- Python e Flask para a aplicação web.
- HTML e CSS para as páginas.
- SQLite para armazenar contatos e tarefas.

## Como executar

Depois que o código da aplicação for adicionado ao repositório, instale as dependências e inicie o Flask na pasta do projeto:

```bash
python -m pip install -r requirements.txt
python app.py
```

Abra no navegador o endereço exibido no terminal, normalmente `http://127.0.0.1:5000`. As páginas HTML devem ser abertas pelo Flask, pois contêm comandos de template que o navegador sozinho não processa.

## Andamento

O projeto está em desenvolvimento. As atividades, os responsáveis e as datas estão no cronograma. Cada contribuição relevante será registrada em um commit no GitHub.

## Licença

Distribuído sob a [licença MIT](LICENSE).
