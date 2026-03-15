# Sistema de Cadastro Acadêmico (Python + CustomTkinter)

## Objetivo

Desenvolver um **sistema de cadastro acadêmico com interface gráfica** utilizando **Python e CustomTkinter**.
O sistema permitirá registrar **alunos, professores e funcionários**, armazenando dados pessoais e de contato.

O projeto deve ser **modular**, separando interface, lógica e modelos de dados.

---

# Tecnologias Utilizadas

* Python 3
* CustomTkinter
* Tkinter
* JSON para persistência de dados

Instalação da biblioteca principal:

```bash
pip install customtkinter
```

---

# Estrutura do Projeto

```text
sistema_academico/

main.py

ui/
    app.py
    tela_principal.py
    tela_cadastro.py
    componentes.py

models/
    pessoa.py
    aluno.py
    professor.py
    funcionario.py

services/
    cadastro_service.py
    validacao_service.py

database/
    database.py

data/
    pessoas.json

README.md
```

---

# Descrição dos Módulos

## main.py

Arquivo de entrada do sistema.

Responsável por iniciar a aplicação gráfica.

Exemplo:

```python
from ui.app import App

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
```

---

# ui/

Contém toda a **interface gráfica do sistema**.

## app.py

Cria a aplicação principal usando CustomTkinter.

Responsável por:

* iniciar a janela
* carregar telas
* gerenciar navegação

---

## tela_principal.py

Tela inicial do sistema.

Contém o menu com opções como:

* Cadastrar aluno
* Cadastrar professor
* Cadastrar funcionário
* Listar registros

---

## tela_cadastro.py

Tela de cadastro reutilizável.

Campos do formulário:

* CPF
* Nome completo
* Email
* Telefone
* Data de nascimento
* CEP
* Rua
* Cidade
* Estado

Campos adicionais podem aparecer dependendo do tipo:

Aluno:

* matrícula
* curso

Professor:

* departamento

Funcionário:

* cargo

---

## componentes.py

Componentes reutilizáveis da interface.

Exemplo:

* campo de formulário
* botão estilizado
* mensagens de alerta

---

# models/

Define as **estruturas de dados do sistema**.

## pessoa.py

Classe base para todas as pessoas cadastradas.

Atributos:

* nome
* cpf
* email
* telefone
* nascimento
* cep
* endereço

---

## aluno.py

Herda de `Pessoa`.

Atributos adicionais:

* matrícula
* curso

---

## professor.py

Herda de `Pessoa`.

Atributos adicionais:

* departamento

---

## funcionario.py

Herda de `Pessoa`.

Atributos adicionais:

* cargo

---

# services/

Contém a **lógica do sistema**.

## cadastro_service.py

Responsável por:

* criar registros
* listar registros
* editar registros
* excluir registros

---

## validacao_service.py

Responsável por validar dados como:

* CPF válido
* email válido
* telefone válido
* campos obrigatórios

---

# database/

Responsável pela **persistência dos dados**.

## database.py

Funções principais:

* salvar dados
* carregar dados
* atualizar registros

Os dados são armazenados em arquivos JSON.

---

# data/

Contém os arquivos de armazenamento.

```text
pessoas.json
```

Exemplo de estrutura de dados:

```json
[
  {
    "tipo": "aluno",
    "nome": "João Silva",
    "cpf": "00000000000",
    "email": "joao@email.com",
    "telefone": "62999999999",
    "cep": "74000000"
  }
]
```

---

# Fluxo do Sistema

1. O usuário executa `main.py`
2. A aplicação gráfica é iniciada
3. A tela principal é exibida
4. O usuário escolhe uma ação
5. O sistema abre a tela de cadastro ou listagem
6. Os dados são validados
7. Os dados são salvos no arquivo JSON

---

# Funcionalidades Esperadas

Cadastro de:

* alunos
* professores
* funcionários

Operações:

* criar registro
* listar registros
* editar registro
* excluir registro

---

# Ordem Recomendada de Desenvolvimento

1. Criar a estrutura de pastas
2. Implementar a classe `Pessoa`
3. Criar as classes `Aluno`, `Professor` e `Funcionario`
4. Criar o sistema de salvamento em JSON
5. Implementar a interface principal
6. Criar a tela de cadastro
7. Implementar validação de dados
8. Implementar listagem de registros
9. Implementar edição e exclusão

---

# Como Executar

No terminal:

```bash
python main.py
```

---

# Observações

* O código deve ser modular
* Evitar lógica de negócio dentro da interface
* Separar claramente interface, modelos e serviços
* Utilizar orientação a objetos para representar entidades
* Garantir que os dados sejam persistidos entre execuções do programa
