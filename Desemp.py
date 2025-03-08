import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# Configuração da barra lateral
with st.sidebar:
     st.divider()
     st.image("./Logo.png", "Por: Ryan Costa Rangel")
     st.markdown(
        "<h1 style='text-align: center;'>Bem-vindo ao ambiente tesouraria</h1>", 
        unsafe_allow_html=True
    )

     st.divider()

     st.text("O mercado de ações é um ambiente dinâmico onde investidores compram e vendem participações em empresas. No setor da construção civil, ações de grandes construtoras brasileiras, como Cyrela, MRV e Even, refletem o desempenho do mercado imobiliário e a confiança dos investidores. Este aplicativo permite visualizar e analisar o histórico de preços dessas ações, identificando tendências e variações ao longo do tempo. Com gráficos interativos e indicadores financeiros, é possível avaliar o comportamento do mercado e tomar decisões mais embasadas. Ao acompanhar métricas como preços de fechamento, volume de negociações e retornos, investidores podem entender melhor os ciclos econômicos e oportunidades no setor. 🚀")

# Lista de construtoras brasileiras na B3
acoes = {
    "Cyrela": "CYRE3.SA",
    "MRV": "MRVE3.SA",
    "Eztec": "EZTC3.SA",
    "Even": "EVEN3.SA",
    "Direcional": "DIRR3.SA",
    "Tenda": "TEND3.SA"
}

st.markdown(
    "<h1 style='text-align: center;'>Análise de Ações de Construtoras Brasileiras</h1>",
    unsafe_allow_html=True
)

st.divider()

# Escolher a construtora
empresa = st.selectbox("🏗️ Escolha uma construtora:", list(acoes.keys()))
simbolo = acoes[empresa]

# Definir período
periodo = st.selectbox("📅 Escolha o período de análise:", ["7d", "1mo", "3mo", "6mo", "1y", "5y"])

st.divider()
# Baixar os dados do Yahoo Finance
st.write(f"### Dados históricos da {empresa} ({simbolo}) para {periodo}")
df = yf.download(simbolo, period=periodo)

# Verificar se há dados retornados
if df.empty:
    st.error("❌ Nenhum dado encontrado para esse período. Tente escolher outro.")
else:
    # Se houver MultiIndex, remover o primeiro nível
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(1) # Pega apenas os nomes das colunas
   

    # Renomear colunas, caso ainda contenham o nome da ação
    df.columns = ["Open", "High", "Low", "Close", "Adj Close", "Volume"][:len(df.columns)]

    # Resetar índice para usar datas corretamente nos gráficos
    df = df.reset_index()

    # Exibir tabela de preços
    st.dataframe(df.tail(),use_container_width=True)
    
    st.divider()
    # Verificar se 'Close' está disponível antes de plotar o gráfico
    if "Close" in df.columns:
        fig = px.line(df, x="Date", y="Close", title=f"📊 Histórico de Preços - {empresa}")
        st.plotly_chart(fig)

        # Cálculo de Retorno
        retorno = ((df["Close"].iloc[-1] / df["Close"].iloc[0]) - 1) * 100
        st.divider()
        st.metric(label=f"📉 Retorno no período ({periodo})", value=f"{retorno:.2f}%")
    else:
        st.warning("⚠️ Dados de volume não disponíveis para este ativo ou período.")

    # Verificar se 'Volume' está disponível antes de exibir
    if "Volume" in df.columns and df["Volume"].notna().any():
        st.write("📊 **Indicadores:**")
        st.write("- 📈 **Volume médio de negociações:**", round(df["Volume"].mean(), 2))
        st.write("- 💰 **Último preço de fechamento:** R$", round(df["Close"].iloc[-1], 2))

# Rodapé
st.write("---")
#st.write("**Desenvolvido com ❤️ usando Streamlit e Yahoo Finance API**")
st.markdown(
        "<h1 style='font-size: 15px;text-align: center;'>Desenvolvido com ❤️ usando Streamlit e Yahoo Finance API</h1>", 
        unsafe_allow_html=True
    )
