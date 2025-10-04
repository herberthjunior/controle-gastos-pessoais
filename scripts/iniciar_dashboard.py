#!/usr/bin/env python3
"""
Script de Inicialização do Dashboard - Sistema de Controle de Gastos Pessoais
Inicia o dashboard web de forma conveniente.
"""

import os
import sys
import subprocess
from datetime import datetime

def verificar_dados():
    """Verifica se os dados estão disponíveis."""
    arquivo_dados = "../data/gastos.xlsx"
    
    if not os.path.exists(arquivo_dados):
        print("❌ Arquivo de dados não encontrado!")
        print("   Execute primeiro: python3 processar_faturas.py")
        return False
    
    try:
        import pandas as pd
        df = pd.read_excel(arquivo_dados)
        
        if df.empty:
            print("❌ Arquivo de dados está vazio!")
            return False
        
        print(f"✅ Dados encontrados: {len(df)} registros")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar dados: {e}")
        return False

def verificar_dependencias():
    """Verifica se as dependências estão instaladas."""
    dependencias = ['streamlit', 'plotly', 'pandas']
    
    for dep in dependencias:
        try:
            __import__(dep)
        except ImportError:
            print(f"❌ Dependência não encontrada: {dep}")
            print(f"   Instale com: pip3 install {dep}")
            return False
    
    print("✅ Todas as dependências estão instaladas")
    return True

def iniciar_dashboard():
    """Inicia o dashboard Streamlit."""
    print("=" * 60)
    print("DASHBOARD DE CONTROLE DE GASTOS PESSOAIS")
    print("Inicializando servidor web...")
    print("=" * 60)
    print(f"Iniciado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    # Verificar dependências
    if not verificar_dependencias():
        return False
    
    # Verificar dados
    if not verificar_dados():
        return False
    
    print("🚀 Iniciando dashboard...")
    print("📊 O dashboard será aberto automaticamente no seu navegador")
    print("🔗 URLs de acesso:")
    print("   - Local: http://localhost:8501")
    print("   - Rede: http://169.254.0.21:8501")
    print()
    print("💡 Para parar o servidor, pressione Ctrl+C")
    print("=" * 60)
    
    try:
        # Iniciar Streamlit
        cmd = [
            sys.executable, "-m", "streamlit", "run", "dashboard.py",
            "--server.headless", "false",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false"
        ]
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n🛑 Dashboard interrompido pelo usuário")
        print("✅ Servidor finalizado com sucesso")
        return True
    except Exception as e:
        print(f"❌ Erro ao iniciar dashboard: {e}")
        return False

def main():
    """Função principal."""
    sucesso = iniciar_dashboard()
    sys.exit(0 if sucesso else 1)

if __name__ == "__main__":
    main()
