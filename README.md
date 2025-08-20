# 🚗 Sistema de Banco de Dados para Estacionamento

Este projeto é um sistema simples para gerenciamento de um estacionamento, desenvolvido em **Python** com integração a um banco de dados **SQLite**.  
O objetivo é registrar, consultar e gerenciar informações de veículos e clientes de forma prática e eficiente.

## 📂 Estrutura do Projeto

- **app.py** → Arquivo principal para execução do sistema.
- **base_de_dados.py** → Módulo responsável pela conexão e manipulação do banco de dados.
- **banco.db** → Banco de dados SQLite com as tabelas e registros.
- **banco.sql** → Script SQL para criação da estrutura do banco.
- **estrutura** → Possível arquivo de configuração ou documentação interna.
- **link** → Arquivo auxiliar (pode conter informações de conexão ou referências).

## 🛠 Tecnologias Utilizadas

- **Python 3.x**
- **SQLite**
- Bibliotecas padrão do Python (`sqlite3`, etc.)

## 🚀 Como Executar

1. **Clone o repositório**
   ```bash
   git clone https://github.com/eduardoegandra/Sistema-Banco-de-dados-Estacionamento.git
2. Acesse a pasta do projeto
   ```bash
cd Sistema-Banco-de-dados-Estacionamento

3. Execute o sistema
   ```bash
python app.py

📌 Funcionalidades- Cadastro de veículos
- Registro de entrada e saída
- Consulta de vagas disponíveis
- Histórico de movimentações
- Integração com banco de dados SQLite

📄 Estrutura do Banco de DadosO banco de dados é composto por tabelas que armazenam informações de clientes, veículos e movimentações.
O script banco.sql pode ser utilizado para recriar a estrutura do banco.📈 Possíveis Melhorias Futuras- Interface gráfica para interação mais amigável
- Relatórios de faturamento
- Controle de tarifas por período
- Integração com sistemas de pagamento


