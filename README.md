# QA Automation – Petstore API & SauceDemo Web

Projeto de automação de testes cobrindo **API REST** e **interface web (E2E)**, desenvolvido com Python, Pytest e Selenium, com pipeline de CI integrada via **GitHub Actions**.

---

## 🗂️ Estrutura do Repositório

```
qa-automation/
├── .github/
│   └── workflows/
│       └── qa-pipeline.yml       # Pipeline CI (API + Web)
├── api-tests/
│   ├── tests/
│   │   ├── test_pet.py           # Endpoints /pet
│   │   ├── test_store.py         # Endpoints /store
│   │   └── test_user.py          # Endpoints /user
│   ├── utils/
│   │   └── helpers.py            # Utilitário de URL
│   ├── conftest.py               # Fixture da sessão HTTP
│   ├── pytest.ini
│   └── requirements.txt
├── web-tests/
│   ├── pages/
│   │   ├── base_page.py          # Page Object base (helpers Selenium)
│   │   ├── login_page.py
│   │   ├── inventory_page.py
│   │   ├── cart_page.py
│   │   └── checkout_page.py
│   ├── tests/
│   │   └── test_saucedemo.py     # Testes E2E
│   ├── conftest.py               # Fixture do driver Chrome
│   ├── pytest.ini
│   └── requirements.txt
└── README.md
```

---

## 🛠️ Tecnologias

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.11 |
| Framework de testes | Pytest |
| Automação Web | Selenium 4 |
| Requisições HTTP | Requests |
| Relatórios | pytest-html |
| CI/CD | GitHub Actions |

---

## ⚙️ Pré-requisitos

- Python 3.11+
- Google Chrome instalado
- `pip` atualizado

---

## 🚀 Instalação e Execução

### 1. Clone o repositório

```bash
git clone https://github.com/<seu-usuario>/qa-automation.git
cd qa-automation
```

### 2. Testes de API – Petstore

```bash
cd api-tests
pip install -r requirements.txt
pytest
```

Gerar relatório HTML:
```bash
pytest --html=report.html --self-contained-html
```

### 3. Testes Web – SauceDemo

```bash
cd web-tests
pip install -r requirements.txt
pytest
```

---

## 🔁 Pipeline de CI (GitHub Actions)

A pipeline é disparada automaticamente em todo **push** ou **pull request** para a branch `main`.

**Jobs:**
- `api-tests` → instala dependências e roda os testes da API
- `web-tests` → instala o Chrome, dependências e roda os testes E2E

Os relatórios HTML são salvos como **artefatos** ao final de cada execução.

**Arquivo:** `.github/workflows/qa-pipeline.yml`

---

## 🧪 Cenários Cobertos

### API – Petstore (`https://petstore.swagger.io/v2`)

| Módulo | Cenário |
|---|---|
| Pet | Criar, buscar, atualizar, buscar por status, deletar |
| Store | Consultar inventário, criar pedido, buscar pedido, deletar |
| User | Criar usuário, buscar, login, atualizar, logout, deletar |

### Web – SauceDemo (`https://www.saucedemo.com`)

| Cenário | Descrição |
|---|---|
| Login com sucesso | Autentica com `standard_user` e valida redirecionamento |
| Login inválido | Verifica mensagem de erro para credenciais incorretas |
| Adicionar ao carrinho | Adiciona 2 produtos e valida o badge do carrinho |
| Fluxo E2E completo | Login → adicionar produtos → checkout → confirmação de pedido |

---

## 🏗️ Design Pattern

O projeto web utiliza o padrão **Page Object Model (POM)**:

- Cada página tem sua própria classe que encapsula os locators e ações
- `BasePage` centraliza os métodos genéricos do Selenium (`find`, `click`, `type`)
- Os testes ficam limpos, sem lógica de UI, apenas orquestrando as páginas

---

## 📋 Credenciais SauceDemo

```
Usuário: standard_user
Senha:   secret_sauce
```

---

## ✅ Boas Práticas Adotadas

- Fixtures com escopo `session` para reuso eficiente do driver e da sessão HTTP
- Nomes de teste descritivos no padrão `test_<ação>_<resultado_esperado>`
- Dados de teste isolados por arquivo (sem dependência entre módulos)
- Asserções explícitas com mensagens claras
- Headless Chrome para execução em CI sem interface gráfica
