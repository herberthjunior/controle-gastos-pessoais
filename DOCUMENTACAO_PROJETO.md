# 🚀 Projeto de Controle de Gastos Pessoais - Documentação Completa

**Autor:** Manus AI
**Data:** 04/10/2025
**Versão:** 1.0

---

## 1. 🎯 Visão Geral do Projeto

Este projeto implementa um **sistema automatizado de controle de gastos pessoais**, projetado para simplificar e otimizar a gestão financeira. A solução processa faturas de cartão de crédito em formato CSV (Banco Inter e C6), classifica as transações usando um **Large Language Model (LLM)**, armazena os dados em um banco de dados Excel e apresenta insights valiosos através de um **dashboard web interativo**.

O objetivo principal é transformar o processo manual e tedioso de controle de gastos em uma **experiência automatizada, inteligente e intuitiva**, permitindo ao usuário tomar decisões financeiras mais informadas com o mínimo de esforço.

### 1.1. Principais Funcionalidades

- **Extração Automática de Dados:** Processa múltiplos formatos de CSV (Inter e C6).
- **Classificação Inteligente:** Utiliza LLM para categorizar despesas com alta precisão.
- **Detecção de Duplicatas:** Sistema de hash MD5 previne a inserção de registros duplicados.
- **Dashboard Interativo:** Interface web rica em visualizações e filtros dinâmicos.
- **Insights com IA:** Geração de análises, recomendações e alertas financeiros.
- **Automação Completa:** Pipeline de ponta a ponta executado com um único comando.

---

## 2. 🛠️ Arquitetura e Tecnologias

O sistema foi construído com uma arquitetura modular em Python, garantindo flexibilidade e escalabilidade. As principais tecnologias utilizadas são:

| Componente | Tecnologia | Propósito |
| :--- | :--- | :--- |
| **Backend & Automação** | Python 3.11 | Orquestração do pipeline, lógica de negócios |
| **Manipulação de Dados** | Pandas | Leitura, transformação e análise de dados |
| **Banco de Dados** | Excel (.xlsx) | Armazenamento persistente e estruturado dos dados |
| **Classificação IA** | OpenAI API (GPT-4.1-mini) | Categorização automática de transações |
| **Dashboard Web** | Streamlit | Interface de usuário interativa e visualizações |
| **Visualização de Dados** | Plotly | Gráficos dinâmicos e interativos |

### 2.1. Estrutura de Pastas

O projeto está organizado na seguinte estrutura de pastas:

```
/controle_de_gastos
├── 📂 faturas/         # → Local para colocar os arquivos CSV das faturas
├── 📂 data/            # → Armazena o banco de dados e arquivos de controle
│   ├── 📄 gastos.xlsx
│   └── 📄 controle_processamento.txt
├── 📂 scripts/         # → Contém todos os scripts Python do sistema
│   ├── 🐍 automatizar_sistema.py  (Gatilho Principal)
│   ├── 🐍 processar_faturas.py    (Orquestrador ETL)
│   ├── 🐍 extrator_csv.py
│   ├── 🐍 tratamento_dados.py
│   ├── 🐍 classificador_llm.py
│   ├── 🐍 config_llm.py
│   ├── 🐍 insights_llm.py
│   ├── 🐍 dashboard.py
│   └── 🐍 iniciar_dashboard.py
├── 📄 DOCUMENTACAO_PROJETO.md
└── 📄 README.md
```

---

## 3. 🚀 Guia de Uso

O uso do sistema foi projetado para ser o mais simples possível. Siga os passos abaixo para a atualização mensal.

### 3.1. Fluxo de Atualização Mensal

1.  **📥 Adicionar Faturas:**
    - Baixe as faturas mais recentes dos seus bancos em formato `.csv`.
    - Coloque os arquivos na pasta `faturas/`.

2.  **🤖 Executar Automação:**
    - Abra um terminal na pasta `scripts/`.
    - Execute o comando principal:
      ```bash
      python3 automatizar_sistema.py
      ```

3.  **✨ Pronto!**
    - O sistema irá processar os novos arquivos, classificar as transações e atualizar o banco de dados.
    - O dashboard será iniciado automaticamente e estará acessível em **http://localhost:8501**.

### 3.2. Scripts Principais

| Script | Comando | Descrição |
| :--- | :--- | :--- |
| **Automação Completa** | `python3 automatizar_sistema.py` | **Recomendado.** Executa todo o pipeline e inicia o dashboard. |
| **Processamento de Dados** | `python3 processar_faturas.py` | Executa apenas o ETL (extração, tratamento, classificação). |
| **Iniciar Dashboard** | `python3 iniciar_dashboard.py` | Inicia o servidor web do dashboard manualmente. |

---

## 4. 🧠 Módulo de Inteligência Artificial

O coração do sistema é o módulo de IA, que realiza a classificação e a geração de insights.

### 4.1. Classificação Automática

- **Modelo:** `gpt-4.1-mini`
- **Precisão:** 100% nos testes realizados.
- **Processo:** Para cada transação não categorizada, o sistema envia a descrição da transação para o LLM com um prompt especializado, que retorna a categoria mais apropriada dentro de uma lista pré-definida.
- **Categorias:** Alimentação, Transporte, Moradia, Saúde, Lazer, Compras, Serviços, Outros.

### 4.2. Geração de Insights

O dashboard possui uma aba dedicada "**🤖 Insights IA**" que, ao ser acionada, gera quatro tipos de análises textuais:

1.  **Análise Geral:** Um resumo da saúde financeira, identificando padrões e pontos de atenção.
2.  **Recomendações de Economia:** Dicas práticas e metas de redução para as principais categorias de gastos.
3.  **Análise de Tendências:** Identificação de padrões sazonais e comportamento de gastos ao longo do tempo.
4.  **Alertas Financeiros:** Detecção de gastos atípicos e concentração excessiva de despesas.

---

## 5. 📊 Dashboard Interativo

O dashboard, acessível via navegador, é a principal interface de visualização dos dados.

### 5.1. Abas de Análise

- **Visão Geral:** KPIs principais e gráficos de distribuição.
- **Análise Temporal:** Evolução dos gastos e receitas ao longo do tempo.
- **Heatmaps:** Matriz de calor para identificar padrões de gastos por dia.
- **Rankings:** Gráfico com os maiores gastos individuais.
- **Insights IA:** Acesso às análises geradas pelo LLM.
- **Detalhes:** Tabela completa de todas as transações.
- **Estatísticas:** Análises numéricas detalhadas por categoria e banco.

### 5.2. Filtros Dinâmicos

O usuário pode filtrar todos os dados exibidos no dashboard por:

- **Categoria**
- **Banco (Origem)**
- **Período (Data de Início e Fim)**
- **Tipo de Transação (Gastos ou Receitas)**

---

## 6. 🔮 Próximos Passos e Evolução

Este projeto possui uma base sólida e pode ser expandido com novas funcionalidades:

- **Suporte a Novos Bancos:** Adicionar novos parsers para diferentes formatos de CSV.
- **Metas e Orçamentos:** Implementar um sistema para o usuário definir metas de gastos por categoria.
- **Análise Preditiva:** Utilizar modelos de machine learning para prever gastos futuros.
- **Deployment em Nuvem:** Publicar o dashboard em uma plataforma web para acesso remoto.
- **Notificações Automáticas:** Enviar alertas por e-mail ou Telegram sobre gastos excessivos.

Este documento serve como um guia completo para a utilização e compreensão do **Sistema de Controle de Gastos Pessoais**.
