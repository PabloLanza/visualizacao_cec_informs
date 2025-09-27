def gols(competicoes=(), mando=()):

    import pandas as pd

    #CRIANDO UM FILTRO NOS FILTROS
    competicoes, mando = filtro_comp_mando(c=competicoes, m=mando)

    #CONECTA NO BANCO DE DADOS
    conn = conectar_banco()

    #REMOVE JOGOS SEM GOLS
    if conn:
        df_gols = pd.read_sql(f"""SELECT e.autor_gols_pro, e.assistencias, j.competicao, j.mando
                                FROM stats.escalacoes e 
                                INNER JOIN stats.jogos j ON e.id_jogo = j.id_jogo
                                WHERE j.competicao IN{competicoes} AND j.mando IN{mando};""", conn)


    df_gols = df_gols[["autor_gols_pro", "assistencias"]]

    df_gols = df_gols.dropna()
        

    #QUEBRA AS COLUNAS EM LISTAS
    df_gols["autor_gols_pro"] = df_gols["autor_gols_pro"].str.split(', ')
    df_gols["assistencias"] = df_gols["assistencias"].str.split(", ")

    #CONCATENA CADA LISTA EM UMA LISTA APENAS
    lista_gols = sum(df_gols["autor_gols_pro"], [])
    lista_ass = sum(df_gols["assistencias"], [])

    #COLOCA TODOS OS JOGADORES EM LETRAS MAIUSCULAS
    lista_gols = [item.upper() for item in lista_gols]
    lista_ass = [item.upper() for item in lista_ass]

    #PREPARA OS DADOS PRA FAZER O DATA FRAME
    dados = {
        "gols": lista_gols,
        "assistencias": lista_ass
    }

    df_resumo_gols = pd.DataFrame(dados)
    


    #CONTAGEM DE GOLS
    gols = df_resumo_gols["gols"].value_counts().reset_index()

    gols = gols.rename(columns={'index': 'jogador'})

    return gols.sort_values("gols", ascending=False)


def filtro_comp_mando(c, m):
    if len(c) < 1:
        competicoes = ('Mineiro', 'Sul Americana', 'Brasileiro', 'Copa do Brasil')
    elif len(c) not in(1,2,3,4):
        competicoes = ('', c)
    else:
        competicoes = c

    
    if len(m) < 1:
        mando = ('Casa', 'Fora')
    elif len(m) not in(1,2):
        mando = ('', m)
    else:
        mando = m

    return competicoes, mando

def conectar_banco():
    import psycopg2

    conn = psycopg2.connect(
        dbname="cecinformsdb",
        user="cecinforms",
        password="cec1010",
        host="localhost",
        port="5434"
    )

    return conn