# 🚗 Sistema de Gerenciamento de Estacionamento

Sistema web para gerenciamento de um estacionamento, desenvolvido em **Python** com **Flask** e banco de dados **MySQL**.

O sistema permite cadastrar clientes e veículos, controlar vagas disponíveis, registrar entradas e saídas com cálculo automático de valores, e consultar o histórico financeiro de transações.

## 🛠 Tecnologias Utilizadas

- **Python 3.11+**
- **Flask** (framework web)
- **MySQL** (banco de dados)
- **mysql-connector-python** (conexão com o banco)
- **Jinja2** (templates HTML)
- **Bootstrap 5** (estilização)

## 📌 Funcionalidades

- Cadastro, edição, exclusão e consulta de **clientes**
- Cadastro, edição, exclusão e consulta de **veículos**, vinculados a um cliente
- Consulta de **vagas** com filtro por status (livre/ocupada) e tipo
- **Registro de entrada** de veículo, associando a uma vaga livre
- **Registro de saída**, com cálculo automático do valor a pagar (por hora, com cobrança de hora cheia, ou diária para permanências acima de 12h)
- Histórico de **estadias** por veículo
- Histórico de **transações** financeiras, com filtro por data e placa
- Atualização automática do status da vaga (LIVRE/OCUPADA) via triggers do banco de dados

## 📂 Estrutura do Projeto

    Sistema-Banco-de-dados-Estacionamento/
    ├── app.py                  → Rotas e lógica principal da aplicação Flask
    ├── base_de_dados.py        → Conexão com o banco de dados MySQL
    ├── banco.sql                → Script SQL para criação das tabelas e dados de exemplo
    ├── templates/                → Templates HTML (Jinja2)
    │   ├── base.html
    │   ├── index.html
    │   ├── clientes.html
    │   ├── novo_cliente.html
    │   ├── editar_cliente.html
    │   ├── veiculos.html
    │   ├── novo_veiculo.html
    │   ├── editar_veiculo.html
    │   ├── veiculos_cliente.html
    │   ├── historico_veiculo.html
    │   ├── vagas.html
    │   ├── estadias.html
    │   ├── registrar_entrada.html
    │   ├── confirmar_saida.html
    │   ├── detalhes_estadia.html
    │   └── transacoes.html
    └── static/
        └── css/
            └── style.css

## 🚀 Como Executar

### Pré-requisitos

- [Python 3.11+](https://www.python.org/downloads/)
- [MySQL Server](https://dev.mysql.com/downloads/installer/) instalado e rodando localmente

### 1. Clone o repositório

    git clone https://github.com/eduardoegandra/Sistema-Banco-de-dados-Estacionamento.git
    cd Sistema-Banco-de-dados-Estacionamento

### 2. Crie e ative um ambiente virtual

    python -m venv .venv
    # Windows
    .venv\Scripts\Activate.ps1
    # Linux/Mac
    source .venv/bin/activate

### 3. Instale as dependências

    pip install flask mysql-connector-python

### 4. Configure o banco de dados

Crie o banco no MySQL:

    mysql -u root -p -e "CREATE DATABASE trabalho_bd CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

Importe a estrutura e os dados de exemplo:

    mysql -u root -p --default-character-set=utf8mb4 trabalho_bd < banco.sql

### 5. Configure a conexão com o banco

Edite o arquivo `base_de_dados.py` com o usuário e senha do seu MySQL local:

    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='SUA_SENHA_AQUI',
        database='trabalho_bd',
        buffered=True,
        charset='utf8mb4'
    )

### 6. Execute o sistema

    python app.py

Acesse no navegador: **http://127.0.0.1:5000**

## 📊 Estrutura do Banco de Dados

O banco é composto pelas tabelas: `Cliente`, `Veiculo`, `TipoVeiculo`, `Vaga`, `TipoVaga`, `Estadia`, `Transacao`, `TabelaPrecos` e `Funcionario`, com relacionamentos entre clientes/veículos e vagas/estadias. Triggers automáticos atualizam o status da vaga (LIVRE/OCUPADA) sempre que uma estadia é criada ou finalizada.

## ⚠️ Aviso de Segurança

Este projeto é de fins acadêmicos. A senha do banco de dados está definida diretamente em `base_de_dados.py` apenas para fins de desenvolvimento local. Não recomendado para uso em produção sem o uso de variáveis de ambiente.

## 📈 Possíveis Melhorias Futuras

- Autenticação de usuários/funcionários
- Relatórios de faturamento por período
- Painel administrativo com gráficos de ocupação
- Integração com sistemas de pagamento