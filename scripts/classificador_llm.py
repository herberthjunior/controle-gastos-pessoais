#!/usr/bin/env python3
"""
Módulo de Classificação com LLM - Sistema de Controle de Gastos Pessoais
Integra o LLM com o banco de dados para classificação automática dos gastos.
"""

import pandas as pd
import time
from typing import List, Dict, Optional, Tuple
from config_llm import ConfigLLM

class ClassificadorLLM:
    def __init__(self, arquivo_bd: str = "../data/gastos.xlsx"):
        self.arquivo_bd = arquivo_bd
        self.config_llm = ConfigLLM()
        self.df_dados = None
        self.estatisticas = {
            'total_processados': 0,
            'classificados_com_sucesso': 0,
            'erros': 0,
            'tempo_total': 0
        }
    
    def inicializar_llm(self) -> bool:
        """
        Inicializa e testa a conexão com o LLM.
        
        Returns:
            True se inicializado com sucesso, False caso contrário.
        """
        print("🤖 Inicializando LLM para classificação...")
        
        if not self.config_llm.configurar_cliente():
            return False
        
        if not self.config_llm.testar_conexao():
            return False
        
        print("✅ LLM inicializado e pronto para classificação")
        return True
    
    def carregar_dados(self) -> bool:
        """
        Carrega os dados do banco de dados.
        
        Returns:
            True se carregado com sucesso, False caso contrário.
        """
        try:
            self.df_dados = pd.read_excel(self.arquivo_bd, engine='openpyxl')
            print(f"📊 Dados carregados: {len(self.df_dados)} registros")
            return True
        except Exception as e:
            print(f"❌ Erro ao carregar dados: {e}")
            return False
    
    def identificar_registros_sem_categoria(self) -> pd.DataFrame:
        """
        Identifica registros que precisam ser classificados.
        
        Returns:
            DataFrame com registros sem categoria
        """
        if self.df_dados is None:
            return pd.DataFrame()
        
        # Identificar registros sem categoria (vazios ou NaN)
        mask = (
            self.df_dados['Categoria'].isna() | 
            (self.df_dados['Categoria'] == '') |
            (self.df_dados['Categoria'] == 'nan')
        )
        
        registros_sem_categoria = self.df_dados[mask].copy()
        
        print(f"🔍 Encontrados {len(registros_sem_categoria)} registros sem categoria")
        
        return registros_sem_categoria
    
    def classificar_lote(self, registros: pd.DataFrame, lote_size: int = 5) -> List[Dict]:
        """
        Classifica um lote de registros usando o LLM.
        
        Args:
            registros: DataFrame com registros para classificar
            lote_size: Tamanho do lote para processamento
            
        Returns:
            Lista de dicionários com resultados da classificação
        """
        resultados = []
        total_registros = len(registros)
        
        print(f"🔄 Iniciando classificação de {total_registros} registros...")
        
        for i in range(0, total_registros, lote_size):
            lote = registros.iloc[i:i+lote_size]
            
            print(f"   Processando lote {i//lote_size + 1}/{(total_registros-1)//lote_size + 1} ({len(lote)} registros)")
            
            for idx, row in lote.iterrows():
                inicio_tempo = time.time()
                
                try:
                    # Classificar usando o LLM
                    categoria = self.config_llm.classificar_gasto(row['Descricao'])
                    
                    if categoria:
                        resultados.append({
                            'index': idx,
                            'descricao': row['Descricao'],
                            'categoria_original': categoria,
                            'categoria_limpa': self.limpar_categoria(categoria),
                            'sucesso': True,
                            'erro': None
                        })
                        self.estatisticas['classificados_com_sucesso'] += 1
                        print(f"      ✅ '{row['Descricao'][:50]}...' → {categoria}")
                    else:
                        resultados.append({
                            'index': idx,
                            'descricao': row['Descricao'],
                            'categoria_original': None,
                            'categoria_limpa': 'Outros',
                            'sucesso': False,
                            'erro': 'Resposta vazia do LLM'
                        })
                        self.estatisticas['erros'] += 1
                        print(f"      ❌ '{row['Descricao'][:50]}...' → Erro: resposta vazia")
                    
                    self.estatisticas['total_processados'] += 1
                    self.estatisticas['tempo_total'] += time.time() - inicio_tempo
                    
                    # Pequena pausa para não sobrecarregar a API
                    time.sleep(0.5)
                    
                except Exception as e:
                    resultados.append({
                        'index': idx,
                        'descricao': row['Descricao'],
                        'categoria_original': None,
                        'categoria_limpa': 'Outros',
                        'sucesso': False,
                        'erro': str(e)
                    })
                    self.estatisticas['erros'] += 1
                    self.estatisticas['total_processados'] += 1
                    print(f"      ❌ '{row['Descricao'][:50]}...' → Erro: {e}")
        
        return resultados
    
    def limpar_categoria(self, categoria: str) -> str:
        """
        Limpa e padroniza a categoria retornada pelo LLM.
        
        Args:
            categoria: Categoria bruta retornada pelo LLM
            
        Returns:
            Categoria limpa e padronizada
        """
        if not categoria:
            return 'Outros'
        
        # Limpar e padronizar
        categoria_limpa = categoria.strip().title()
        
        # Mapear variações para categorias padrão
        mapeamento = {
            'Alimentacao': 'Alimentação',
            'Educacao': 'Educação',
            'Saude': 'Saúde',
            'Servicos': 'Serviços',
            'Investimento': 'Investimentos',
            'Outro': 'Outros',
            'Other': 'Outros'
        }
        
        return mapeamento.get(categoria_limpa, categoria_limpa)
    
    def aplicar_classificacoes(self, resultados: List[Dict]) -> bool:
        """
        Aplica as classificações ao banco de dados.
        
        Args:
            resultados: Lista com resultados da classificação
            
        Returns:
            True se aplicado com sucesso, False caso contrário.
        """
        try:
            print("💾 Aplicando classificações ao banco de dados...")
            
            # Aplicar cada classificação
            for resultado in resultados:
                idx = resultado['index']
                categoria = resultado['categoria_limpa']
                
                # Atualizar a categoria no DataFrame
                self.df_dados.at[idx, 'Categoria'] = categoria
            
            # Salvar o arquivo atualizado
            self.df_dados.to_excel(self.arquivo_bd, index=False, engine='openpyxl')
            
            print(f"✅ {len(resultados)} classificações aplicadas e salvas")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao aplicar classificações: {e}")
            return False
    
    def gerar_relatorio_classificacao(self, resultados: List[Dict]) -> None:
        """
        Gera um relatório detalhado da classificação.
        
        Args:
            resultados: Lista com resultados da classificação
        """
        print("\n" + "="*60)
        print("📊 RELATÓRIO DE CLASSIFICAÇÃO")
        print("="*60)
        
        # Estatísticas gerais
        print(f"Total processados: {self.estatisticas['total_processados']}")
        print(f"Classificados com sucesso: {self.estatisticas['classificados_com_sucesso']}")
        print(f"Erros: {self.estatisticas['erros']}")
        print(f"Taxa de sucesso: {(self.estatisticas['classificados_com_sucesso']/self.estatisticas['total_processados']*100):.1f}%")
        print(f"Tempo total: {self.estatisticas['tempo_total']:.1f}s")
        print(f"Tempo médio por classificação: {(self.estatisticas['tempo_total']/self.estatisticas['total_processados']):.2f}s")
        
        # Distribuição por categoria
        if resultados:
            categorias = {}
            for resultado in resultados:
                if resultado['sucesso']:
                    cat = resultado['categoria_limpa']
                    categorias[cat] = categorias.get(cat, 0) + 1
            
            print(f"\n📈 Distribuição por categoria:")
            for categoria, count in sorted(categorias.items()):
                print(f"   {categoria}: {count}")
        
        # Erros (se houver)
        erros = [r for r in resultados if not r['sucesso']]
        if erros:
            print(f"\n⚠️  Erros encontrados ({len(erros)}):")
            for erro in erros[:5]:  # Mostrar apenas os primeiros 5
                print(f"   '{erro['descricao'][:40]}...' → {erro['erro']}")
            if len(erros) > 5:
                print(f"   ... e mais {len(erros)-5} erros")
        
        print("="*60)
    
    def executar_classificacao_completa(self) -> bool:
        """
        Executa o processo completo de classificação.
        
        Returns:
            True se executado com sucesso, False caso contrário.
        """
        print("🚀 Iniciando processo de classificação completa...")
        
        # Inicializar LLM
        if not self.inicializar_llm():
            return False
        
        # Carregar dados
        if not self.carregar_dados():
            return False
        
        # Identificar registros sem categoria
        registros_sem_categoria = self.identificar_registros_sem_categoria()
        
        if len(registros_sem_categoria) == 0:
            print("✅ Todos os registros já estão classificados!")
            return True
        
        # Classificar registros
        resultados = self.classificar_lote(registros_sem_categoria)
        
        # Aplicar classificações
        if not self.aplicar_classificacoes(resultados):
            return False
        
        # Gerar relatório
        self.gerar_relatorio_classificacao(resultados)
        
        print("\n✅ Processo de classificação concluído com sucesso!")
        return True

def main():
    """Função principal para teste do módulo."""
    classificador = ClassificadorLLM()
    sucesso = classificador.executar_classificacao_completa()
    
    if not sucesso:
        print("❌ Falha no processo de classificação")
        return False
    
    return True

if __name__ == "__main__":
    main()
