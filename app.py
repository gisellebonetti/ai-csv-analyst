import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.title("AI CSV Analyst")

uploaded_file = st.file_uploader("Escolha seu CSV", type=["csv"])

# Função que chama a IA local (Ollama)
def gerar_insight(dados_texto):
    prompt = f"""
Você é um analista de dados.
Com base nos dados abaixo, gere insights claros e objetivos em até 5 frases:

{dados_texto}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:1b",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Dados")
    st.dataframe(df)

    st.subheader("📈 Resumo estatístico")
    st.write(df.describe())

    # ---------------- GRÁFICO 1 ----------------
    if "data" in df.columns and "vendas" in df.columns:
        df["data"] = pd.to_datetime(df["data"])
        fig = px.line(df, x="data", y="vendas", title="Vendas ao longo do tempo")
        st.plotly_chart(fig)

    # ---------------- GRÁFICO 2 ----------------
    if "regiao" in df.columns:
        fig2 = px.bar(df, x="regiao", y="vendas", title="Vendas por região")
        st.plotly_chart(fig2)

    # ---------------- IA ----------------
    st.subheader("🧠 Insights da IA")

    dados_texto = df.head(10).to_string()

    if st.button("Gerar insights com IA"):
        with st.spinner("Analisando com IA..."):
            try:
                insight = gerar_insight(dados_texto)
                st.success(insight)
            except Exception as e:
                st.error(f"Erro ao gerar insight: {e}")