import streamlit as st

def gols(competicoes=[], mando=[]):

    import pandas as pd
    import openpyxl

    #TABELAS QUE SERÃO USADAS
    df_escalacao = pd.read_excel("escalacoes.xlsx")
    df_jogos = pd.read_excel("jogos.xlsx")

    #CRIANDO UM FILTRO NOS FILTROS
    competicoes, mando = filtro_comp_mando(c=competicoes, m=mando)


    df_gols = pd.merge(df_escalacao[["id_jogo", "autor_gols_pro"]], df_jogos[["id_jogo", "competicao", "mando"]], on="id_jogo", how="inner")
    for col in df_gols.select_dtypes(include=["object", "string"]):
        df_gols[col] = df_gols[col].str.strip()

    df_gols = df_gols[(df_gols["competicao"].isin(competicoes)) & (df_gols["mando"].isin(mando))]
    #REMOVE JOGOS SEM GOLS
    

    df_gols = df_gols.dropna()

        

    #QUEBRA AS COLUNAS EM LISTAS
    df_gols["autor_gols_pro"] = df_gols["autor_gols_pro"].str.split(', ')

    #CONCATENA CADA LISTA EM UMA LISTA APENAS
    lista_gols = sum(df_gols["autor_gols_pro"], [])

    #COLOCA TODOS OS JOGADORES EM LETRAS MAIUSCULAS
    lista_gols = [item.upper() for item in lista_gols]

    #PREPARA OS DADOS PRA FAZER O DATA FRAME
    dados = {
        "gols": lista_gols
    }

    df_resumo_gols = pd.DataFrame(dados)
    


    #CONTAGEM DE GOLS
    gols = df_resumo_gols["gols"].value_counts().reset_index()

    gols = gols.rename(columns={'index': 'jogador'})

    return gols.sort_values("gols", ascending=False)


def filtro_comp_mando(c, m):
    if len(c) < 1:
        competicoes = ['Mineiro', 'Sul Americana', 'Brasileiro', 'Copa do Brasil']
    else:
        competicoes = c

    
    if len(m) < 1:
        mando = ['Casa', 'Fora']
    else:
        mando = m

    return competicoes, mando


st.title("Painel de Artilheiros")

competicao_sel = st.multiselect("Selecione as Competições: ", ['Mineiro', 'Sul Americana', 'Brasileiro', 'Copa do Brasil', ''])
mando_sel = st.multiselect("Selecione os Mandos: ", ['Casa', 'Fora'])


df = gols(competicoes=competicao_sel, mando=mando_sel)


st.table(df)

