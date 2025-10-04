#!/usr/bin/env python3
"""
Integração com Google Drive - Sistema de Controle de Gastos Pessoais
Permite baixar arquivos de uma pasta compartilhada do Google Drive.
"""

import os
import requests
import re
from typing import List, Dict, Optional
from datetime import datetime

class GoogleDriveIntegration:
    def __init__(self, folder_id: Optional[str] = None):
        """
        Inicializa a integração com Google Drive.
        
        Args:
            folder_id: ID da pasta compartilhada do Google Drive
        """
        self.folder_id = folder_id or self.obter_folder_id_config()
        self.pasta_local = "../faturas"
        self.arquivos_baixados = []
    
    def obter_folder_id_config(self) -> Optional[str]:
        """Obtém o folder ID do arquivo de configuração."""
        config_file = "config_google_drive.py"
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Procurar por GOOGLE_DRIVE_FOLDER_ID
                    match = re.search(r'GOOGLE_DRIVE_FOLDER_ID\s*=\s*["\']([^"\']+)["\']', content)
                    if match:
                        return match.group(1)
            except Exception as e:
                print(f"Erro ao ler configuração: {e}")
        
        return None
    
    def criar_config_exemplo(self):
        """Cria arquivo de configuração de exemplo."""
        config_content = '''#!/usr/bin/env python3
"""
Configuração do Google Drive - Sistema de Controle de Gastos Pessoais
"""

# ID da pasta compartilhada do Google Drive
# Para obter o ID:
# 1. Abra a pasta no Google Drive
# 2. Copie o ID da URL: https://drive.google.com/drive/folders/SEU_FOLDER_ID_AQUI
GOOGLE_DRIVE_FOLDER_ID = "SEU_FOLDER_ID_AQUI"

# Exemplo:
# GOOGLE_DRIVE_FOLDER_ID = "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
'''
        
        with open("config_google_drive.py", 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        print("✅ Arquivo config_google_drive.py criado!")
        print("📝 Edite o arquivo e adicione o ID da sua pasta do Google Drive")
    
    def obter_url_download_direto(self, file_id: str) -> str:
        """Converte file ID para URL de download direto."""
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    
    def extrair_file_id_da_url(self, url: str) -> Optional[str]:
        """Extrai file ID de uma URL do Google Drive."""
        patterns = [
            r'/file/d/([a-zA-Z0-9-_]+)',
            r'id=([a-zA-Z0-9-_]+)',
            r'/open\?id=([a-zA-Z0-9-_]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def listar_arquivos_pasta(self) -> List[Dict]:
        """
        Lista arquivos CSV na pasta do Google Drive.
        
        Nota: Esta é uma implementação simplificada que requer URLs diretas.
        Para uma implementação completa, seria necessário usar a Google Drive API.
        """
        print("📁 Para usar a integração com Google Drive:")
        print("1. Compartilhe sua pasta do Google Drive com acesso público")
        print("2. Configure o FOLDER_ID no arquivo config_google_drive.py")
        print("3. Ou forneça URLs diretas dos arquivos")
        
        return []
    
    def baixar_arquivo_por_url(self, url: str, nome_arquivo: str) -> bool:
        """Baixa um arquivo específico por URL."""
        try:
            # Extrair file ID se for URL do Google Drive
            file_id = self.extrair_file_id_da_url(url)
            if file_id:
                url = self.obter_url_download_direto(file_id)
            
            print(f"📥 Baixando: {nome_arquivo}")
            
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # Garantir que a pasta existe
            os.makedirs(self.pasta_local, exist_ok=True)
            
            # Salvar arquivo
            caminho_arquivo = os.path.join(self.pasta_local, nome_arquivo)
            with open(caminho_arquivo, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            self.arquivos_baixados.append(caminho_arquivo)
            print(f"✅ Arquivo salvo: {caminho_arquivo}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao baixar {nome_arquivo}: {e}")
            return False
    
    def baixar_arquivos_por_lista(self, urls_arquivos: List[Dict[str, str]]) -> int:
        """
        Baixa arquivos a partir de uma lista de URLs.
        
        Args:
            urls_arquivos: Lista de dicts com 'url' e 'nome'
        
        Returns:
            Número de arquivos baixados com sucesso
        """
        sucessos = 0
        
        print(f"🚀 Iniciando download de {len(urls_arquivos)} arquivos...")
        
        for item in urls_arquivos:
            url = item.get('url', '')
            nome = item.get('nome', f'arquivo_{sucessos + 1}.csv')
            
            if self.baixar_arquivo_por_url(url, nome):
                sucessos += 1
        
        print(f"✅ {sucessos}/{len(urls_arquivos)} arquivos baixados com sucesso")
        return sucessos
    
    def gerar_relatorio_download(self) -> Dict:
        """Gera relatório dos downloads realizados."""
        return {
            'timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            'arquivos_baixados': len(self.arquivos_baixados),
            'lista_arquivos': [os.path.basename(arq) for arq in self.arquivos_baixados],
            'pasta_destino': self.pasta_local
        }

def exemplo_uso_google_drive():
    """Exemplo de como usar a integração com Google Drive."""
    print("=" * 60)
    print("EXEMPLO DE USO - INTEGRAÇÃO GOOGLE DRIVE")
    print("=" * 60)
    
    # Inicializar integração
    gd = GoogleDriveIntegration()
    
    # Verificar se existe configuração
    if not gd.folder_id or gd.folder_id == "SEU_FOLDER_ID_AQUI":
        print("⚠️  Configuração do Google Drive não encontrada")
        gd.criar_config_exemplo()
        return
    
    print(f"📁 Pasta configurada: {gd.folder_id}")
    
    # Exemplo com URLs diretas (método recomendado para simplicidade)
    urls_exemplo = [
        {
            'url': 'https://drive.google.com/file/d/EXEMPLO_FILE_ID_1/view',
            'nome': 'fatura-inter-2025-11.csv'
        },
        {
            'url': 'https://drive.google.com/file/d/EXEMPLO_FILE_ID_2/view',
            'nome': 'Fatura_2025-11-15.csv'
        }
    ]
    
    print("\n📋 Para usar com seus arquivos:")
    print("1. Faça upload dos CSVs para uma pasta no Google Drive")
    print("2. Compartilhe cada arquivo com acesso público")
    print("3. Copie as URLs dos arquivos")
    print("4. Use o método baixar_arquivos_por_lista()")
    
    # Gerar relatório
    relatorio = gd.gerar_relatorio_download()
    print(f"\n📊 Relatório: {relatorio}")

def main():
    """Função principal para teste."""
    exemplo_uso_google_drive()

if __name__ == "__main__":
    main()
