#!/usr/bin/env python3
"""
Módulo de Configuração do LLM - Sistema de Controle de Gastos Pessoais
Configura e testa a conexão com Gemini 2.5 Flash via OpenAI client.
"""

import os
from openai import OpenAI
from typing import Optional, Dict, Any

class ConfigLLM:
    def __init__(self):
        self.client = None
        self.modelo = "gpt-4.1-mini"  # Modelo disponível via proxy Manus
        self.configurado = False
    
    def configurar_cliente(self) -> bool:
        """
        Configura o cliente OpenAI para acessar o Gemini via proxy.
        
        Returns:
            True se configurado com sucesso, False caso contrário.
        """
        try:
            # As variáveis de ambiente já estão configuradas
            api_key = os.getenv('OPENAI_API_KEY')
            base_url = os.getenv('OPENAI_BASE_URL')
            
            if not api_key or not base_url:
                print("❌ Configuração da API não encontrada nas variáveis de ambiente")
                return False
            
            # Criar cliente OpenAI configurado para o proxy Manus
            self.client = OpenAI()  # Usa automaticamente as variáveis de ambiente
            
            print("✅ Cliente LLM configurado com sucesso")
            print(f"   Modelo: {self.modelo}")
            print(f"   Endpoint: {base_url}")
            
            self.configurado = True
            return True
            
        except Exception as e:
            print(f"❌ Erro ao configurar cliente: {e}")
            return False
    
    def testar_conexao(self) -> bool:
        """
        Testa a conexão com a API fazendo uma requisição simples.
        
        Returns:
            True se o teste passou, False caso contrário.
        """
        if not self.configurado:
            print("❌ LLM não configurado. Execute configurar_cliente() primeiro.")
            return False
        
        try:
            print("🔄 Testando conexão com a API...")
            
            # Fazer uma requisição simples de teste
            response = self.client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {"role": "user", "content": "Responda apenas: 'Teste OK'"}
                ],
                max_tokens=10,
                temperature=0
            )
            
            if response and response.choices and response.choices[0].message.content:
                resposta = response.choices[0].message.content.strip()
                print(f"✅ Teste de conexão bem-sucedido")
                print(f"   Resposta: {resposta}")
                return True
            else:
                print("❌ Resposta vazia da API")
                return False
                
        except Exception as e:
            print(f"❌ Erro no teste de conexão: {e}")
            return False
    
    def classificar_gasto(self, descricao: str) -> Optional[str]:
        """
        Classifica um gasto usando o LLM.
        
        Args:
            descricao: Descrição do gasto para classificar
            
        Returns:
            Categoria classificada ou None em caso de erro
        """
        if not self.configurado:
            print("❌ LLM não configurado")
            return None
        
        try:
            # Prompt para classificação de gastos
            prompt = f"""Você é um assistente especializado em classificação de gastos pessoais.

Classifique o gasto a seguir em UMA das categorias abaixo:

CATEGORIAS DISPONÍVEIS:
- Alimentação
- Transporte
- Moradia
- Saúde
- Educação
- Lazer
- Compras
- Serviços
- Investimentos
- Outros

DESCRIÇÃO DO GASTO: {descricao}

INSTRUÇÕES:
- Responda APENAS com o nome da categoria
- Use exatamente um dos nomes listados acima
- Não adicione explicações ou comentários

CATEGORIA:"""

            response = self.client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=20,
                temperature=0
            )
            
            if response and response.choices and response.choices[0].message.content:
                categoria = response.choices[0].message.content.strip()
                return categoria
            else:
                return None
                
        except Exception as e:
            print(f"❌ Erro na classificação: {e}")
            return None
    
    def obter_configuracao(self) -> Dict[str, Any]:
        """
        Retorna informações sobre a configuração atual.
        
        Returns:
            Dicionário com informações da configuração
        """
        return {
            'configurado': self.configurado,
            'cliente_inicializado': bool(self.client),
            'modelo': self.modelo,
            'api_key_definida': bool(os.getenv('OPENAI_API_KEY')),
            'base_url': os.getenv('OPENAI_BASE_URL')
        }

def main():
    """Função principal para teste e configuração inicial."""
    print("=== CONFIGURAÇÃO DO LLM (GEMINI 2.5 FLASH) ===")
    
    config = ConfigLLM()
    
    # Configurar cliente
    if not config.configurar_cliente():
        return False
    
    # Testar conexão
    if not config.testar_conexao():
        return False
    
    # Teste de classificação
    print("\n🧪 Testando classificação de gastos...")
    
    exemplos_teste = [
        "APPLE COM BILL SAO PAULO BRA",
        "99Food IFOOD CLUB Osasco BRA", 
        "POSTO SHELL COMBUSTIVEL",
        "FARMACIA DROGA RAIA"
    ]
    
    for exemplo in exemplos_teste:
        categoria = config.classificar_gasto(exemplo)
        print(f"   '{exemplo}' → {categoria}")
    
    # Exibir configuração final
    print("\n📊 Configuração final:")
    info = config.obter_configuracao()
    for chave, valor in info.items():
        print(f"   {chave}: {valor}")
    
    print("\n✅ LLM configurado e pronto para classificação de gastos!")
    return True

if __name__ == "__main__":
    main()
