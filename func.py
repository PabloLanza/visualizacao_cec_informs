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



def assistencias(competicoes=[], mando=[]):

    import pandas as pd


    #TABELAS QUE SERÃO USADAS
    df_escalacao = pd.read_excel("escalacoes.xlsx")
    df_jogos = pd.read_excel("jogos.xlsx")

    #CRIANDO UM FILTRO NOS FILTROS
    competicoes, mando = filtro_comp_mando(c=competicoes, m=mando)

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


df = assistencias(competicoes=["Brasileiro", "Copa do Brasil"], mando=["Casa", "Fora"])
print(df)