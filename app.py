import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Agenda Semanal Online",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2e86ab;
        margin: 1rem 0;
    }
    .card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .feriado {
        background-color: #fff3cd;
        color: #856404;
        padding: 0.3rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .folga {
        background-color: #d4edda;
        color: #155724;
        padding: 0.3rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .remota {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 0.3rem;
        border-radius: 5px;
    }
    .stDataFrame {
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Dados completos da agenda
def carregar_dados_completos():
    # Gerentes
    gerentes = [
        {'Nome': 'ALESSANDRO', 'Categoria': 'Gerente', 'Função': 'GERÊNCIA DE OPERAÇÕES', 
         'Segunda': 'GERÊNCIA DE OPERAÇÕES', 'Terça': 'GERÊNCIA DE OPERAÇÕES', 
         'Quarta': 'GERÊNCIA DE OPERAÇÕES', 'Quinta': 'FERIADO', 'Sexta': 'FOLGA', 'Sábado': ''},
        
        {'Nome': 'CESAR CANDIDO', 'Categoria': 'Gerente', 'Função': 'GERÊNCIA COMERCIAL', 
         'Segunda': 'GERÊNCIA COMERCIAL', 'Terça': 'GERÊNCIA COMERCIAL', 
         'Quarta': 'GERÊNCIA COMERCIAL', 'Quinta': 'FERIADO', 'Sexta': 'GERÊNCIA COMERCIAL', 'Sábado': ''},
        
        {'Nome': 'GERALDO', 'Categoria': 'Gerente', 'Função': 'GERÊNCIA DE RELACIONAMENTOS', 
         'Segunda': 'GERÊNCIA DE RELACIONAMENTOS', 'Terça': 'GERÊNCIA DE RELACIONAMENTOS', 
         'Quarta': 'GERÊNCIA DE RELACIONAMENTOS', 'Quinta': 'FERIADO', 'Sexta': 'GERÊNCIA DE RELACIONAMENTOS (atividade remota)', 'Sábado': ''}
    ]
    
    # Líderes
    lideres = [
        {'Nome': 'MARIZELDA', 'Categoria': 'Líder', 'Função': 'LIDERANÇA RBI AUTOMOB', 
         'Segunda': '[RBI] AUTOMOB 2.473/521 (atividade remota)', 'Terça': '[RBI] AUTOMOB 2.473/521 (atividade remota)', 
         'Quarta': '[RBI] AUTOMOB 2.473/521 (atividade remota)', 'Quinta': 'FERIADO', 'Sexta': '[RBI] AUTOMOB 2.473/521 (atividade remota)', 'Sábado': ''},
        
        {'Nome': 'GILSON', 'Categoria': 'Líder', 'Função': 'LIDERANÇA AT. PREMIUM', 
         'Segunda': 'FOLGA', 'Terça': '[RBI] BRAVO AT. PREMIUM 8.073/36 (atividade remota)', 
         'Quarta': 'AT. PREMIUM 8.073/36 (manhã) (atividade remota)', 'Quinta': 'FERIADO', 'Sexta': 'FOLGA', 'Sábado': ''},
        
        {'Nome': 'DANIELE', 'Categoria': 'Líder', 'Função': 'LIDERANÇA DO SAC', 
         'Segunda': 'LIDERANÇA DO SAC', 'Terça': 'LIDERANÇA DO SAC', 
         'Quarta': 'LIDERANÇA DO SAC', 'Quinta': 'FERIADO', 'Sexta': 'LIDERANÇA DO SAC', 'Sábado': ''}
    ]
    
    # Consultores Chave
    consultores_chave = [
        {'Nome': 'TANIA', 'Categoria': 'Consultor Chave', 'Função': 'CONSULTORIA ESPECIALIZADA', 
         'Segunda': '[EI] REFORMA TRIB. 9.258/10', 'Terça': '[RNP] VSV 9.786/1 (atividade remota)', 
         'Quarta': '[EI] REFORMA TRIB. 9.258/10 (manhã)', 'Quinta': 'FERIADO', 'Sexta': 'FOLGA BH', 'Sábado': ''},
        
        {'Nome': 'PAULO EDUARDO', 'Categoria': 'Consultor Chave', 'Função': 'CONSULTORIA ESPECIALIZADA', 
         'Segunda': '[RNP] DIMACOL 8.629/3 (manhã) (atividade remota)', 'Terça': '[CBI] AUTOMOB PLM 9.563/3 (atividade remota)', 
         'Quarta': '[EI] SUPPORT 9.822/1 (atividade remota)', 'Quinta': 'FERIADO', 'Sexta': 'FOLGA BH', 'Sábado': ''},
        
        {'Nome': 'TIAGO MORETTO', 'Categoria': 'Consultor Chave', 'Função': 'CONSULTORIA ESPECIALIZADA', 
         'Segunda': '[RNP] CASA DO PÃO 9.528/6 (tarde) (atividade remota)', 'Terça': '[RNP] PARANA 9.806/1 (atividade remota)', 
         'Quarta': '[EI] SUPPORT 9.822/1 (atividade remota)', 'Quinta': 'FERIADO', 'Sexta': 'FOLGA BH', 'Sábado': ''},
        
        {'Nome': 'EVERTON', 'Categoria': 'Consultor Chave', 'Função': 'CONSULTORIA ESPECIALIZADA', 
         'Segunda': '[RBI] GAPLAN 9.824/1 (atividade remota)', 'Terça': '[CBI] VILHEIRA 9.124/4 (atividade remota)', 
         'Quarta': '[CBI] VILHEIRA 9.124/4 (atividade remota)', 'Quinta': '[RBI] NORTE HIDR. 9.472/1 (atividade remota)', 
         'Sexta': '[CBI] BUFALA 9.823/1 (atividade remota)', 'Sábado': ''}
    ]
    
    # Consultores (amostra)
    consultores = [
        {'Nome': 'RODRIGO FARIAS', 'Categoria': 'Consultor', 'Função': 'CONSULTOR EBI AUTOMOB', 
         'Segunda': '[EBI] AUTOMOB 8.542/22 (atividade remota)', 'Terça': '[EBI] AUTOMOB 8.542/22 (atividade remota)', 
         'Quarta': '[EBI] AUTOMOB 8.542/22 (atividade remota)', 'Quinta': 'FERIADO', 'Sexta': '[EBI] AUTOMOB 8.542/22', 'Sábado': ''},
        
        {'Nome': 'FELIPE', 'Categoria': 'Consultor', 'Função': 'CONSULTOR - FÉRIAS', 
         'Segunda': 'FÉRIAS ATÉ 25/11/2025', 'Terça': 'FÉRIAS ATÉ 25/11/2025', 
         'Quarta': 'FÉRIAS ATÉ 25/11/2025', 'Quinta': 'FÉRIAS ATÉ 25/11/2025', 'Sexta': 'FÉRIAS ATÉ 25/11/2025', 'Sábado': ''},
        
        {'Nome': 'GABRIEL TORRES', 'Categoria': 'Consultor', 'Função': 'CONSULTOR RNP ACAV', 
         'Segunda': '[RNP] ACAV 9.026/6 (atividade remota)', 'Terça': '[RNP] ACAV 9.028/6 (atividade remota)', 
         'Quarta': '[RNP] ACAV 9.029/6 (atividade remota)', 'Quinta': 'FERIADO', 'Sexta': 'FOLGA', 'Sábado': ''}
    ]
    
    # Combinar todos os dados
    todos_dados = gerentes + lideres + consultores_chave + consultores
    df = pd.DataFrame(todos_dados)
    
    # Formato longo para análises
    df_long = pd.melt(df, 
                     id_vars=['Nome', 'Categoria', 'Função'],
                     value_vars=['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'],
                     var_name='Dia', 
                     value_name='Atividade')
    
    return df, df_long

def main():
    st.markdown('<div class="main-header">📅 AGENDA SEMANAL ONLINE</div>', unsafe_allow_html=True)
    st.markdown('### 17 a 21 de Novembro de 2025')
    
    # Carregar dados
    df, df_long = carregar_dados_completos()
    
    # Sidebar
    st.sidebar.header("🔍 Filtros e Navegação")
    
    # Navegação
    pagina = st.sidebar.radio(
        "Navegar para:",
        ["🏠 Visão Geral", "👥 Agenda por Pessoa", "📊 Estatísticas", "🔍 Busca Avançada"]
    )
    
    # Filtros
    st.sidebar.subheader("Filtros")
    categorias = st.sidebar.multiselect(
        "Categorias:",
        options=df['Categoria'].unique(),
        default=df['Categoria'].unique()
    )
    
    # Aplicar filtros
    df_filtrado = df_long[df_long['Categoria'].isin(categorias)]
    
    # Páginas
    if pagina == "🏠 Visão Geral":
        mostrar_visao_geral(df, df_filtrado)
    elif pagina == "👥 Agenda por Pessoa":
        mostrar_agenda_pessoa(df, df_filtrado)
    elif pagina == "📊 Estatísticas":
        mostrar_estatisticas(df_filtrado)
    elif pagina == "🔍 Busca Avançada":
        mostrar_busca_avancada(df_filtrado)

def mostrar_visao_geral(df, df_filtrado):
    st.markdown('<div class="sub-header">📋 Visão Geral da Semana</div>', unsafe_allow_html=True)
    
    # Métricas rápidas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Pessoas", df['Nome'].nunique())
    
    with col2:
        st.metric("Atividades Agendadas", df_filtrado[df_filtrado['Atividade'] != ''].shape[0])
    
    with col3:
        st.metric("Atividades Remotas", df_filtrado[df_filtrado['Atividade'].str.contains('remota', na=False)].shape[0])
    
    with col4:
        st.metric("Folgas/Férias", df_filtrado[df_filtrado['Atividade'].str.contains('FOLGA|FERIADO|FÉRIAS', na=False)].shape[0])
    
    # Tabela principal
    st.subheader("🎯 Agenda Consolidada")
    
    # Criar tabela pivot
    pivot_df = df.pivot_table(
        index=['Nome', 'Categoria', 'Função'], 
        columns=['Dia'],
        values='Atividade',
        aggfunc='first'
    ).reset_index()
    
    st.dataframe(pivot_df, use_container_width=True, height=400)

def mostrar_agenda_pessoa(df, df_filtrado):
    st.markdown('<div class="sub-header">👥 Agenda Individual</div>', unsafe_allow_html=True)
    
    pessoa_selecionada = st.selectbox("Selecione uma pessoa:", sorted(df['Nome'].unique()))
    
    if pessoa_selecionada:
        dados_pessoa = df_filtrado[df_filtrado['Nome'] == pessoa_selecionada]
        info_pessoa = df[df['Nome'] == pessoa_selecionada].iloc[0]
        
        # Card da pessoa
        st.markdown(f"""
        <div class="card">
            <h3>{info_pessoa['Nome']}</h3>
            <p><strong>Categoria:</strong> {info_pessoa['Categoria']}</p>
            <p><strong>Função:</strong> {info_pessoa['Função']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Agenda da pessoa
        st.subheader("📅 Agenda da Semana")
        st.dataframe(dados_pessoa[['Dia', 'Atividade']].set_index('Dia'), use_container_width=True)

def mostrar_estatisticas(df_filtrado):
    st.markdown('<div class="sub-header">📊 Estatísticas e Análises</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de atividades por categoria
        atividades_por_categoria = df_filtrado[df_filtrado['Atividade'] != ''].groupby('Categoria').size()
        fig_cat = px.bar(
            x=atividades_por_categoria.index,
            y=atividades_por_categoria.values,
            labels={'x': 'Categoria', 'y': 'Número de Atividades'},
            title='Atividades por Categoria'
        )
        st.plotly_chart(fig_cat, use_container_width=True)
    
    with col2:
        # Gráfico de distribuição por dia
        atividades_por_dia = df_filtrado[df_filtrado['Atividade'] != ''].groupby('Dia').size()
        fig_dia = px.pie(
            values=atividades_por_dia.values,
            names=atividades_por_dia.index,
            title='Atividades por Dia da Semana'
        )
        st.plotly_chart(fig_dia, use_container_width=True)

def mostrar_busca_avancada(df_filtrado):
    st.markdown('<div class="sub-header">🔍 Busca Avançada</div>', unsafe_allow_html=True)
    
    termo_busca = st.text_input("🔎 Buscar nas atividades:", placeholder="Ex: AUTOMOB, SUPPORT, FOLGA...")
    
    if termo_busca:
        resultados = df_filtrado[df_filtrado['Atividade'].str.contains(termo_busca, case=False, na=False)]
        st.subheader(f"📋 Resultados ({len(resultados)} encontrados)")
        st.dataframe(resultados, use_container_width=True)
        
        # Exportação
        if st.button("📤 Exportar para CSV"):
            csv = resultados.to_csv(index=False)
            st.download_button(
                label="Baixar CSV",
                data=csv,
                file_name=f"busca_agenda_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    else:
        st.info("Digite um termo para buscar nas atividades.")

if __name__ == "__main__":
    main()