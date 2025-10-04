#!/usr/bin/env python3
"""
Módulo de Insights com LLM - Sistema de Controle de Gastos Pessoais
Gera análises inteligentes e recomendações usando LLM.
"""

import pandas as pd
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from config_llm import ConfigLLM

class InsightsLLM:
    def __init__(self, arquivo_dados: str = "../data/gastos.xlsx"):
        self.arquivo_dados = arquivo_dados
        self.config_llm = ConfigLLM()
        self.df = None
        self.insights_cache = {}
    
    def inicializar_llm(self) -> bool:
        """Inicializa o LLM para geração de insights."""
        return self.config_llm.configurar_cliente()
    
    def carregar_dados(self) -> bool:
        """Carrega os dados financeiros."""
        try:
            self.df = pd.read_excel(self.arquivo_dados, engine='openpyxl')
            self.df['Data'] = pd.to_datetime(self.df['Data'], format='%d/%m/%Y', errors='coerce')
            return True
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            return False
    
    def preparar_resumo_dados(self) -> Dict:
        """Prepara um resumo dos dados para o LLM."""
        if self.df is None or self.df.empty:
            return {}
        
        # Separar gastos e receitas
        gastos = self.df[self.df['Valor'] > 0]
        receitas = self.df[self.df['Valor'] < 0]
        
        # Estatísticas básicas
        resumo = {
            'periodo': {
                'inicio': self.df['Data'].min().strftime('%d/%m/%Y'),
                'fim': self.df['Data'].max().strftime('%d/%m/%Y'),
                'dias': (self.df['Data'].max() - self.df['Data'].min()).days
            },
            'totais': {
                'gastos': float(gastos['Valor'].sum()),
                'receitas': float(abs(receitas['Valor'].sum())),
                'saldo': float(self.df['Valor'].sum()),
                'transacoes': len(self.df)
            },
            'categorias': {
                'gastos_por_categoria': gastos.groupby('Categoria')['Valor'].sum().to_dict(),
                'quantidade_por_categoria': gastos.groupby('Categoria').size().to_dict()
            },
            'bancos': {
                'gastos_por_banco': self.df.groupby('Origem')['Valor'].sum().to_dict(),
                'transacoes_por_banco': self.df.groupby('Origem').size().to_dict()
            },
            'padroes': {
                'ticket_medio': float(gastos['Valor'].mean()) if not gastos.empty else 0,
                'maior_gasto': float(gastos['Valor'].max()) if not gastos.empty else 0,
                'categoria_principal': gastos.groupby('Categoria')['Valor'].sum().idxmax() if not gastos.empty else 'N/A'
            }
        }
        
        return resumo
    
    def gerar_insight_geral(self) -> str:
        """Gera insight geral sobre os gastos."""
        if not self.inicializar_llm():
            return "Erro ao conectar com o sistema de análise."
        
        resumo = self.preparar_resumo_dados()
        if not resumo:
            return "Dados insuficientes para análise."
        
        prompt = f"""Você é um consultor financeiro especializado em análise de gastos pessoais.

Analise os dados financeiros abaixo e forneça insights valiosos e recomendações práticas:

DADOS FINANCEIROS:
- Período: {resumo['periodo']['inicio']} a {resumo['periodo']['fim']} ({resumo['periodo']['dias']} dias)
- Total de gastos: R$ {resumo['totais']['gastos']:,.2f}
- Total de receitas: R$ {resumo['totais']['receitas']:,.2f}
- Saldo líquido: R$ {resumo['totais']['saldo']:,.2f}
- Transações: {resumo['totais']['transacoes']}

GASTOS POR CATEGORIA:
{json.dumps(resumo['categorias']['gastos_por_categoria'], indent=2, ensure_ascii=False)}

DISTRIBUIÇÃO POR BANCO:
{json.dumps(resumo['bancos']['gastos_por_banco'], indent=2, ensure_ascii=False)}

PADRÕES:
- Ticket médio: R$ {resumo['padroes']['ticket_medio']:,.2f}
- Maior gasto: R$ {resumo['padroes']['maior_gasto']:,.2f}
- Categoria principal: {resumo['padroes']['categoria_principal']}

INSTRUÇÕES:
1. Forneça uma análise clara e objetiva da situação financeira
2. Identifique padrões importantes nos gastos
3. Destaque pontos de atenção ou oportunidades de economia
4. Dê recomendações práticas e específicas
5. Use linguagem acessível e evite jargões técnicos
6. Seja positivo mas realista

Responda em português brasileiro, de forma estruturada e profissional."""

        try:
            response = self.config_llm.client.chat.completions.create(
                model=self.config_llm.modelo,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.7
            )
            
            if response and response.choices:
                return response.choices[0].message.content.strip()
            else:
                return "Não foi possível gerar insights no momento."
                
        except Exception as e:
            return f"Erro na análise: {str(e)}"
    
    def gerar_recomendacoes_economia(self) -> str:
        """Gera recomendações específicas de economia."""
        if not self.inicializar_llm():
            return "Erro ao conectar com o sistema de recomendações."
        
        resumo = self.preparar_resumo_dados()
        if not resumo:
            return "Dados insuficientes para recomendações."
        
        # Identificar categorias com maior potencial de economia
        gastos_cat = resumo['categorias']['gastos_por_categoria']
        categorias_ordenadas = sorted(gastos_cat.items(), key=lambda x: x[1], reverse=True)
        
        prompt = f"""Você é um consultor financeiro especializado em otimização de gastos pessoais.

Com base nos dados de gastos abaixo, forneça recomendações ESPECÍFICAS e PRÁTICAS para economia:

TOP 5 CATEGORIAS DE GASTOS:
{json.dumps(dict(categorias_ordenadas[:5]), indent=2, ensure_ascii=False)}

CONTEXTO ADICIONAL:
- Saldo atual: R$ {resumo['totais']['saldo']:,.2f}
- Ticket médio: R$ {resumo['padroes']['ticket_medio']:,.2f}
- Período analisado: {resumo['periodo']['dias']} dias

INSTRUÇÕES:
1. Foque nas 3 principais categorias de gasto
2. Dê dicas específicas e actionáveis para cada categoria
3. Sugira metas de redução realistas (percentuais)
4. Inclua alternativas práticas e substituições
5. Considere o contexto brasileiro
6. Use linguagem motivadora mas realista

Formato da resposta:
- Use bullet points para facilitar leitura
- Seja específico (ex: "reduza 15% nos gastos com alimentação")
- Inclua pelo menos uma dica para cada categoria principal

Responda em português brasileiro."""

        try:
            response = self.config_llm.client.chat.completions.create(
                model=self.config_llm.modelo,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=600,
                temperature=0.6
            )
            
            if response and response.choices:
                return response.choices[0].message.content.strip()
            else:
                return "Não foi possível gerar recomendações no momento."
                
        except Exception as e:
            return f"Erro nas recomendações: {str(e)}"
    
    def gerar_analise_tendencias(self) -> str:
        """Gera análise de tendências e padrões."""
        if not self.inicializar_llm():
            return "Erro ao conectar com o sistema de análise."
        
        if self.df is None or self.df.empty:
            return "Dados insuficientes para análise de tendências."
        
        # Análise temporal
        self.df['Mes_Ano'] = self.df['Data'].dt.to_period('M')
        gastos_mensais = self.df[self.df['Valor'] > 0].groupby('Mes_Ano')['Valor'].sum()
        
        # Análise por dia da semana
        self.df['Dia_Semana'] = self.df['Data'].dt.day_name()
        gastos_dia_semana = self.df[self.df['Valor'] > 0].groupby('Dia_Semana')['Valor'].sum()
        
        prompt = f"""Você é um analista financeiro especializado em identificação de padrões de consumo.

Analise os padrões temporais de gastos abaixo e identifique tendências importantes:

GASTOS POR MÊS:
{gastos_mensais.to_dict()}

GASTOS POR DIA DA SEMANA:
{gastos_dia_semana.to_dict()}

PERÍODO TOTAL: {len(self.df)} transações em {(self.df['Data'].max() - self.df['Data'].min()).days} dias

INSTRUÇÕES:
1. Identifique padrões sazonais ou mensais
2. Analise comportamento por dia da semana
3. Destaque tendências de crescimento ou redução
4. Identifique dias/períodos de maior gasto
5. Sugira estratégias baseadas nos padrões identificados

Seja objetivo e foque em insights acionáveis. Responda em português brasileiro."""

        try:
            response = self.config_llm.client.chat.completions.create(
                model=self.config_llm.modelo,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.5
            )
            
            if response and response.choices:
                return response.choices[0].message.content.strip()
            else:
                return "Não foi possível analisar tendências no momento."
                
        except Exception as e:
            return f"Erro na análise de tendências: {str(e)}"
    
    def gerar_alerta_gastos(self) -> str:
        """Gera alertas sobre gastos incomuns ou preocupantes."""
        if not self.inicializar_llm():
            return "Sistema de alertas indisponível."
        
        resumo = self.preparar_resumo_dados()
        if not resumo:
            return "Dados insuficientes para alertas."
        
        # Calcular métricas para alertas
        gastos = self.df[self.df['Valor'] > 0]
        
        # Gastos acima da média + 2 desvios padrão
        media = gastos['Valor'].mean()
        desvio = gastos['Valor'].std()
        limite_alto = media + (2 * desvio)
        gastos_altos = gastos[gastos['Valor'] > limite_alto]
        
        # Concentração em uma categoria
        total_gastos = gastos['Valor'].sum()
        concentracao_categoria = {}
        for categoria in gastos['Categoria'].unique():
            valor_cat = gastos[gastos['Categoria'] == categoria]['Valor'].sum()
            percentual = (valor_cat / total_gastos) * 100
            concentracao_categoria[categoria] = percentual
        
        categoria_dominante = max(concentracao_categoria, key=concentracao_categoria.get)
        percentual_dominante = concentracao_categoria[categoria_dominante]
        
        prompt = f"""Você é um consultor financeiro especializado em alertas e controle de riscos financeiros.

Analise a situação financeira e identifique possíveis alertas ou pontos de atenção:

SITUAÇÃO ATUAL:
- Saldo líquido: R$ {resumo['totais']['saldo']:,.2f}
- Total de gastos: R$ {resumo['totais']['gastos']:,.2f}
- Gastos acima do normal: {len(gastos_altos)} transações
- Categoria dominante: {categoria_dominante} ({percentual_dominante:.1f}% dos gastos)

GASTOS ELEVADOS DETECTADOS:
{gastos_altos[['Descricao', 'Valor', 'Categoria']].to_dict('records') if not gastos_altos.empty else 'Nenhum gasto elevado detectado'}

CONCENTRAÇÃO POR CATEGORIA:
{json.dumps(concentracao_categoria, indent=2, ensure_ascii=False)}

INSTRUÇÕES:
1. Identifique possíveis alertas financeiros
2. Avalie se há concentração excessiva em alguma categoria
3. Destaque gastos que merecem atenção
4. Sugira ações preventivas se necessário
5. Seja construtivo e evite alarmes desnecessários

Se não houver alertas importantes, parabenize pela gestão financeira.
Responda em português brasileiro de forma clara e objetiva."""

        try:
            response = self.config_llm.client.chat.completions.create(
                model=self.config_llm.modelo,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.3
            )
            
            if response and response.choices:
                return response.choices[0].message.content.strip()
            else:
                return "Sistema de alertas temporariamente indisponível."
                
        except Exception as e:
            return f"Erro nos alertas: {str(e)}"
    
    def gerar_todos_insights(self) -> Dict[str, str]:
        """Gera todos os tipos de insights."""
        if not self.carregar_dados():
            return {"erro": "Não foi possível carregar os dados"}
        
        print("🧠 Gerando insights inteligentes...")
        
        insights = {}
        
        print("   📊 Análise geral...")
        insights['analise_geral'] = self.gerar_insight_geral()
        
        print("   💡 Recomendações de economia...")
        insights['recomendacoes'] = self.gerar_recomendacoes_economia()
        
        print("   📈 Análise de tendências...")
        insights['tendencias'] = self.gerar_analise_tendencias()
        
        print("   ⚠️  Alertas financeiros...")
        insights['alertas'] = self.gerar_alerta_gastos()
        
        print("✅ Insights gerados com sucesso!")
        
        return insights

def main():
    """Função principal para teste do módulo."""
    print("=== GERAÇÃO DE INSIGHTS COM LLM - TESTE ===")
    
    insights_generator = InsightsLLM()
    insights = insights_generator.gerar_todos_insights()
    
    if 'erro' in insights:
        print(f"❌ {insights['erro']}")
        return False
    
    print("\n" + "="*60)
    print("🧠 INSIGHTS GERADOS")
    print("="*60)
    
    for tipo, conteudo in insights.items():
        print(f"\n📋 {tipo.upper().replace('_', ' ')}:")
        print("-" * 40)
        print(conteudo)
    
    return True

if __name__ == "__main__":
    main()
