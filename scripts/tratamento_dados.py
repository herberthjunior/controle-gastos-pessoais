#!/usr/bin/env python3
"""
Módulo de Tratamento e Padronização de Dados - Sistema de Controle de Gastos Pessoais
Integra dados extraídos dos CSVs com o banco de dados principal (gastos.xlsx).
"""

import pandas as pd
import os
from datetime import datetime
from typing import List, Dict, Tuple
import hashlib
from extrator_csv import ExtratorCSV

class TratamentoDados:
    def __init__(self, arquivo_bd: str = "../data/gastos.xlsx"):
        self.arquivo_bd = arquivo_bd
        self.df_atual = None
        self.novos_registros = 0
        self.registros_duplicados = 0
    
    def carregar_banco_dados(self) -> pd.DataFrame:
        """
        Carrega o banco de dados principal. Se não existir, cria um vazio.
        
        Returns:
            DataFrame com os dados atuais
        """
        if os.path.exists(self.arquivo_bd):
            try:
                df = pd.read_excel(self.arquivo_bd, engine='openpyxl')
                print(f"Banco de dados carregado: {len(df)} registros existentes")
                return df
            except Exception as e:
                print(f"Erro ao carregar banco de dados: {e}")
                return self.criar_dataframe_vazio()
        else:
            print("Banco de dados não existe. Criando estrutura vazia.")
            return self.criar_dataframe_vazio()
    
    def criar_dataframe_vazio(self) -> pd.DataFrame:
        """
        Cria um DataFrame vazio com a estrutura padrão.
        
        Returns:
            DataFrame vazio com colunas padronizadas
        """
        colunas = [
            'Data', 'Descricao', 'Valor', 'Categoria', 'Subcategoria', 
            'Mes_Ano', 'Observacoes', 'Origem', 'Hash_ID', 'Data_Processamento'
        ]
        return pd.DataFrame(columns=colunas)
    
    def gerar_hash_transacao(self, data: str, descricao: str, valor: float, origem: str) -> str:
        """
        Gera um hash único para identificar transações duplicadas.
        
        Args:
            data: Data da transação
            descricao: Descrição da transação
            valor: Valor da transação
            origem: Banco de origem
            
        Returns:
            String hash MD5 para identificação única
        """
        # Normalizar dados para hash consistente
        data_norm = str(data).strip()
        descricao_norm = str(descricao).strip().upper()
        valor_norm = f"{float(valor):.2f}"
        origem_norm = str(origem).strip().upper()
        
        # Criar string única
        string_unica = f"{data_norm}|{descricao_norm}|{valor_norm}|{origem_norm}"
        
        # Gerar hash MD5
        return hashlib.md5(string_unica.encode('utf-8')).hexdigest()
    
    def adicionar_campos_controle(self, dados: List[Dict]) -> List[Dict]:
        """
        Adiciona campos de controle aos dados (Hash_ID, Data_Processamento).
        
        Args:
            dados: Lista de dicionários com os dados
            
        Returns:
            Lista atualizada com campos de controle
        """
        data_processamento = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        for registro in dados:
            # Gerar hash único
            hash_id = self.gerar_hash_transacao(
                registro['Data'],
                registro['Descricao'],
                registro['Valor'],
                registro['Origem']
            )
            
            # Adicionar campos de controle
            registro['Hash_ID'] = hash_id
            registro['Data_Processamento'] = data_processamento
        
        return dados
    
    def identificar_duplicatas(self, novos_dados: List[Dict], df_existente: pd.DataFrame) -> Tuple[List[Dict], List[Dict]]:
        """
        Identifica registros novos e duplicatas baseado no Hash_ID.
        
        Args:
            novos_dados: Lista com novos dados a serem inseridos
            df_existente: DataFrame com dados já existentes
            
        Returns:
            Tupla (registros_novos, registros_duplicados)
        """
        # Obter hashes existentes
        hashes_existentes = set()
        if not df_existente.empty and 'Hash_ID' in df_existente.columns:
            hashes_existentes = set(df_existente['Hash_ID'].tolist())
        
        registros_novos = []
        registros_duplicados = []
        
        for registro in novos_dados:
            if registro['Hash_ID'] in hashes_existentes:
                registros_duplicados.append(registro)
            else:
                registros_novos.append(registro)
        
        return registros_novos, registros_duplicados
    
    def validar_dados(self, dados: List[Dict]) -> List[Dict]:
        """
        Valida e limpa os dados antes da inserção.
        
        Args:
            dados: Lista de dados para validação
            
        Returns:
            Lista de dados validados
        """
        dados_validos = []
        
        for registro in dados:
            # Validações básicas
            try:
                # Verificar se data está no formato correto
                data_str = str(registro['Data'])
                if len(data_str.split('/')) != 3:
                    print(f"Data inválida ignorada: {data_str}")
                    continue
                
                # Verificar se valor é numérico
                valor = float(registro['Valor'])
                registro['Valor'] = valor
                
                # Limpar descrição
                registro['Descricao'] = str(registro['Descricao']).strip()
                
                # Garantir que campos obrigatórios não estão vazios
                if not registro['Descricao'] or registro['Descricao'] == 'nan':
                    print(f"Descrição vazia ignorada para valor {valor}")
                    continue
                
                dados_validos.append(registro)
                
            except Exception as e:
                print(f"Erro na validação de registro: {e}")
                continue
        
        return dados_validos
    
    def integrar_novos_dados(self, novos_dados: List[Dict]) -> Dict:
        """
        Integra novos dados ao banco de dados principal.
        
        Args:
            novos_dados: Lista de novos dados para integração
            
        Returns:
            Dicionário com estatísticas do processamento
        """
        # Carregar banco atual
        self.df_atual = self.carregar_banco_dados()
        
        # Adicionar campos de controle
        novos_dados = self.adicionar_campos_controle(novos_dados)
        
        # Validar dados
        novos_dados = self.validar_dados(novos_dados)
        
        # Identificar duplicatas
        registros_novos, registros_duplicados = self.identificar_duplicatas(novos_dados, self.df_atual)
        
        # Estatísticas
        stats = {
            'total_processados': len(novos_dados),
            'novos_inseridos': len(registros_novos),
            'duplicatas_ignoradas': len(registros_duplicados),
            'total_final': len(self.df_atual) + len(registros_novos)
        }
        
        # Inserir apenas registros novos
        if registros_novos:
            df_novos = pd.DataFrame(registros_novos)
            
            # Combinar com dados existentes
            if self.df_atual.empty:
                self.df_atual = df_novos
            else:
                self.df_atual = pd.concat([self.df_atual, df_novos], ignore_index=True)
            
            # Salvar banco atualizado
            self.salvar_banco_dados()
            
            print(f"✅ {len(registros_novos)} novos registros inseridos")
        else:
            print("ℹ️  Nenhum registro novo para inserir")
        
        if registros_duplicados:
            print(f"⚠️  {len(registros_duplicados)} duplicatas ignoradas")
        
        return stats
    
    def salvar_banco_dados(self):
        """Salva o banco de dados atualizado."""
        try:
            self.df_atual.to_excel(self.arquivo_bd, index=False, engine='openpyxl')
            print(f"💾 Banco de dados salvo: {self.arquivo_bd}")
        except Exception as e:
            print(f"❌ Erro ao salvar banco de dados: {e}")
    
    def obter_estatisticas(self) -> Dict:
        """
        Obtém estatísticas do banco de dados atual.
        
        Returns:
            Dicionário com estatísticas
        """
        if self.df_atual is None or self.df_atual.empty:
            return {'total_registros': 0}
        
        stats = {
            'total_registros': len(self.df_atual),
            'valor_total': self.df_atual['Valor'].sum(),
            'bancos': self.df_atual['Origem'].value_counts().to_dict(),
            'periodos': sorted(self.df_atual['Mes_Ano'].unique().tolist()),
            'registros_sem_categoria': len(self.df_atual[self.df_atual['Categoria'].isna() | (self.df_atual['Categoria'] == '')])
        }
        
        return stats

def main():
    """Função principal para teste do módulo."""
    print("=== TRATAMENTO E INTEGRAÇÃO DE DADOS - TESTE ===")
    
    # Extrair dados dos CSVs
    extrator = ExtratorCSV()
    dados_extraidos = extrator.processar_todos_arquivos()
    
    if not dados_extraidos:
        print("❌ Nenhum dado extraído para processar")
        return
    
    # Processar e integrar dados
    tratamento = TratamentoDados()
    stats = tratamento.integrar_novos_dados(dados_extraidos)
    
    # Exibir estatísticas
    print("\n=== ESTATÍSTICAS DE PROCESSAMENTO ===")
    for chave, valor in stats.items():
        print(f"{chave}: {valor}")
    
    # Estatísticas do banco final
    print("\n=== ESTATÍSTICAS DO BANCO DE DADOS ===")
    stats_bd = tratamento.obter_estatisticas()
    for chave, valor in stats_bd.items():
        if isinstance(valor, dict):
            print(f"{chave}:")
            for sub_chave, sub_valor in valor.items():
                print(f"  {sub_chave}: {sub_valor}")
        else:
            print(f"{chave}: {valor}")

if __name__ == "__main__":
    main()
