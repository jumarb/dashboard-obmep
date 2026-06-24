import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO

csv_texto = """edicao,nivel,ouro_pub_fem,ouro_pub_masc,prata_pub_fem,prata_pub_masc,bronze_pub_fem,bronze_pub_masc,ouro_priv_fem,ouro_priv_masc,prata_priv_fem,prata_priv_masc,bronze_priv_fem,bronze_priv_masc
16ª,1,7,10,13,18,19,40,0,2,1,4,5,8
17ª,1,5,7,4,15,28,56,0,3,1,2,3,16
18ª,1,1,11,9,15,25,54,2,2,0,11,10,31
19ª,1,4,7,4,21,23,57,0,4,3,7,17,33
20ª,1,1,7,4,16,14,55,4,6,5,12,14,31
16ª,2,2,16,13,21,19,36,1,1,0,3,6,15
17ª,2,4,7,5,28,13,44,0,1,0,8,8,13
18ª,2,1,5,7,24,24,48,0,2,2,6,7,24
19ª,2,2,5,2,15,14,46,3,2,1,13,3,34
20ª,2,0,4,9,24,16,34,0,3,7,15,18,40
16ª,3,2,13,8,47,12,59,0,1,2,3,4,17
17ª,3,1,4,13,41,21,48,0,1,0,11,4,18
18ª,3,0,7,3,15,14,38,0,7,4,9,7,29
19ª,3,2,4,2,28,6,52,0,4,3,12,6,39
20ª,3,0,3,5,26,4,45,1,3,1,13,11,41"""

df = pd.read_csv(StringIO(csv_texto))

df['total_pub']   = (df['ouro_pub_fem'] + df['ouro_pub_masc'] +
                     df['prata_pub_fem'] + df['prata_pub_masc'] +
                     df['bronze_pub_fem'] + df['bronze_pub_masc'])
df['total_priv']  = (df['ouro_priv_fem'] + df['ouro_priv_masc'] +
                     df['prata_priv_fem'] + df['prata_priv_masc'] +
                     df['bronze_priv_fem'] + df['bronze_priv_masc'])
df['total_geral'] = df['total_pub'] + df['total_priv']
df['total_fem']   = (df['ouro_pub_fem'] + df['prata_pub_fem'] + df['bronze_pub_fem'] +
                     df['ouro_priv_fem'] + df['prata_priv_fem'] + df['bronze_priv_fem'])
df['total_masc']  = (df['ouro_pub_masc'] + df['prata_pub_masc'] + df['bronze_pub_masc'] +
                     df['ouro_priv_masc'] + df['prata_priv_masc'] + df['bronze_priv_masc'])
df['pct_pub']  = (df['total_pub']  / df['total_geral'] * 100).round(1)
df['pct_priv'] = (df['total_priv'] / df['total_geral'] * 100).round(1)
df['pct_fem']  = (df['total_fem']  / df['total_geral'] * 100).round(1)
df['pct_masc'] = (df['total_masc'] / df['total_geral'] * 100).round(1)

# ── Layout ────────────────────────────────────────────────────────────────────
st.title('📊 Dashboard OBMEP')
st.markdown('Análise de medalhas da 16ª à 20ª edição')

# ── Filtro ────────────────────────────────────────────────────────────────────
nivel_selecionado = st.selectbox(
    'Filtrar por nível',
    options=['Todos', 'Nível 1', 'Nível 2', 'Nível 3']
)

if nivel_selecionado == 'Nível 1':
    df_filtrado = df[df['nivel'] == 1]
elif nivel_selecionado == 'Nível 2':
    df_filtrado = df[df['nivel'] == 2]
elif nivel_selecionado == 'Nível 3':
    df_filtrado = df[df['nivel'] == 3]
else:
    df_filtrado = df

# ── Métricas ──────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
col1.metric('Total de medalhas', df_filtrado['total_geral'].sum())
col2.metric('Média % pública', f"{df_filtrado['pct_pub'].mean():.1f}%")
col3.metric('Média % feminina', f"{df_filtrado['pct_fem'].mean():.1f}%")

st.divider()

# ── Gráfico 1 ─────────────────────────────────────────────────────────────────
por_edicao = df_filtrado.groupby('edicao')['total_geral'].sum().reset_index()
fig1 = px.line(
    por_edicao, x='edicao', y='total_geral',
    title='Evolução do total de medalhas',
    labels={'edicao': 'Edição', 'total_geral': 'Total'},
    markers=True, line_shape='spline'
)
fig1.update_traces(line_color='#2E86AB', line_width=3, marker_size=10)
fig1.update_layout(    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(color='#111111', size=13),
    xaxis=dict(tickfont=dict(color='#111111'), title_font=dict(color='#111111')),
    yaxis=dict(tickfont=dict(color='#111111'), title_font=dict(color='#111111')),
    legend=dict(font=dict(color='#111111'), title=dict(text='Sexo', font=dict(color='#111111'))),
    title_font_color='#111111' )
fig1.update_yaxes(gridcolor='#EEEEEE')
st.plotly_chart(fig1, use_container_width=True)

# ── Gráfico 2 ─────────────────────────────────────────────────────────────────
por_rede = df_filtrado.groupby('edicao')[['total_pub', 'total_priv']].sum().reset_index()
por_rede = por_rede.rename(columns={'total_pub': 'Pública', 'total_priv': 'Privada'})
fig2 = px.bar(
    por_rede, x='edicao', y=['Pública', 'Privada'],
    title='Medalhas por rede escolar',
    labels={'edicao': 'Edição', 'value': 'Total', 'variable': 'Rede'},
    barmode='stack',
    color_discrete_map={'Pública': '#2E86AB', 'Privada': '#E84855'}
)
fig2.update_layout(    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(color='#111111', size=13),
    xaxis=dict(tickfont=dict(color='#111111'), title_font=dict(color='#111111')),
    yaxis=dict(tickfont=dict(color='#111111'), title_font=dict(color='#111111')),
    legend=dict(font=dict(color='#111111'), title=dict(text='Sexo', font=dict(color='#111111'))),
    title_font_color='#111111')
fig2.update_yaxes(gridcolor='#EEEEEE')
st.plotly_chart(fig2, use_container_width=True)

# ── Gráfico 3 ─────────────────────────────────────────────────────────────────
por_sexo = df_filtrado.groupby('edicao')[['total_fem', 'total_masc']].sum().reset_index()
por_sexo = por_sexo.rename(columns={'total_fem': 'Feminino', 'total_masc': 'Masculino'})
fig3 = px.bar(
    por_sexo, x='edicao', y=['Feminino', 'Masculino'],
    title='Distribuição por sexo',
    labels={'edicao': 'Edição', 'value': 'Total', 'variable': 'Sexo'},
    barmode='stack',
    color_discrete_map={'Feminino': '#E84855', 'Masculino': '#2E86AB'}
)
fig3.update_layout(    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(color='#111111', size=13),
    xaxis=dict(tickfont=dict(color='#111111'), title_font=dict(color='#111111')),
    yaxis=dict(tickfont=dict(color='#111111'), title_font=dict(color='#111111')),
    legend=dict(font=dict(color='#111111'), title=dict(text='Sexo', font=dict(color='#111111'))),
    title_font_color='#111111')
fig3.update_yaxes(gridcolor='#EEEEEE')
st.plotly_chart(fig3, use_container_width=True)
# ── Gráfico 4 ─────────────────────────────────────────────────────────────────
por_nivel_edicao = df_filtrado.groupby(['edicao', 'nivel'])['pct_pub'].mean().reset_index()
por_nivel_edicao['nivel'] = por_nivel_edicao['nivel'].map({
    1: 'Nível 1',
    2: 'Nível 2',
    3: 'Nível 3'
})

fig4 = px.line(
    por_nivel_edicao,
    x='edicao', y='pct_pub',
    color='nivel',
    title='Evolução do percentual público por nível',
    labels={
        'edicao': 'Edição',
        'pct_pub': '% de medalhas em escolas públicas',
        'nivel': 'Nível'
    },
    markers=True,
    line_shape='spline',
    color_discrete_map={
        'Nível 1': '#2E86AB',
        'Nível 2': '#E84855',
        'Nível 3': '#F4A261',
    }
)
fig4.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(color='#111111', size=13),
    xaxis=dict(tickfont=dict(color='#111111'), title_font=dict(color='#111111')),
    yaxis=dict(tickfont=dict(color='#111111'), title_font=dict(color='#111111'), ticksuffix='%'),
    legend=dict(font=dict(color='#111111'), title=dict(text='Nível', font=dict(color='#111111'))),
    title_font_color='#111111',
)
fig4.update_yaxes(gridcolor='#EEEEEE', range=[40, 100])
st.plotly_chart(fig4, use_container_width=True)
# ── Gráfico 5 ─────────────────────────────────────────────────────────────────
por_nivel_edicao_priv = df_filtrado.groupby(['edicao', 'nivel'])['pct_priv'].mean().reset_index()
por_nivel_edicao_priv['nivel'] = por_nivel_edicao_priv['nivel'].map({
    1: 'Nível 1',
    2: 'Nível 2',
    3: 'Nível 3'
})

fig5 = px.line(
    por_nivel_edicao_priv,
    x='edicao', y='pct_priv',
    color='nivel',
    title='Evolução do percentual privado por nível',
    labels={
        'edicao': 'Edição',
        'pct_priv': '% de medalhas em escolas privadas',
        'nivel': 'Nível'
    },
    markers=True,
    line_shape='spline',
    color_discrete_map={
        'Nível 1': '#2E86AB',
        'Nível 2': '#E84855',
        'Nível 3': '#F4A261',
    }
)
fig5.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(color='#111111', size=13),
    xaxis=dict(tickfont=dict(color='#111111'), title_font=dict(color='#111111')),
    yaxis=dict(tickfont=dict(color='#111111'), title_font=dict(color='#111111'), ticksuffix='%'),
    legend=dict(font=dict(color='#111111'), title=dict(text='Nível', font=dict(color='#111111'))),
    title_font_color='#111111',
)
fig5.update_yaxes(gridcolor='#EEEEEE', range=[0, 60])
st.plotly_chart(fig5, use_container_width=True)
