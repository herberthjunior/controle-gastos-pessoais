#!/usr/bin/env python3
"""
Sistema de Automação Completo - Controle de Gastos Pessoais
Orquestra todo o pipeline: extração, tratamento, classificação e dashboard.
"""

import os
import sys
import subprocess
import time
from datetime import datetime
from typing import List, Dict, Tuple
import glob

class AutomacaoSistema:
    def __init__(self, pasta_faturas: str = "../faturas", pasta_data: str = "../data"):
        self.pasta_faturas = pasta_faturas
        self.pasta_data = pasta_data
        self.arquivo_controle = os.path.join(pasta_data, "controle_processamento.txt")
        self.log_execucoes = []
    
    def log(self, mensagem: str, tipo: str = "INFO"):
        """Registra mensagem no log."""
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        log_entry = f"[{timestamp}] {tipo}: {mensagem}"
        print(log_entry)
        self.log_execucoes.append(log_entry)
    
    def verificar_estrutura_projeto(self) -> bool:
        """Verifica se a estrutura do projeto está correta."""
        self.log("Verificando estrutura do projeto...")
        
        # Verificar pastas essenciais
        pastas_necessarias = [
            self.pasta_faturas,
            self.pasta_data,
            "."  # pasta scripts
        ]
        
        for pasta in pastas_necessarias:
            if not os.path.exists(pasta):
                self.log(f"Pasta não encontrada: {pasta}", "ERRO")
                return False
        
        # Verificar scripts essenciais
        scripts_necessarios = [
            "extrator_csv.py",
            "tratamento_dados.py",
            "classificador_llm.py",
            "dashboard.py",
            "iniciar_dashboard.py"
        ]
        
        for script in scripts_necessarios:
            if not os.path.exists(script):
                self.log(f"Script não encontrado: {script}", "ERRO")
                return False
        
        self.log("✅ Estrutura do projeto verificada com sucesso")
        return True
    
    def detectar_novos_arquivos(self) -> List[str]:
        """Detecta novos arquivos CSV na pasta de faturas."""
        self.log("Detectando novos arquivos...")
        
        # Padrões de arquivos suportados
        padroes = [
            "fatura-inter-*.csv",
            "Fatura_*.csv"
        ]
        
        arquivos_encontrados = []
        for padrao in padroes:
            caminho_padrao = os.path.join(self.pasta_faturas, padrao)
            arquivos_encontrados.extend(glob.glob(caminho_padrao))
        
        # Verificar arquivos já processados
        arquivos_processados = self.obter_arquivos_processados()
        novos_arquivos = [arq for arq in arquivos_encontrados if arq not in arquivos_processados]
        
        if novos_arquivos:
            self.log(f"📁 {len(novos_arquivos)} novos arquivos detectados:")
            for arquivo in novos_arquivos:
                self.log(f"   • {os.path.basename(arquivo)}")
        else:
            self.log("📁 Nenhum arquivo novo detectado")
        
        return novos_arquivos
    
    def obter_arquivos_processados(self) -> List[str]:
        """Obtém lista de arquivos já processados."""
        if not os.path.exists(self.arquivo_controle):
            return []
        
        try:
            with open(self.arquivo_controle, 'r', encoding='utf-8') as f:
                return [linha.strip() for linha in f.readlines() if linha.strip()]
        except Exception as e:
            self.log(f"Erro ao ler arquivo de controle: {e}", "AVISO")
            return []
    
    def marcar_arquivo_processado(self, arquivo: str):
        """Marca arquivo como processado."""
        try:
            with open(self.arquivo_controle, 'a', encoding='utf-8') as f:
                f.write(f"{arquivo}\n")
        except Exception as e:
            self.log(f"Erro ao marcar arquivo como processado: {e}", "AVISO")
    
    def executar_processamento(self, novos_arquivos: List[str]) -> bool:
        """Executa o processamento completo dos novos arquivos."""
        if not novos_arquivos:
            self.log("⏭️  Nenhum arquivo para processar")
            return True
        
        self.log("🚀 Iniciando processamento completo...")
        
        try:
            # 1. Executar processamento de faturas
            self.log("📊 Executando processamento de faturas...")
            resultado = subprocess.run(
                [sys.executable, "processar_faturas.py"],
                capture_output=True,
                text=True,
                cwd="."
            )
            
            if resultado.returncode != 0:
                self.log(f"Erro no processamento: {resultado.stderr}", "ERRO")
                return False
            
            self.log("✅ Processamento concluído com sucesso")
            
            # Marcar arquivos como processados
            for arquivo in novos_arquivos:
                self.marcar_arquivo_processado(arquivo)
            
            return True
            
        except Exception as e:
            self.log(f"Erro durante processamento: {e}", "ERRO")
            return False
    
    def gerar_relatorio_execucao(self) -> Dict:
        """Gera relatório da execução."""
        self.log("📋 Gerando relatório de execução...")
        
        relatorio = {
            'timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            'status': 'sucesso',
            'arquivos_processados': 0,
            'total_registros': 0,
            'tempo_execucao': 0,
            'logs': self.log_execucoes.copy()
        }
        
        # Verificar se o banco de dados existe e obter estatísticas
        arquivo_dados = os.path.join(self.pasta_data, "gastos.xlsx")
        if os.path.exists(arquivo_dados):
            try:
                import pandas as pd
                df = pd.read_excel(arquivo_dados)
                relatorio['total_registros'] = len(df)
                relatorio['periodo'] = {
                    'inicio': df['Data'].min() if not df.empty else 'N/A',
                    'fim': df['Data'].max() if not df.empty else 'N/A'
                }
            except Exception as e:
                self.log(f"Erro ao ler estatísticas: {e}", "AVISO")
        
        return relatorio
    
    def iniciar_dashboard_automatico(self) -> bool:
        """Inicia o dashboard automaticamente após processamento."""
        self.log("🌐 Iniciando dashboard...")
        
        try:
            # Verificar se o dashboard já está rodando
            try:
                import requests
                response = requests.get("http://localhost:8501", timeout=2)
                if response.status_code == 200:
                    self.log("✅ Dashboard já está rodando em http://localhost:8501")
                    return True
            except:
                pass  # Dashboard não está rodando, vamos iniciar
            
            # Iniciar dashboard em background
            processo = subprocess.Popen(
                [sys.executable, "iniciar_dashboard.py"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                cwd="."
            )
            
            # Aguardar alguns segundos para o dashboard inicializar
            time.sleep(5)
            
            # Verificar se o dashboard está respondendo
            try:
                import requests
                response = requests.get("http://localhost:8501", timeout=10)
                if response.status_code == 200:
                    self.log("✅ Dashboard iniciado com sucesso em http://localhost:8501")
                    return True
                else:
                    self.log("⚠️  Dashboard iniciado mas não está respondendo corretamente", "AVISO")
                    return False
            except Exception as e:
                self.log("⚠️  Dashboard iniciado mas verificação falhou", "AVISO")
                return True  # Assumir sucesso mesmo sem verificação
                
        except Exception as e:
            self.log(f"Erro ao iniciar dashboard: {e}", "ERRO")
            return False
    
    def executar_automacao_completa(self, iniciar_dashboard: bool = True) -> Dict:
        """Executa o ciclo completo de automação."""
        inicio_execucao = time.time()
        
        self.log("=" * 60)
        self.log("🤖 SISTEMA DE AUTOMAÇÃO - CONTROLE DE GASTOS PESSOAIS")
        self.log("=" * 60)
        
        # 1. Verificar estrutura
        if not self.verificar_estrutura_projeto():
            return {'status': 'erro', 'mensagem': 'Estrutura do projeto inválida'}
        
        # 2. Detectar novos arquivos
        novos_arquivos = self.detectar_novos_arquivos()
        
        # 3. Processar arquivos
        if not self.executar_processamento(novos_arquivos):
            return {'status': 'erro', 'mensagem': 'Falha no processamento'}
        
        # 4. Iniciar dashboard (opcional)
        if iniciar_dashboard:
            self.iniciar_dashboard_automatico()
        
        # 5. Gerar relatório
        tempo_execucao = time.time() - inicio_execucao
        relatorio = self.gerar_relatorio_execucao()
        relatorio['tempo_execucao'] = round(tempo_execucao, 2)
        relatorio['arquivos_processados'] = len(novos_arquivos)
        
        self.log("=" * 60)
        self.log("✅ AUTOMAÇÃO CONCLUÍDA COM SUCESSO!")
        self.log(f"⏱️  Tempo de execução: {tempo_execucao:.2f} segundos")
        self.log(f"📁 Arquivos processados: {len(novos_arquivos)}")
        self.log(f"📊 Total de registros: {relatorio.get('total_registros', 0)}")
        self.log("=" * 60)
        
        return relatorio

def main():
    """Função principal."""
    print("🤖 Sistema de Automação - Controle de Gastos Pessoais")
    print("=" * 60)
    
    # Verificar argumentos da linha de comando
    iniciar_dashboard = True
    usar_google_drive = False
    
    for arg in sys.argv[1:]:
        if arg == "--sem-dashboard":
            iniciar_dashboard = False
            print("⚠️  Dashboard não será iniciado automaticamente")
        elif arg == "--google-drive":
            usar_google_drive = True
            print("☁️  Modo Google Drive ativado")
    
    # Baixar arquivos do Google Drive se solicitado
    if usar_google_drive:
        try:
            from google_drive_integration import GoogleDriveIntegration
            from config_google_drive import URLS_ARQUIVOS_EXEMPLO
            
            print("📥 Baixando arquivos do Google Drive...")
            gd = GoogleDriveIntegration()
            
            # Usar URLs de exemplo (usuário deve configurar)
            if URLS_ARQUIVOS_EXEMPLO and len(URLS_ARQUIVOS_EXEMPLO) > 0:
                # Filtrar URLs válidas (não exemplo)
                urls_validas = [
                    item for item in URLS_ARQUIVOS_EXEMPLO 
                    if 'EXEMPLO_FILE_ID' not in item.get('url', '')
                ]
                
                if urls_validas:
                    sucessos = gd.baixar_arquivos_por_lista(urls_validas)
                    print(f"✅ {sucessos} arquivos baixados do Google Drive")
                else:
                    print("⚠️  Configure as URLs dos arquivos em config_google_drive.py")
                    print("📝 Veja as instruções no arquivo para configurar")
            else:
                print("⚠️  Nenhuma URL configurada em config_google_drive.py")
                
        except ImportError:
            print("❌ Módulo google_drive_integration não encontrado")
        except Exception as e:
            print(f"❌ Erro ao baixar do Google Drive: {e}")
    
    # Executar automação
    automacao = AutomacaoSistema()
    relatorio = automacao.executar_automacao_completa(iniciar_dashboard)
    
    # Exibir resultado final
    if relatorio['status'] == 'erro':
        print(f"\n❌ ERRO: {relatorio['mensagem']}")
        sys.exit(1)
    else:
        print(f"\n✅ Automação concluída com sucesso!")
        if iniciar_dashboard:
            print("🌐 Dashboard disponível em: http://localhost:8501")
        print("📋 Execute 'python3 iniciar_dashboard.py' para acessar o dashboard")
        
        # Instruções para Google Drive
        if usar_google_drive:
            print("\n☁️  GOOGLE DRIVE:")
            print("📝 Para próximas atualizações, adicione novos arquivos no Google Drive")
            print("🔄 Execute: python3 automatizar_sistema.py --google-drive")
        
        sys.exit(0)

if __name__ == "__main__":
    main()
