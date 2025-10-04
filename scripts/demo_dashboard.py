#!/usr/bin/env python3
"""
Demonstração do Dashboard - Sistema de Controle de Gastos Pessoais
Script para demonstrar as funcionalidades do dashboard sem iniciar o servidor.
"""

import pandas as pd
import os
from datetime import datetime

def demonstrar_funcionalidades():
    """Demonstra as funcionalidades do dashboard."""
    print("=" * 60)
    print("DEMONSTRAÇÃO DO DASHBOARD AVANÇADO")
    print("Sistema de Controle de Gastos Pessoais")
    print("=" * 60)
    
    # Verificar dados
    arquivo_dados = "../data/gastos.xlsx"
    
    if not os.path.exists(arquivo_dados):
        print("❌ Arquivo de dados não encontrado!")
        return False
    
    try:
        df = pd.read_excel(arquivo_dados)
        print(f"✅ Dados carregados: {len(df)} registros")
        
        # Converter data
        df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y', errors='coerce')
        
        # Estatísticas básicas
        print("\n📊 ESTATÍSTICAS BÁSICAS:")
        print(f"   • Total de transações: {len(df):,}")
        print(f"   • Período: {df['Data'].min().strftime('%d/%m/%Y')} a {df['Data'].max().strftime('%d/%m/%Y')}")
        print(f"   • Categorias: {df['Categoria'].nunique()}")
        print(f"   • Bancos: {', '.join(df['Origem'].unique())}")
        
        # Análise de gastos vs receitas
        gastos = df[df['Valor'] > 0]['Valor'].sum()
        receitas = abs(df[df['Valor'] < 0]['Valor'].sum())
        saldo = df['Valor'].sum()
        
        print(f"\n💰 ANÁLISE FINANCEIRA:")
        print(f"   • Total de gastos: R$ {gastos:,.2f}")
        print(f"   • Total de receitas: R$ {receitas:,.2f}")
        print(f"   • Saldo líquido: R$ {saldo:,.2f}")
        
        # Top categorias
        print(f"\n🏆 TOP 5 CATEGORIAS (GASTOS):")
        top_categorias = df[df['Valor'] > 0].groupby('Categoria')['Valor'].sum().sort_values(ascending=False).head(5)
        for i, (categoria, valor) in enumerate(top_categorias.items(), 1):
            print(f"   {i}. {categoria}: R$ {valor:,.2f}")
        
        # Distribuição por banco
        print(f"\n🏦 DISTRIBUIÇÃO POR BANCO:")
        por_banco = df.groupby('Origem').agg({
            'Valor': ['sum', 'count']
        }).round(2)
        for banco in df['Origem'].unique():
            total = df[df['Origem'] == banco]['Valor'].sum()
            count = len(df[df['Origem'] == banco])
            print(f"   • {banco}: R$ {total:,.2f} ({count} transações)")
        
        # Funcionalidades do dashboard
        print(f"\n🚀 FUNCIONALIDADES DO DASHBOARD:")
        print("   ✅ 6 abas interativas de análise")
        print("   ✅ Métricas principais em tempo real")
        print("   ✅ Gráficos interativos (Pizza, Barras, Timeline)")
        print("   ✅ Heatmap de padrões de gastos")
        print("   ✅ Rankings e top gastos")
        print("   ✅ Filtros dinâmicos (categoria, banco, período)")
        print("   ✅ Tabela detalhada com busca")
        print("   ✅ Estatísticas avançadas")
        print("   ✅ Insights automáticos")
        print("   ✅ Comparativo entre bancos")
        print("   ✅ Análise temporal completa")
        
        print(f"\n🎨 RECURSOS VISUAIS:")
        print("   • Interface responsiva e moderna")
        print("   • Tema personalizado com cores otimizadas")
        print("   • Gráficos interativos com hover e zoom")
        print("   • Filtros em tempo real na sidebar")
        print("   • Métricas com indicadores visuais")
        print("   • CSS customizado para melhor UX")
        
        print(f"\n🔧 COMO EXECUTAR:")
        print("   1. Execute: python3 iniciar_dashboard.py")
        print("   2. Ou execute: streamlit run dashboard.py")
        print("   3. Acesse: http://localhost:8501")
        
        print("\n" + "=" * 60)
        print("✅ DASHBOARD PRONTO PARA USO!")
        print("🚀 Execute o comando acima para iniciar a interface web")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao analisar dados: {e}")
        return False

def main():
    """Função principal."""
    sucesso = demonstrar_funcionalidades()
    
    if sucesso:
        print("\n💡 DICA: Para uma experiência completa, execute:")
        print("   python3 iniciar_dashboard.py")
    
    return sucesso

if __name__ == "__main__":
    main()
