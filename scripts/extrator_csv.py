#!/usr/bin/env python3
"""
Módulo de Extração de CSV - Sistema de Controle de Gastos Pessoais
Processa arquivos CSV dos Bancos Inter e C6, padronizando os dados.
"""

import pandas as pd
import os
import re
from datetime import datetime
from typing import List, Dict, Tuple

class ExtratorCSV:
    def __init__(self, pasta_faturas: str = "../faturas"):
        self.pasta_faturas = pasta_faturas
        self.dados_processados = []
    
    def identificar_banco(self, nome_arquivo: str) -> str:
        """
        Identifica o banco baseado no padrão do nome do arquivo.
        
        Args:
            nome_arquivo: Nome do arquivo CSV
            
        Returns:
            'inter', 'c6' ou 'desconhecido'
        """
        if re.match(r'fatura-inter-\d{4}-\d{2}\.csv', nome_arquivo):
            return 'inter'
        elif re.match(r'Fatura_\d{4}-\d{2}-\d{2}\.csv', nome_arquivo):
            return 'c6'
        else:
            return 'desconhecido'
    
    def extrair_mes_ano_do_arquivo(self, nome_arquivo: str, banco: str) -> str:
        """
        Extrai o mês/ano do nome do arquivo.
        
        Args:
            nome_arquivo: Nome do arquivo
            banco: Banco identificado ('inter' ou 'c6')
            
        Returns:
            String no formato MM/YYYY
        """
        if banco == 'inter':
            # fatura-inter-2025-10.csv -> 10/2025
            match = re.search(r'fatura-inter-(\d{4})-(\d{2})\.csv', nome_arquivo)
            if match:
                ano, mes = match.groups()
                return f"{mes}/{ano}"
        elif banco == 'c6':
            # Fatura_2025-10-10.csv -> 10/2025
            match = re.search(r'Fatura_(\d{4})-(\d{2})-\d{2}\.csv', nome_arquivo)
            if match:
                ano, mes = match.groups()
                return f"{mes}/{ano}"
        
        return "00/0000"  # Fallback
    
    def processar_inter(self, caminho_arquivo: str, mes_ano: str) -> List[Dict]:
        """
        Processa arquivo CSV do Banco Inter.
        
        Args:
            caminho_arquivo: Caminho completo do arquivo
            mes_ano: Mês/ano no formato MM/YYYY
            
        Returns:
            Lista de dicionários com os dados padronizados
        """
        try:
            # Ler CSV do Inter (com BOM, separador vírgula)
            df = pd.read_csv(caminho_arquivo, encoding='utf-8-sig', sep=',')
            
            dados = []
            for _, row in df.iterrows():
                # Limpar e converter valor
                valor_str = str(row['Valor']).replace('R$', '').replace(' ', '').replace(',', '.')
                try:
                    valor = float(valor_str)
                except:
                    valor = 0.0
                
                # Padronizar data
                data_str = str(row['Data'])
                
                dados.append({
                    'Data': data_str,
                    'Descricao': str(row['Lançamento']).strip(),
                    'Valor': valor,
                    'Categoria': '',  # Será preenchida pelo LLM
                    'Subcategoria': '',
                    'Mes_Ano': mes_ano,
                    'Observacoes': f"Categoria Original: {row['Categoria']} | Tipo: {row['Tipo']}",
                    'Origem': 'Inter'
                })
            
            return dados
            
        except Exception as e:
            print(f"Erro ao processar arquivo Inter {caminho_arquivo}: {e}")
            return []
    
    def processar_c6(self, caminho_arquivo: str, mes_ano: str) -> List[Dict]:
        """
        Processa arquivo CSV do Banco C6.
        
        Args:
            caminho_arquivo: Caminho completo do arquivo
            mes_ano: Mês/ano no formato MM/YYYY
            
        Returns:
            Lista de dicionários com os dados padronizados
        """
        try:
            # Ler CSV do C6 (separador ponto e vírgula)
            df = pd.read_csv(caminho_arquivo, encoding='utf-8', sep=';')
            
            dados = []
            for _, row in df.iterrows():
                # Converter valor (já vem como número)
                try:
                    valor = float(row['Valor (em R$)'])
                except:
                    valor = 0.0
                
                # Padronizar data
                data_str = str(row['Data de Compra'])
                
                # Informação de parcela
                parcela_info = str(row['Parcela']) if pd.notna(row['Parcela']) else ''
                
                dados.append({
                    'Data': data_str,
                    'Descricao': str(row['Descrição']).strip(),
                    'Valor': valor,
                    'Categoria': '',  # Será preenchida pelo LLM
                    'Subcategoria': '',
                    'Mes_Ano': mes_ano,
                    'Observacoes': f"Categoria Original: {row['Categoria']} | Parcela: {parcela_info}",
                    'Origem': 'C6'
                })
            
            return dados
            
        except Exception as e:
            print(f"Erro ao processar arquivo C6 {caminho_arquivo}: {e}")
            return []
    
    def processar_todos_arquivos(self) -> List[Dict]:
        """
        Processa todos os arquivos CSV na pasta de faturas.
        
        Returns:
            Lista consolidada com todos os dados processados
        """
        todos_dados = []
        
        if not os.path.exists(self.pasta_faturas):
            print(f"Pasta {self.pasta_faturas} não encontrada!")
            return todos_dados
        
        arquivos_csv = [f for f in os.listdir(self.pasta_faturas) if f.endswith('.csv')]
        
        for arquivo in arquivos_csv:
            caminho_completo = os.path.join(self.pasta_faturas, arquivo)
            banco = self.identificar_banco(arquivo)
            
            if banco == 'desconhecido':
                print(f"Arquivo {arquivo} não segue padrão conhecido. Ignorando.")
                continue
            
            mes_ano = self.extrair_mes_ano_do_arquivo(arquivo, banco)
            
            print(f"Processando {arquivo} (Banco: {banco.upper()}, Período: {mes_ano})")
            
            if banco == 'inter':
                dados = self.processar_inter(caminho_completo, mes_ano)
            elif banco == 'c6':
                dados = self.processar_c6(caminho_completo, mes_ano)
            
            todos_dados.extend(dados)
            print(f"  → {len(dados)} transações processadas")
        
        self.dados_processados = todos_dados
        return todos_dados
    
    def salvar_dados_temporarios(self, dados: List[Dict], arquivo_saida: str = "../data/dados_temp.xlsx"):
        """
        Salva os dados processados em um arquivo temporário para análise.
        
        Args:
            dados: Lista de dados processados
            arquivo_saida: Caminho do arquivo de saída
        """
        if not dados:
            print("Nenhum dado para salvar.")
            return
        
        df = pd.DataFrame(dados)
        df.to_excel(arquivo_saida, index=False, engine='openpyxl')
        print(f"Dados temporários salvos em: {arquivo_saida}")
        print(f"Total de transações: {len(dados)}")

def main():
    """Função principal para teste do módulo."""
    extrator = ExtratorCSV()
    
    print("=== EXTRATOR DE CSV - TESTE ===")
    dados = extrator.processar_todos_arquivos()
    
    if dados:
        extrator.salvar_dados_temporarios(dados)
        
        # Estatísticas básicas
        print("\n=== ESTATÍSTICAS ===")
        df = pd.DataFrame(dados)
        print(f"Total de transações: {len(df)}")
        print(f"Bancos processados: {df['Origem'].unique()}")
        print(f"Períodos encontrados: {df['Mes_Ano'].unique()}")
        print(f"Valor total: R$ {df['Valor'].sum():.2f}")
    else:
        print("Nenhum dado foi processado.")

if __name__ == "__main__":
    main()
