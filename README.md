# Gerenciador de Atividades

Aplicação web para organizar atividades, definir responsáveis e acompanhar prazos e prioridades. Desenvolvida como trabalho da disciplina de **Fundamentos de Sistemas de Informação**, do curso de **Sistemas de Informação da Universidade do Estado do Amazonas (UEA)**.

## Equipe

* Guilherme Amaral
* Erick Coutinho
* Katriny Monteiro

O planejamento e a divisão das atividades estão no [cronograma do projeto](https://docs.google.com/spreadsheets/d/1ogO2FRa288dpRAqjsJit0C6fy4Ri6QZU0cL5cyOwxBU/edit?gid=2003380003#gid=2003380003).

## Funcionalidades

* Cadastro e listagem de contatos com nome, e-mail e telefone.
* Criação de atividades com título, descrição, prazo, prioridade e responsável.
* Prioridades **Baixa**, **Média** e **Alta**.
* Status **A fazer**, **Fazendo**, **Concluída** e **Atrasada**.
* Conclusão, reabertura e exclusão de atividades.
* Atualização automática de atividades vencidas para o status **Atrasada** ao carregar a página inicial.
* Agrupamento em **Atrasadas**, **Hoje**, **Esta semana**, **Depois**, **Sem prazo** e **Concluídas**.
* Filtros com contadores e painel de progresso circular.
* Temas claro e escuro, com a preferência salva no navegador.
* Layout responsivo com estética neobrutalista, animações e suporte à preferência de movimento reduzido.

## Organização das atividades

As atividades são ordenadas dentro de cada grupo por prazo, prioridade e data de criação. O grupo **Esta semana** reúne os prazos de amanhã até os próximos sete dias, sem depender da semana do calendário.

As concluídas ficam em uma seção que pode ser expandida ou recolhida. Uma atividade atrasada continua disponível para conclusão; o atraso apenas indica que o prazo passou.

## Tecnologias

| Tecnologia | Uso |
| --- | --- |
| Python e Flask | Rotas e regras da aplicação |
| Flask-SQLAlchemy e SQLite | Modelos e armazenamento dos dados |
| Jinja2 e HTML | Estrutura das páginas |
| CSS | Layout, temas e responsividade |a
| JavaScript | Menus, animações e interações |
| Google Fonts e Font Awesome | Fontes e ícones |

## Como executar

É necessário ter **Python 3** e **Git** instalados.

### 1. Clonar o repositório

```bash
git clone https://github.com/by-amaral/gerenciador-atividades.git
cd gerenciador-atividades
```

### 2. Criar o ambiente e instalar as dependências

No **Windows, pelo PowerShell**:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

No **Linux ou macOS**:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

### 3. Iniciar a aplicação

No **Windows**:

```powershell
.\.venv\Scripts\python.exe app.py
```

No **Linux ou macOS**:

```bash
.venv/bin/python app.py
```

Acesse **http://127.0.0.1:5000** no navegador. Para encerrar o servidor, pressione `Ctrl + C` no terminal.

As páginas devem ser acessadas pelo servidor Flask. Abrir os arquivos HTML diretamente não executa os templates da aplicação.

## Como usar

1. Acesse **Novo contato** e cadastre as pessoas que poderão ser responsáveis pelas atividades.
2. Em **Nova atividade**, informe o título e, se desejar, descrição, prazo e responsável. A prioridade inicial é **Média**.
3. Use os filtros da página inicial para acompanhar as atividades.
4. Altere o status e a prioridade pelos menus de cada card. Use o botão de marcação para concluir ou reabrir uma atividade.
5. Acompanhe a quantidade de concluídas e de atrasadas no painel de progresso.

O cadastro de contatos é opcional: também é possível criar atividades sem responsável e sem prazo.

## Estrutura do projeto

| Arquivo ou pasta | Conteúdo |
| --- | --- |
| `app.py` | Configuração, modelos, rotas e regras de negócio |
| `templates/base.html` | Estrutura compartilhada pelas páginas |
| `templates/index.html` | Painel e lista de atividades |
| `templates/ad_atv.html` | Formulário de nova atividade |
| `templates/contacts.html` | Cadastro e lista de contatos |
| `static/style.css` | Estilos, temas e adaptações de tela |
| `static/app.js` | Comportamentos e animações da interface |
| `requirements.txt` | Dependências Python |
| `instance/todo.db` | Banco SQLite, criado ao iniciar a aplicação |

Os dados ficam salvos localmente em `instance/todo.db`. Essa pasta e o ambiente virtual são ignorados pelo Git. O banco de dados não precisa ser criado manualmente.

## Licença

Este repositório está distribuído sob a [licença MIT](LICENSE).