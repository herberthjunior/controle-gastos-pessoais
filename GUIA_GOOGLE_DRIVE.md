# ☁️ Guia de Integração com Google Drive

Este guia explica como configurar e usar a integração com Google Drive para compartilhar arquivos de faturas mensalmente.

---

## 🎯 Objetivo

Permitir que você coloque seus arquivos CSV de faturas em uma pasta do Google Drive e o sistema baixe automaticamente para processamento, facilitando o compartilhamento e backup dos dados.

---

## 🚀 Configuração Rápida

### Passo 1: Preparar Arquivos no Google Drive

1. **Faça upload** dos seus arquivos CSV para o Google Drive
2. **Compartilhe cada arquivo** individualmente:
   - Clique com botão direito no arquivo
   - Selecione "Compartilhar"
   - Clique em "Alterar para qualquer pessoa com o link"
   - Defina permissão como "Visualizador"
   - Copie o link compartilhado

### Passo 2: Configurar URLs no Sistema

1. **Abra o arquivo** `scripts/config_google_drive.py`
2. **Substitua os exemplos** pela lista dos seus arquivos:

```python
URLS_ARQUIVOS_EXEMPLO = [
    {
        'url': 'https://drive.google.com/file/d/SEU_FILE_ID_REAL_1/view',
        'nome': 'fatura-inter-2025-11.csv'
    },
    {
        'url': 'https://drive.google.com/file/d/SEU_FILE_ID_REAL_2/view',
        'nome': 'Fatura_2025-11-15.csv'
    }
]
```

### Passo 3: Executar com Google Drive

```bash
cd scripts
python3 automatizar_sistema.py --google-drive
```

---

## 📋 Exemplo Prático

### Cenário: Atualização Mensal de Novembro

1. **Upload no Google Drive:**
   - `fatura-inter-2025-11.csv`
   - `Fatura_2025-11-15.csv`

2. **Compartilhar arquivos** e obter links:
   - Inter: `https://drive.google.com/file/d/1ABC123.../view`
   - C6: `https://drive.google.com/file/d/1XYZ789.../view`

3. **Configurar no sistema:**
```python
URLS_ARQUIVOS_EXEMPLO = [
    {
        'url': 'https://drive.google.com/file/d/1ABC123DEF456GHI789JKL/view',
        'nome': 'fatura-inter-2025-11.csv'
    },
    {
        'url': 'https://drive.google.com/file/d/1XYZ789ABC123DEF456GHI/view',
        'nome': 'Fatura_2025-11-15.csv'
    }
]
```

4. **Executar:**
```bash
python3 automatizar_sistema.py --google-drive
```

5. **Resultado:**
```
☁️  Modo Google Drive ativado
📥 Baixando arquivos do Google Drive...
📥 Baixando: fatura-inter-2025-11.csv
✅ Arquivo salvo: ../faturas/fatura-inter-2025-11.csv
📥 Baixando: Fatura_2025-11-15.csv
✅ Arquivo salvo: ../faturas/Fatura_2025-11-15.csv
✅ 2 arquivos baixados do Google Drive
```

---

## 🔧 Comandos Disponíveis

| Comando | Descrição |
|---------|-----------|
| `python3 automatizar_sistema.py` | Processamento normal (arquivos locais) |
| `python3 automatizar_sistema.py --google-drive` | Baixar do Google Drive + processar |
| `python3 automatizar_sistema.py --google-drive --sem-dashboard` | Apenas baixar e processar |

---

## 💡 Dicas e Boas Práticas

### Organização no Google Drive

1. **Crie uma pasta** específica para faturas (ex: "Faturas Cartão")
2. **Organize por mês/ano** para facilitar localização
3. **Use nomes consistentes** seguindo os padrões:
   - Inter: `fatura-inter-YYYY-MM.csv`
   - C6: `Fatura_YYYY-MM-DD.csv`

### Segurança

- ✅ **Links compartilhados** são seguros (apenas visualização)
- ✅ **Dados ficam no seu Google Drive** (você mantém controle)
- ✅ **Sistema baixa temporariamente** apenas para processamento
- ⚠️ **Não compartilhe** o arquivo `config_google_drive.py` com URLs reais

### Fluxo Mensal Recomendado

1. **Baixe as faturas** dos bancos
2. **Faça upload** para o Google Drive
3. **Compartilhe os novos arquivos**
4. **Atualize** `config_google_drive.py` com os novos links
5. **Execute** `python3 automatizar_sistema.py --google-drive`

---

## 🆘 Solução de Problemas

### Erro: "Arquivo não encontrado"
- Verifique se o link está correto
- Confirme que o arquivo está compartilhado publicamente

### Erro: "Acesso negado"
- Certifique-se que a permissão está como "Qualquer pessoa com o link"
- Teste o link no navegador antes de usar

### Erro: "Módulo não encontrado"
- Verifique se está na pasta `scripts/`
- Confirme que o arquivo `google_drive_integration.py` existe

### Links não funcionam
- Use links no formato: `https://drive.google.com/file/d/FILE_ID/view`
- Evite links encurtados ou com parâmetros extras

---

## 🔄 Automatização Futura

Para automatizar ainda mais o processo, você pode:

1. **Criar um script** que gera automaticamente a configuração
2. **Usar a API oficial** do Google Drive (requer autenticação)
3. **Configurar sincronização** automática com Google Drive Desktop

---

**💡 Lembre-se:** Esta integração facilita o compartilhamento, mas você sempre pode usar o método tradicional colocando os arquivos diretamente na pasta `faturas/`.
