# Análise dos Formatos de CSV dos Bancos

## Banco Inter
**Padrão do nome do arquivo:** `fatura-inter-YYYY-MM.csv`

**Estrutura do CSV:**
- **Separador:** Vírgula (,)
- **Encoding:** UTF-8 com BOM
- **Cabeçalho:** "Data","Lançamento","Categoria","Tipo","Valor"

**Colunas:**
1. **Data:** Formato DD/MM/YYYY (ex: "01/10/2025")
2. **Lançamento:** Descrição do estabelecimento/transação (ex: "APPLE COM BILL SAO PAULO BRA")
3. **Categoria:** Categoria pré-definida pelo banco (ex: "COMPRAS", "RESTAURANTES")
4. **Tipo:** Tipo da transação (ex: "Compra à vista")
5. **Valor:** Formato monetário brasileiro com "R$" (ex: "R$ 29,90")

**Exemplo de linha:**
```
"01/10/2025","APPLE COM BILL         SAO PAULO     BRA","COMPRAS","Compra à vista","R$ 29,90"
```

## Banco C6
**Padrão do nome do arquivo:** `Fatura_YYYY-MM-DD.csv`

**Estrutura do CSV:**
- **Separador:** Ponto e vírgula (;)
- **Encoding:** UTF-8
- **Cabeçalho:** Data de Compra;Nome no Cartão;Final do Cartão;Categoria;Descrição;Parcela;Valor (em US$);Cotação (em R$);Valor (em R$)

**Colunas:**
1. **Data de Compra:** Formato DD/MM/YYYY (ex: "06/09/2025")
2. **Nome no Cartão:** Nome do portador (ex: "HERBERTH JUNIOR")
3. **Final do Cartão:** Últimos 4 dígitos (ex: "7164")
4. **Categoria:** Categoria detalhada (ex: "Supermercados / Mercearia / Padarias / Lojas de Conveniência")
5. **Descrição:** Nome do estabelecimento (ex: "UNIMED GOIANIA")
6. **Parcela:** Informação de parcelamento (ex: "4/4", "Única")
7. **Valor (em US$):** Valor em dólares (geralmente "0")
8. **Cotação (em R$):** Cotação do dólar (geralmente "0")
9. **Valor (em R$):** Valor em reais (ex: "199.09")

**Exemplo de linha:**
```
25/06/2025;HERBERTH JUNIOR;7509;Seguro;UNIMED GOIANIA;4/4;0;0;199.09
```

## Mapeamento para Estrutura Unificada

### Banco Inter → Estrutura Padrão
- Data → Data
- Lançamento → Descricao
- Valor → Valor (limpar "R$" e converter vírgula para ponto)
- Categoria → Categoria_Original (manter para referência)
- Origem → "Inter"

### Banco C6 → Estrutura Padrão
- Data de Compra → Data
- Descrição → Descricao
- Valor (em R$) → Valor
- Categoria → Categoria_Original (manter para referência)
- Origem → "C6"

## Observações Importantes
1. **Tratamento de valores negativos:** C6 pode ter valores negativos (estornos)
2. **Parcelamento:** C6 tem informação de parcelas que pode ser útil
3. **Categorias:** Ambos os bancos já têm categorização, mas usaremos LLM para padronizar
4. **Encoding:** Inter usa BOM, C6 não - tratar na leitura
