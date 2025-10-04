#!/usr/bin/env python3
"""
Dashboard Interativo Avançado com Insights LLM - Sistema de Controle de Gastos Pessoais
Interface web completa para visualização e análise dos dados financeiros com IA.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import os
import numpy as np
from insights_llm import InsightsLLM

# Configuração da página
st.set_page_config(
    page_title="Controle de Gastos Pessoais",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

class DashboardGastos:
    def __init__(self, arquivo_dados: str = "../data/gastos.xlsx"):
        self.arquivo_dados = arquivo_dados
        self.df = None
        self.insights_generator = InsightsLLM(arquivo_dados)
        self.carregar_dados()
    
    def carregar_dados(self):
        """Carrega os dados do arquivo Excel."""
        try:
            if os.path.exists(self.arquivo_dados):
                self.df = pd.read_excel(self.arquivo_dados, engine='openpyxl')
                # Converter coluna de data para datetime
                self.df['Data'] = pd.to_datetime(self.df['Data'], format='%d/%m/%Y', errors='coerce')
                # Adicionar colunas derivadas
                self.df['Dia_Semana'] = self.df['Data'].dt.day_name()
                self.df['Mes'] = self.df['Data'].dt.month
                self.df['Ano'] = self.df['Data'].dt.year
                self.df['Dia_Mes'] = self.df['Data'].dt.day
                return True
            else:
                st.error(f"Arquivo de dados não encontrado: {self.arquivo_dados}")
                return False
        except Exception as e:
            st.error(f"Erro ao carregar dados: {e}")
            return False
    
    def aplicar_filtros(self, df, filtros):
        """Aplica filtros ao DataFrame."""
        df_filtrado = df.copy()
        
        if filtros.get('categoria') and filtros['categoria'] != 'Todas':
            df_filtrado = df_filtrado[df_filtrado['Categoria'] == filtros['categoria']]
        
        if filtros.get('banco') and filtros['banco'] != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['Origem'] == filtros['banco']]
        
        if filtros.get('data_inicio') and filtros.get('data_fim'):
            df_filtrado = df_filtrado[
                (df_filtrado['Data'].dt.date >= filtros['data_inicio']) &
                (df_filtrado['Data'].dt.date <= filtros['data_fim'])
            ]
        
        return df_filtrado
    
    def exibir_metricas_principais(self, df_filtrado):
        """Exibe as métricas principais no topo do dashboard."""
        if df_filtrado is None or df_filtrado.empty:
            st.warning("Nenhum dado disponível para exibir métricas.")
            return
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            total_gastos = df_filtrado[df_filtrado['Valor'] > 0]['Valor'].sum()
            st.metric(
                label="💰 Total de Gastos",
                value=f"R$ {total_gastos:,.2f}",
                delta=None
            )
        
        with col2:
            total_receitas = abs(df_filtrado[df_filtrado['Valor'] < 0]['Valor'].sum())
            st.metric(
                label="💵 Total de Receitas",
                value=f"R$ {total_receitas:,.2f}",
                delta=None
            )
        
        with col3:
            saldo_liquido = df_filtrado['Valor'].sum()
            delta_color = "normal" if saldo_liquido >= 0 else "inverse"
            st.metric(
                label="📊 Saldo Líquido",
                value=f"R$ {saldo_liquido:,.2f}",
                delta=None
            )
        
        with col4:
            ticket_medio = df_filtrado[df_filtrado['Valor'] > 0]['Valor'].mean()
            st.metric(
                label="🎯 Ticket Médio",
                value=f"R$ {ticket_medio:,.2f}" if not pd.isna(ticket_medio) else "R$ 0,00",
                delta=None
            )
        
        with col5:
            total_transacoes = len(df_filtrado)
            st.metric(
                label="📈 Transações",
                value=f"{total_transacoes:,}",
                delta=None
            )
    
    def criar_grafico_pizza_categorias(self, df_filtrado):
        """Cria gráfico de pizza das categorias."""
        if df_filtrado is None or df_filtrado.empty:
            return None
        
        # Filtrar apenas gastos (valores positivos)
        df_gastos = df_filtrado[df_filtrado['Valor'] > 0]
        
        if df_gastos.empty:
            return None
        
        # Agrupar por categoria
        categorias = df_gastos.groupby('Categoria')['Valor'].sum().reset_index()
        categorias = categorias.sort_values('Valor', ascending=False)
        
        fig = px.pie(
            categorias, 
            values='Valor', 
            names='Categoria',
            title="Distribuição de Gastos por Categoria",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Valor: R$ %{value:,.2f}<br>Percentual: %{percent}<extra></extra>'
        )
        fig.update_layout(height=500, showlegend=True)
        
        return fig
    
    def criar_grafico_barras_categorias(self, df_filtrado):
        """Cria gráfico de barras das categorias."""
        if df_filtrado is None or df_filtrado.empty:
            return None
        
        # Filtrar apenas gastos (valores positivos)
        df_gastos = df_filtrado[df_filtrado['Valor'] > 0]
        
        if df_gastos.empty:
            return None
        
        # Agrupar por categoria
        categorias = df_gastos.groupby('Categoria').agg({
            'Valor': 'sum',
            'Descricao': 'count'
        }).reset_index()
        categorias.columns = ['Categoria', 'Valor_Total', 'Quantidade']
        categorias = categorias.sort_values('Valor_Total', ascending=True)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=categorias['Categoria'],
            x=categorias['Valor_Total'],
            orientation='h',
            text=[f'R$ {v:,.0f}' for v in categorias['Valor_Total']],
            textposition='auto',
            marker_color='lightblue',
            hovertemplate='<b>%{y}</b><br>Valor: R$ %{x:,.2f}<br>Transações: %{customdata}<extra></extra>',
            customdata=categorias['Quantidade']
        ))
        
        fig.update_layout(
            title="Gastos por Categoria (Valor Total)",
            xaxis_title="Valor (R$)",
            yaxis_title="Categoria",
            height=500
        )
        
        return fig
    
    def criar_grafico_timeline(self, df_filtrado):
        """Cria gráfico de linha temporal dos gastos."""
        if df_filtrado is None or df_filtrado.empty:
            return None
        
        # Separar gastos e receitas
        df_gastos = df_filtrado[df_filtrado['Valor'] > 0]
        df_receitas = df_filtrado[df_filtrado['Valor'] < 0]
        
        # Agrupar por data
        timeline_gastos = df_gastos.groupby(df_gastos['Data'].dt.date)['Valor'].sum().reset_index()
        timeline_receitas = df_receitas.groupby(df_receitas['Data'].dt.date)['Valor'].sum().abs().reset_index()
        
        fig = go.Figure()
        
        if not timeline_gastos.empty:
            fig.add_trace(go.Scatter(
                x=timeline_gastos['Data'],
                y=timeline_gastos['Valor'],
                mode='lines+markers',
                name='Gastos',
                line=dict(color='red', width=2),
                marker=dict(size=6)
            ))
        
        if not timeline_receitas.empty:
            fig.add_trace(go.Scatter(
                x=timeline_receitas['Data'],
                y=timeline_receitas['Valor'],
                mode='lines+markers',
                name='Receitas',
                line=dict(color='green', width=2),
                marker=dict(size=6)
            ))
        
        fig.update_layout(
            title="Evolução de Gastos e Receitas ao Longo do Tempo",
            xaxis_title="Data",
            yaxis_title="Valor (R$)",
            height=400,
            hovermode='x unified'
        )
        
        return fig
    
    def criar_grafico_heatmap_gastos(self, df_filtrado):
        """Cria heatmap de gastos por dia da semana e hora."""
        if df_filtrado is None or df_filtrado.empty:
            return None
        
        # Filtrar apenas gastos
        df_gastos = df_filtrado[df_filtrado['Valor'] > 0]
        
        if df_gastos.empty:
            return None
        
        # Criar matriz de gastos por dia da semana e dia do mês
        heatmap_data = df_gastos.groupby(['Dia_Semana', 'Dia_Mes'])['Valor'].sum().reset_index()
        
        # Pivot para criar matriz
        pivot_data = heatmap_data.pivot(index='Dia_Semana', columns='Dia_Mes', values='Valor').fillna(0)
        
        # Ordenar dias da semana
        dias_ordem = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        pivot_data = pivot_data.reindex(dias_ordem)
        
        fig = px.imshow(
            pivot_data,
            title="Heatmap de Gastos por Dia da Semana e Dia do Mês",
            labels=dict(x="Dia do Mês", y="Dia da Semana", color="Valor (R$)"),
            color_continuous_scale="Reds"
        )
        
        fig.update_layout(height=400)
        
        return fig
    
    def criar_grafico_comparativo_bancos(self, df_filtrado):
        """Cria gráfico comparativo entre bancos."""
        if df_filtrado is None or df_filtrado.empty:
            return None
        
        # Agrupar por banco e categoria
        comparativo = df_filtrado.groupby(['Origem', 'Categoria'])['Valor'].sum().reset_index()
        
        fig = px.bar(
            comparativo,
            x='Categoria',
            y='Valor',
            color='Origem',
            title="Comparativo de Gastos por Banco e Categoria",
            barmode='group'
        )
        
        fig.update_layout(
            height=400,
            xaxis_title="Categoria",
            yaxis_title="Valor (R$)"
        )
        
        return fig
    
    def criar_grafico_top_gastos(self, df_filtrado, top_n=10):
        """Cria gráfico dos maiores gastos."""
        if df_filtrado is None or df_filtrado.empty:
            return None
        
        # Filtrar apenas gastos e pegar os maiores
        df_gastos = df_filtrado[df_filtrado['Valor'] > 0]
        top_gastos = df_gastos.nlargest(top_n, 'Valor')
        
        if top_gastos.empty:
            return None
        
        fig = px.bar(
            top_gastos,
            x='Valor',
            y='Descricao',
            orientation='h',
            title=f"Top {top_n} Maiores Gastos",
            color='Categoria',
            hover_data=['Data', 'Origem']
        )
        
        fig.update_layout(
            height=500,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        return fig
    
    def exibir_tabela_detalhada(self, df_filtrado):
        """Exibe tabela detalhada dos gastos."""
        if df_filtrado is None or df_filtrado.empty:
            st.warning("Nenhum dado disponível para exibir na tabela.")
            return
        
        # Selecionar colunas para exibição
        colunas_exibir = ['Data', 'Descricao', 'Valor', 'Categoria', 'Origem']
        df_exibir = df_filtrado[colunas_exibir].copy()
        
        # Formatar data
        df_exibir['Data'] = df_exibir['Data'].dt.strftime('%d/%m/%Y')
        
        # Formatar valor com cores
        def formatar_valor(valor):
            if valor >= 0:
                return f"R$ {valor:,.2f}"
            else:
                return f"-R$ {abs(valor):,.2f}"
        
        df_exibir['Valor_Formatado'] = df_exibir['Valor'].apply(formatar_valor)
        
        # Ordenar por data (mais recente primeiro)
        df_exibir = df_exibir.sort_values('Data', ascending=False)
        
        # Remover coluna original de valor
        df_exibir = df_exibir.drop('Valor', axis=1)
        df_exibir = df_exibir.rename(columns={'Valor_Formatado': 'Valor'})
        
        st.dataframe(
            df_exibir,
            use_container_width=True,
            height=400
        )
    
    def criar_sidebar_filtros(self):
        """Cria sidebar com filtros."""
        st.sidebar.header("🔍 Filtros")
        
        filtros = {}
        
        if self.df is not None and not self.df.empty:
            # Filtro por categoria
            categorias = ['Todas'] + sorted(self.df['Categoria'].unique().tolist())
            filtros['categoria'] = st.sidebar.selectbox(
                "Categoria:",
                categorias
            )
            
            # Filtro por banco
            bancos = ['Todos'] + sorted(self.df['Origem'].unique().tolist())
            filtros['banco'] = st.sidebar.selectbox(
                "Banco:",
                bancos
            )
            
            # Filtro por período
            if 'Data' in self.df.columns:
                data_min = self.df['Data'].min().date()
                data_max = self.df['Data'].max().date()
                
                filtros['data_inicio'] = st.sidebar.date_input(
                    "Data início:",
                    value=data_min,
                    min_value=data_min,
                    max_value=data_max
                )
                
                filtros['data_fim'] = st.sidebar.date_input(
                    "Data fim:",
                    value=data_max,
                    min_value=data_min,
                    max_value=data_max
                )
            
            # Filtro por tipo de transação
            filtros['tipo_transacao'] = st.sidebar.selectbox(
                "Tipo de Transação:",
                ['Todas', 'Apenas Gastos', 'Apenas Receitas']
            )
        
        return filtros
    
    def exibir_estatisticas_detalhadas(self, df_filtrado):
        """Exibe estatísticas detalhadas."""
        if df_filtrado is None or df_filtrado.empty:
            return
        
        st.subheader("📈 Estatísticas Detalhadas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Por Categoria:**")
            stats_categoria = df_filtrado.groupby('Categoria').agg({
                'Valor': ['sum', 'mean', 'count', 'std']
            }).round(2)
            stats_categoria.columns = ['Total', 'Média', 'Quantidade', 'Desvio Padrão']
            st.dataframe(stats_categoria)
        
        with col2:
            st.write("**Por Banco:**")
            stats_banco = df_filtrado.groupby('Origem').agg({
                'Valor': ['sum', 'mean', 'count', 'std']
            }).round(2)
            stats_banco.columns = ['Total', 'Média', 'Quantidade', 'Desvio Padrão']
            st.dataframe(stats_banco)
    
    def exibir_insights_automaticos(self, df_filtrado):
        """Exibe insights automáticos baseados nos dados."""
        if df_filtrado is None or df_filtrado.empty:
            return
        
        st.subheader("🧠 Insights Automáticos")
        
        # Categoria com maior gasto
        categoria_maior = df_filtrado[df_filtrado['Valor'] > 0].groupby('Categoria')['Valor'].sum().idxmax()
        valor_maior = df_filtrado[df_filtrado['Valor'] > 0].groupby('Categoria')['Valor'].sum().max()
        
        # Dia da semana com mais gastos
        dia_maior = df_filtrado[df_filtrado['Valor'] > 0].groupby('Dia_Semana')['Valor'].sum().idxmax()
        
        # Ticket médio por categoria
        ticket_medio_cat = df_filtrado[df_filtrado['Valor'] > 0].groupby('Categoria')['Valor'].mean()
        categoria_ticket_alto = ticket_medio_cat.idxmax()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info(f"💡 **Maior Categoria de Gasto**\n\n{categoria_maior}: R$ {valor_maior:,.2f}")
        
        with col2:
            st.info(f"📅 **Dia com Mais Gastos**\n\n{dia_maior}")
        
        with col3:
            st.info(f"🎯 **Maior Ticket Médio**\n\n{categoria_ticket_alto}: R$ {ticket_medio_cat[categoria_ticket_alto]:,.2f}")
    
    def exibir_insights_llm(self):
        """Exibe insights gerados por LLM."""
        st.subheader("🤖 Análise Inteligente com IA")
        
        # Botão para gerar insights
        if st.button("🧠 Gerar Insights com IA", type="primary"):
            with st.spinner("Analisando seus dados financeiros com IA..."):
                try:
                    insights = self.insights_generator.gerar_todos_insights()
                    
                    if 'erro' in insights:
                        st.error(f"❌ {insights['erro']}")
                        return
                    
                    # Exibir insights em abas
                    tab1, tab2, tab3, tab4 = st.tabs([
                        "📊 Análise Geral", 
                        "💡 Recomendações", 
                        "📈 Tendências", 
                        "⚠️ Alertas"
                    ])
                    
                    with tab1:
                        st.markdown("### 📊 Análise Geral da Situação Financeira")
                        st.write(insights.get('analise_geral', 'Análise não disponível'))
                    
                    with tab2:
                        st.markdown("### 💡 Recomendações de Economia")
                        st.write(insights.get('recomendacoes', 'Recomendações não disponíveis'))
                    
                    with tab3:
                        st.markdown("### 📈 Análise de Tendências e Padrões")
                        st.write(insights.get('tendencias', 'Análise de tendências não disponível'))
                    
                    with tab4:
                        st.markdown("### ⚠️ Alertas Financeiros")
                        st.write(insights.get('alertas', 'Nenhum alerta identificado'))
                    
                    # Salvar timestamp da última análise
                    st.session_state['ultima_analise'] = datetime.now()
                    
                except Exception as e:
                    st.error(f"❌ Erro ao gerar insights: {str(e)}")
        
        # Mostrar quando foi a última análise
        if 'ultima_analise' in st.session_state:
            st.caption(f"Última análise: {st.session_state['ultima_analise'].strftime('%d/%m/%Y %H:%M:%S')}")

def main():
    """Função principal do dashboard."""
    
    # CSS customizado
    st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff6b6b;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
    .insight-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Título principal
    st.title("💰 Dashboard de Controle de Gastos Pessoais")
    st.markdown("---")
    
    # Inicializar dashboard
    dashboard = DashboardGastos()
    
    # Verificar se os dados foram carregados
    if dashboard.df is None or dashboard.df.empty:
        st.error("❌ Não foi possível carregar os dados.")
        st.info("💡 Execute primeiro o script `processar_faturas.py` para gerar os dados.")
        return
    
    # Criar filtros na sidebar
    filtros = dashboard.criar_sidebar_filtros()
    
    # Aplicar filtros
    df_filtrado = dashboard.aplicar_filtros(dashboard.df, filtros)
    
    # Aplicar filtro de tipo de transação
    if filtros.get('tipo_transacao') == 'Apenas Gastos':
        df_filtrado = df_filtrado[df_filtrado['Valor'] > 0]
    elif filtros.get('tipo_transacao') == 'Apenas Receitas':
        df_filtrado = df_filtrado[df_filtrado['Valor'] < 0]
    
    # Informações na sidebar
    st.sidebar.markdown("---")
    st.sidebar.info(f"📊 **{len(df_filtrado)}** transações filtradas")
    st.sidebar.info(f"📅 Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # Métricas principais
    dashboard.exibir_metricas_principais(df_filtrado)
    
    st.markdown("---")
    
    # Layout em abas
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Visão Geral", 
        "📈 Análise Temporal", 
        "🔥 Heatmaps", 
        "🏆 Rankings", 
        "🤖 Insights IA",
        "📋 Detalhes", 
        "📊 Estatísticas"
    ])
    
    with tab1:
        st.subheader("📊 Visão Geral dos Gastos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_pizza = dashboard.criar_grafico_pizza_categorias(df_filtrado)
            if fig_pizza:
                st.plotly_chart(fig_pizza, use_container_width=True)
        
        with col2:
            fig_barras = dashboard.criar_grafico_barras_categorias(df_filtrado)
            if fig_barras:
                st.plotly_chart(fig_barras, use_container_width=True)
        
        # Insights automáticos
        dashboard.exibir_insights_automaticos(df_filtrado)
    
    with tab2:
        st.subheader("📈 Análise Temporal")
        
        fig_timeline = dashboard.criar_grafico_timeline(df_filtrado)
        if fig_timeline:
            st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Gráfico comparativo por bancos
        fig_comparativo = dashboard.criar_grafico_comparativo_bancos(df_filtrado)
        if fig_comparativo:
            st.plotly_chart(fig_comparativo, use_container_width=True)
    
    with tab3:
        st.subheader("🔥 Análise de Padrões")
        
        fig_heatmap = dashboard.criar_grafico_heatmap_gastos(df_filtrado)
        if fig_heatmap:
            st.plotly_chart(fig_heatmap, use_container_width=True)
    
    with tab4:
        st.subheader("🏆 Rankings e Top Gastos")
        
        # Controle do número de itens no ranking
        top_n = st.slider("Número de itens no ranking:", 5, 20, 10)
        
        fig_top = dashboard.criar_grafico_top_gastos(df_filtrado, top_n)
        if fig_top:
            st.plotly_chart(fig_top, use_container_width=True)
    
    with tab5:
        dashboard.exibir_insights_llm()
    
    with tab6:
        st.subheader("📋 Detalhes das Transações")
        dashboard.exibir_tabela_detalhada(df_filtrado)
    
    with tab7:
        dashboard.exibir_estatisticas_detalhadas(df_filtrado)

if __name__ == "__main__":
    main()
