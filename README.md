# 🛍️ Sistema de Gerenciamento de Produtos

Este é um sistema simples de cadastro, edição e exclusão de produtos, feito com Python e Flask. Ele permite que o usuário gerencie um inventário básico via interface web.

## 🚀 Tecnologias usadas

- Python 3.13.3
- Flask
- SQLite (via SQLAlchemy)
- HTML + CSS
- JavaScript

## ⚙️ Como executar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
```

### 2. Crie e ative um ambiente virtual (recomendado)

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o sistema de gerenciamento de produtos

Em alguns casos ao invés de python é py ou python3.

```bash
python main.py
```

A aplicação estará rodando em http://localhost:5000

🗃️ Banco de Dados

O sistema usa SQLite. O banco é criado automaticamente na pasta instance/ na primeira execução.
