#!/usr/bin/env python3
"""
Script Principal - Sistema de Controle de Gastos Pessoais
Orquestra a extração, tratamento e classificação automática de dados das faturas CSV.
"""

import os
import sys
from datetime import datetime
from extrator_csv import ExtratorCSV
from tratamento_dados import TratamentoDados
from classificador_llm import ClassificadorLLM

def main():
    """
    Função principal que executa todo o processo de ETL + Classificação.
    """
    print("=" * 60)
    print("SISTEMA DE CONTROLE DE GASTOS PESSOAIS")
    print("Processamento Completo de Faturas - Versão 2.0")
    print("=" * 60)
    print(f"Iniciado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    try:
        # Etapa 1: Extração de dados dos CSVs
        print("📁 ETAPA 1: Extração de dados dos arquivos CSV")
        print("-" * 50)
        
        extrator = ExtratorCSV()
        dados_extraidos = extrator.processar_todos_arquivos()
        
        if not dados_extraidos:
            print("❌ Nenhum arquivo CSV encontrado para processar.")
            print("   Verifique se existem arquivos na pasta 'faturas/'")
            return False
        
        print(f"✅ {len(dados_extraidos)} transações extraídas com sucesso")
        print()
        
        # Etapa 2: Tratamento e integração dos dados
        print("🔄 ETAPA 2: Tratamento e integração dos dados")
        print("-" * 50)
        
        tratamento = TratamentoDados()
        stats = tratamento.integrar_novos_dados(dados_extraidos)
        
        print()
        
        # Etapa 3: Classificação automática com LLM
        print("🤖 ETAPA 3: Classificação automática com LLM")
        print("-" * 50)
        
        classificador = ClassificadorLLM()
        
        # Verificar se há registros para classificar
        classificador.carregar_dados()
        registros_sem_categoria = classificador.identificar_registros_sem_categoria()
        
        if len(registros_sem_categoria) > 0:
            print(f"Encontrados {len(registros_sem_categoria)} registros para classificar...")
            sucesso_classificacao = classificador.executar_classificacao_completa()
            
            if not sucesso_classificacao:
                print("⚠️  Falha na classificação, mas dados foram processados")
        else:
            print("✅ Todos os registros já estão classificados!")
        
        print()
        
        # Etapa 4: Relatório final
        print("📊 ETAPA 4: Relatório final de processamento")
        print("-" * 50)
        
        print(f"Total processado: {stats['total_processados']} transações")
        print(f"Novos registros: {stats['novos_inseridos']}")
        print(f"Duplicatas ignoradas: {stats['duplicatas_ignoradas']}")
        print(f"Total no banco: {stats['total_final']} registros")
        
        # Estatísticas detalhadas do banco final
        stats_bd = tratamento.obter_estatisticas()
        
        print(f"\n💰 Valor total: R$ {stats_bd['valor_total']:.2f}")
        print(f"🏦 Bancos: {', '.join(stats_bd['bancos'].keys())}")
        print(f"📅 Períodos: {', '.join(stats_bd['periodos'])}")
        print(f"🏷️  Registros sem categoria: {stats_bd['registros_sem_categoria']}")
        
        # Se todos estão classificados, mostrar distribuição
        if stats_bd['registros_sem_categoria'] == 0:
            print("\n🎯 Distribuição por categoria:")
            # Recarregar dados para pegar as classificações
            classificador.carregar_dados()
            if classificador.df_dados is not None:
                categorias = classificador.df_dados['Categoria'].value_counts()
                for cat, count in categorias.head(5).items():
                    valor_cat = classificador.df_dados[classificador.df_dados['Categoria'] == cat]['Valor'].sum()
                    print(f"   {cat}: {count} registros (R$ {valor_cat:.2f})")
        
        print()
        print("=" * 60)
        print("✅ PROCESSAMENTO COMPLETO CONCLUÍDO COM SUCESSO!")
        print("🚀 PRÓXIMO PASSO: Dashboard interativo")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ ERRO DURANTE O PROCESSAMENTO: {e}")
        print("=" * 60)
        return False

if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1)
