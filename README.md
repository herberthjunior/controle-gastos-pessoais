# 💰 Sistema de Controle de Gastos Pessoais

Um sistema automatizado e inteligente para controle de gastos pessoais, com classificação automática usando IA e dashboard interativo.

## 🚀 Funcionalidades

- **📊 Extração Automática**: Processa faturas CSV dos bancos Inter e C6
- **🤖 Classificação com IA**: Categorização automática usando GPT-4.1-mini
- **📈 Dashboard Interativo**: Interface web com gráficos e filtros dinâmicos
- **🧠 Insights Inteligentes**: Análises e recomendações geradas por IA
- **🔄 Automação Completa**: Pipeline de ponta a ponta com um único comando
- **☁️ Integração Google Drive**: Suporte para pasta compartilhada

## 🛠️ Tecnologias

- **Python 3.11+**
- **Streamlit** (Dashboard Web)
- **Plotly** (Visualizações)
- **Pandas** (Manipulação de dados)
- **OpenAI API** (Classificação IA)

## 📦 Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/herberthjunior/controle-gastos-pessoais.git
   cd controle-gastos-pessoais
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure a API do OpenAI:**
   - Defina a variável de ambiente `OPENAI_API_KEY`
   - Ou configure no arquivo `scripts/config_llm.py`

## 🚀 Uso Rápido

### Método 1: Arquivos Locais

1. **Adicione suas faturas** na pasta `faturas/`:
   - Banco Inter: `fatura-inter-YYYY-MM.csv`
   - Banco C6: `Fatura_YYYY-MM-DD.csv`

2. **Execute a automação:**
   ```bash
   cd scripts
   python automatizar_sistema.py
   ```

3. **Acesse o dashboard:** http://localhost:8501

### Método 2: Google Drive (Recomendado)

1. **Configure a pasta do Google Drive** (veja seção abaixo)
2. **Execute com Google Drive:**
   ```bash
   cd scripts
   python automatizar_sistema.py --google-drive
   ```

## ☁️ Configuração Google Drive

Para usar uma pasta compartilhada do Google Drive:

1. **Crie uma pasta no Google Drive** e compartilhe com acesso de edição
2. **Copie o ID da pasta** da URL (parte após `/folders/`)
3. **Configure no arquivo** `scripts/config_google_drive.py`:
   ```python
   GOOGLE_DRIVE_FOLDER_ID = "seu_folder_id_aqui"
   ```

## 📊 Dashboard

O dashboard possui 7 abas principais:

- **📊 Visão Geral**: KPIs e distribuição por categoria
- **📈 Análise Temporal**: Evolução dos gastos ao longo do tempo
- **🔥 Heatmaps**: Padrões de gastos por dia/semana
- **🏆 Rankings**: Maiores gastos individuais
- **🤖 Insights IA**: Análises e recomendações inteligentes
- **📋 Detalhes**: Tabela completa de transações
- **📊 Estatísticas**: Métricas detalhadas

## 🧠 Insights com IA

O sistema gera 4 tipos de análises inteligentes:

1. **Análise Geral**: Resumo da saúde financeira
2. **Recomendações**: Dicas práticas de economia
3. **Tendências**: Padrões temporais de gastos
4. **Alertas**: Detecção de gastos atípicos

## 📁 Estrutura do Projeto

```
controle-gastos-pessoais/
├── 📂 faturas/              # Arquivos CSV das faturas
├── 📂 data/                 # Banco de dados e controles
├── 📂 scripts/              # Scripts Python
│   ├── automatizar_sistema.py    # 🚀 Script principal
│   ├── processar_faturas.py      # ETL pipeline
│   ├── dashboard.py              # Interface web
│   └── ...
├── 📄 requirements.txt      # Dependências
├── 📄 README.md            # Este arquivo
└── 📄 DOCUMENTACAO_PROJETO.md    # Documentação completa
```

## 🔧 Scripts Principais

| Script | Comando | Descrição |
|--------|---------|-----------|
| **Automação Completa** | `python automatizar_sistema.py` | Executa todo o pipeline |
| **Apenas Processamento** | `python processar_faturas.py` | ETL sem dashboard |
| **Apenas Dashboard** | `python iniciar_dashboard.py` | Inicia interface web |

## 📈 Exemplo de Uso

```bash
# 1. Adicionar novas faturas na pasta faturas/
# 2. Executar automação
python scripts/automatizar_sistema.py

# Saída esperada:
# ✅ 45 transações processadas
# ✅ 45 registros classificados (100% sucesso)
# 🌐 Dashboard disponível em: http://localhost:8501
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para dúvidas ou suporte:
- Abra uma [Issue](https://github.com/herberthjunior/controle-gastos-pessoais/issues)
- Consulte a [Documentação Completa](DOCUMENTACAO_PROJETO.md)

---

**Desenvolvido com ❤️ por [Manus AI](https://manus.im)**
