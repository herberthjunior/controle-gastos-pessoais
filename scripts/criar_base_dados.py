#!/usr/bin/env python3
"""
Script para criar o arquivo inicial gastos.xlsx com a estrutura definida.
Parte do Sistema de Controle de Gastos Pessoais.
"""

import pandas as pd
import os

def criar_arquivo_base():
    """Cria o arquivo gastos.xlsx com o cabeçalho estruturado."""
    
    # Definir o caminho do arquivo
    caminho_arquivo = "../data/gastos.xlsx"
    
    # Verificar se o arquivo já existe
    if os.path.exists(caminho_arquivo):
        print(f"Arquivo {caminho_arquivo} já existe. Não será sobrescrito.")
        return
    
    # Definir a estrutura das colunas
    colunas = [
        'Data',           # Data da transação (formato DD/MM/AAAA)
        'Descricao',      # Descrição original como aparece na fatura
        'Valor',          # Valor da transação (número decimal)
        'Categoria',      # Categoria que será preenchida pelo LLM
        'Subcategoria',   # Subcategoria opcional para detalhamento
        'Mes_Ano',        # Formato MM/AAAA para facilitar filtros
        'Observacoes'     # Campo livre para anotações manuais
    ]
    
    # Criar DataFrame vazio com as colunas definidas
    df = pd.DataFrame(columns=colunas)
    
    # Salvar o arquivo Excel
    df.to_excel(caminho_arquivo, index=False, engine='openpyxl')
    
    print(f"Arquivo {caminho_arquivo} criado com sucesso!")
    print(f"Estrutura das colunas: {', '.join(colunas)}")

if __name__ == "__main__":
    criar_arquivo_base()
