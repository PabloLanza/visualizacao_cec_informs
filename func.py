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


def gols(competicoes=[], mando=[]):

    import pandas as pd


    #TABELAS QUE SERÃO USADAS
    df_escalacao = pd.read_excel("escalacoes.xlsx")
    df_jogos = pd.read_excel("jogos.xlsx")

    #JUNÇÃO DOS DFs
    df_gols = pd.merge(df_escalacao[["id_jogo", "autor_gols_pro"]], df_jogos[["id_jogo", "competicao", "mando"]], on="id_jogo", how="inner")
    
    #REMOVENDO ESPAÇOS ANTES E DEPOIS DOS NOMES
    for col in df_gols.select_dtypes(include=["object", "string"]):
        df_gols[col] = df_gols[col].str.strip()

    #CRIANDO UM FILTRO NOS FILTROS
    competicoes, mando = filtro_comp_mando(c=competicoes, m=mando)
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

    #RENOMEANDO AS COLUNAS
    gols = gols.rename(columns={'gols': 'jogador'})
    gols = gols.rename(columns={'count': 'gols'})

    return gols.sort_values(by=("gols"), ascending=False)





def assistencias(competicoes=[], mando=[]):

    import pandas as pd


    #TABELAS QUE SERÃO USADAS
    df_escalacao = pd.read_excel("escalacoes.xlsx")
    df_jogos = pd.read_excel("jogos.xlsx")

    #FAZENDO A JUNÇÃO DOS DFs
    df_ass = pd.merge(df_escalacao[["id_jogo", "assistencias"]], df_jogos[["id_jogo", "competicao", "mando"]], on="id_jogo", how="inner")
    
    #REMOVENDO ESPAÇOS ANTES E DEPOIS DOS NOMES
    for col in df_ass.select_dtypes(include=["object", "string"]):
        df_ass[col] = df_ass[col].str.strip()
    
    #CRIANDO UM FILTRO NOS FILTROS
    competicoes, mando = filtro_comp_mando(c=competicoes, m=mando)
    df_ass = df_ass[(df_ass["competicao"].isin(competicoes)) & (df_ass["mando"].isin(mando))]


    #REMOVE JOGOS SEM GOLS
    df_ass = df_ass.dropna()

        

    #QUEBRA AS COLUNAS EM LISTAS
    df_ass["assistencias"] = df_ass["assistencias"].str.split(', ')

    #CONCATENA CADA LISTA EM UMA LISTA APENAS
    lista_ass = sum(df_ass["assistencias"], [])

    #COLOCA TODOS OS JOGADORES EM LETRAS MAIUSCULAS
    lista_ass = [item.upper() for item in lista_ass]

    #PREPARA OS DADOS PRA FAZER O DATA FRAME
    dados = {
        "assistencias": lista_ass
    }

    df_resumo_ass = pd.DataFrame(dados)
    


    #CONTAGEM DE GOLS
    ass = df_resumo_ass["assistencias"].value_counts().reset_index()

    ass = ass.rename(columns={'assistencias': 'jogador'})
    ass = ass.rename(columns={'count': 'assistencias'})

    #REMOVENDO COLUNAS COM NONE, PENALTI E FALTA
    ass = ass[~ass["jogador"].isin(["NONE", "PÊNALTI", "FALTA"])]

    return ass.sort_values(by=("assistencias"), ascending=False)





def dobradinha(competicoes=[], mando=[]):
    import pandas as pd


    #TABELAS QUE SERÃO USADAS
    df_escalacao = pd.read_excel("escalacoes.xlsx")
    df_jogos = pd.read_excel("jogos.xlsx")

    #JUNÇÃO DOS DFs
    df_gol_ass = pd.merge(df_escalacao[["id_jogo", "autor_gols_pro", "assistencias"]], df_jogos[["id_jogo", "competicao", "mando"]], on="id_jogo", how="inner")

    #REMOVENDO ESPAÇOS ANTES E DEPOIS DOS NOMES
    for col in df_gol_ass.select_dtypes(include=["object", "string"]):
        df_gol_ass[col] = df_gol_ass[col].str.strip()

    #CRIANDO UM FILTRO NOS FILTROS
    competicoes, mando = filtro_comp_mando(c=competicoes, m=mando)
    df_gol_ass = df_gol_ass[(df_gol_ass["competicao"].isin(competicoes)) & (df_gol_ass["mando"].isin(mando))]

    #REMOVENDO COLUNAS QUE NÃO SERÃO USADAS
    df_gol_ass = df_gol_ass[["autor_gols_pro", "assistencias"]]

    #REMOVENDO VALORES NULOS
    df_gol_ass = df_gol_ass.dropna()

    #QUEBRA AS COLUNAS EM LISTAS
    df_gol_ass["autor_gols_pro"] = df_gol_ass["autor_gols_pro"].str.split(', ')
    df_gol_ass["assistencias"] = df_gol_ass["assistencias"].str.split(', ')

    #CONCATENA CADA LISTA EM UMA LISTA APENAS
    lista_gol = sum(df_gol_ass["autor_gols_pro"], [])
    lista_ass = sum(df_gol_ass["assistencias"], [])

    #COLOCA TODOS OS JOGADORES EM LETRAS MAIUSCULAS
    lista_gol = [item.upper() for item in lista_gol]
    lista_ass = [item.upper() for item in lista_ass]

    #PREPARA OS DADOS PRA FAZER O DATA FRAME
    dados = {
        "gols": lista_gol,
        "assistencias": lista_ass
    }

    #CRIA O DATA FRAME
    df_dobradinha = pd.DataFrame(dados)

    #INDICA QUE NÃO IMPORTA A ORDEM DA DUPLA (A + B) OU (B + A)
    df_dobradinha["dupla"] = df_dobradinha.apply(lambda x: tuple(sorted([x["gols"], x["assistencias"]])), axis=1)

    #FAZ A CONTAGEM DE QUANTAS VEZES CADA DUPLA APARECEU
    contagem_duplas = df_dobradinha["dupla"].value_counts().reset_index()
    contagem_duplas.columns = ["dupla", "quantidade"]

    #REMOVENDO DADOS NÃO COERENTES
    contagem_duplas = contagem_duplas[contagem_duplas["dupla"].apply(lambda x: all(v not in ["NONE", "PÊNALTI", "FALTA"] for v in x))]

    #TRANFORMAR AS TUPLAS EM STRINGS
    contagem_duplas["dupla"] = contagem_duplas["dupla"].apply(lambda x: " - ".join(map(str, x)))

    return contagem_duplas.sort_values(by="quantidade", ascending=False)


def participacoes(competicoes=[], mando=[]):
    import pandas as pd

    df_gols = gols(competicoes=competicoes, mando=mando)
    df_ass = assistencias(competicoes=competicoes, mando=mando)

    df_participacoes = pd.merge(df_gols, df_ass, on="jogador", how="outer")

    #PREENCHER VALORES AUSENTES COM 0
    df_participacoes = df_participacoes.fillna(0)

    #CALCULA AS PARTICIPACOES (GOLS + ASSISTENCIAS)
    df_participacoes["participacoes"] = df_participacoes["gols"] + df_participacoes["assistencias"]

    #TRANSFORMANDOAS COLUNAS FLOAT DO DF PRO TIPO INT
    for c in df_participacoes.select_dtypes(include="float"):
        df_participacoes[c] = df_participacoes[c].astype(int)
    
    #REMOVENDO DADOS NÃO COERENTES
    df_participacoes = df_participacoes[~df_participacoes["jogador"].isin(["NONE", "PÊNALTI", "FALTA"])]

    return df_participacoes.sort_values(by="participacoes", ascending=False)    
    
    


    